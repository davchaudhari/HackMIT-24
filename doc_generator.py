# document_generator.py
from fpdf import FPDF
from flask import render_template
import os

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Add content to the PDF using data
    pdf.cell(200, 10, txt=f"Name: {data.get('name', '')}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {data.get('date', '')}", ln=True)
    # Save the PDF to a file
    output_path = 'output.pdf'
    pdf.output(output_path)
    return output_path

def fill_pdf_form(input_pdf_path, output_pdf_path, data_dict):
    import pdfrw
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    annotations = template_pdf.pages[0]['/Annots']
    for annotation in annotations:
        if annotation['/Subtype'] == '/Widget':
            field = annotation['/T'][1:-1]  # Remove parentheses
            if field in data_dict:
                annotation.update(
                    pdfrw.PdfDict(V='{}'.format(data_dict[field]))
                )
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
    return output_path

def html_to_pdf(template_name, data, output_path):
    from weasyprint import HTML
    html_out = render_template(template_name, data=data)
    HTML(string=html_out).write_pdf(output_path)
    return output_path
