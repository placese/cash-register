from jinja2 import Template
import pdfkit
from datetime import datetime
import pytz

import uuid

from cash_register import settings

import qrcode
import tempfile

from .models import Item, Receipt
from .serializers import ItemSerializer


def is_items_valid(items: list) -> bool:
    """Returns True if each item exists in database"""
    query_set = Item.objects.all().values_list('id', flat=True)
    items = set(items)
    for item in items:
        if item not in query_set:
            return False
    return True

def generate_receipt(items: list) -> None:
    """Generates pdf template, saves, writes to model, and returns it's filename"""
    receipt = _generate_pdf_receipt(_generate_html_receipt(items))
    Receipt.objects.create(receipt=receipt)
    return receipt

def get_items_as_list(items: dict) -> list:
    """Returns list of items as list with qty field"""
    query_set = Item.objects.filter(id__in=list(set(items)))
    items_quantity = {i: items.count(i) for i in items}
    items = []
    for item in query_set:
        item = dict(ItemSerializer(item).data)
        item['qty'] = items_quantity[item['id']]
        items.append(item)
    return items

def _generate_html_receipt(items: list) -> str:
    """Generates html template and returns it"""
    with open ('./cash_machine/static/templates/receipt.html') as f:
        template = Template(f.read())
    total_price = sum(item['price'] * item['qty'] for item in items)
    generated_datetime = datetime.now(tz=pytz.timezone('EUROPE/MOSCOW')).strftime("%d.%m.%Y %H:%M")
    
    return template.render(
            items=items,
            total_price=total_price,
            date=generated_datetime
    )

def _generate_pdf_receipt(html_receipt: str):
    """Generates pdf receipt, saves it and returns it's filename"""
    options = {
        'encoding': 'UTF-8'
    }
    pdf_receipt = str(uuid.uuid4())
    pdfkit.from_string(
        input=html_receipt,
        output_path=f'./cash_machine/media/{pdf_receipt}.pdf',
        options=options)
    return pdf_receipt

def generate_qr_code_with_url_to_pdf(pdf_filename: str) -> str:
    """Generates qr code with url to pdf receipt, saves it and returns it's filename"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'http://{settings.ROOT_HOST}/media/{pdf_filename}.pdf')
    qr.make(fit=True)
    img = qr.make_image()
    qr_file_name = f'{tempfile.NamedTemporaryFile().name}.png'
    img.save(qr_file_name)
    return qr_file_name

def get_qr_code_as_bytes_str(path_to_qr_code: str) -> bytes | None:
    """Tries to read qr code. If success, returns it as bytes, else returns None"""
    try:
        with open(path_to_qr_code, 'rb') as f:
            return f.read()
    except:
        return

def get_receipt_from_file(receipt: str) -> bytes | None:
    """Tries to read receipt. If success, returns it as bytes, else returns None"""
    try:
        pdfFileObj = open(f'./cash_machine/media/{receipt}', 'rb')
        return pdfFileObj
    except:
        return
