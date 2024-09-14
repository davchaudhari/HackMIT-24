import os
import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from werkzeug.utils import secure_filename

def save_signature_image(signature_file, upload_folder):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    filename = secure_filename(signature_file.filename)
    signature_path = os.path.join(upload_folder, filename)
    signature_file.save(signature_path)
    return signature_path

def add_signature_to_pdf(pdf_path, signature_path, output_path, x=100, y=100, page_number=0):
    import io
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    # Create a new PDF with the signature image
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Adjust x, y, width, and height as needed
    can.drawImage(signature_path, x=x, y=y, width=200, height=50)
    can.save()

    # Move to the beginning of the BytesIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # Read the existing PDF
    existing_pdf = PdfReader(open(pdf_path, "rb"))
    output = PdfWriter()

    # Merge the signature PDF with the existing PDF
    signature_page = new_pdf.pages[0]

    # Iterate through all pages
    for page_num, page in enumerate(existing_pdf.pages):
        if page_num == page_number:  # Apply signature to the specified page
            page.merge_page(signature_page)
        output.add_page(page)

    # Write the output to a new PDF
    with open(output_path, "wb") as outputStream:
        output.write(outputStream)
    return output_path


