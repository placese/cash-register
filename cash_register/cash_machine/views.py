from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
import json

from .servises import is_items_valid, get_items_as_list, generate_receipt, \
    generate_qr_code_with_url_to_pdf, get_qr_code_as_bytes_str, get_receipt_from_file

@csrf_exempt
@require_POST
def create_receipt(request):
    items = json.loads(request.body.decode()).get('items')
    if not items:
        return JsonResponse({'success': False, 'message': 'excpected list of items'})
    if not is_items_valid(items):
        return JsonResponse({'success': False, 'message': 'wrong item'})
    items = get_items_as_list(items)
    
    receipt_pdf = generate_receipt(items)
    
    qr_code = generate_qr_code_with_url_to_pdf(receipt_pdf)
    qr_code = get_qr_code_as_bytes_str(qr_code)
    if qr_code:
        return HttpResponse(qr_code, content_type='image/png')
    return JsonResponse({'success': False, 'message': 'something went wrong'})

@csrf_exempt
@require_GET
def get_receipt(request, receipt):
    receipt = get_receipt_from_file(receipt)
    if receipt:
        return HttpResponse(receipt, content_type='application/pdf')
    return JsonResponse({'success': False, 'message': 'no such pdf file'})
        

