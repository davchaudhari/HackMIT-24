import os
import fitz  # PyMuPDF
from flask import Flask, send_file
from io import BytesIO

app = Flask(__name__)

# Emulate the JSON data
json_data = {
    "id": "REDACTED",
    "sender": {
        "name": "John Doe",  # Fake Employer Name
        "email": "john.doe@fakemail.com"
    },
    "recipients": [
        "interactioncocalifornia@gmail.com"
    ],
    "subject": "[HackMIT-easy] Bill of Sale"
}

# Sample function to create a test PDF with signature fields
def create_sample_pdf():
    pdf_document = fitz.open()
    page = pdf_document.new_page()

    # Add sample content
    page.insert_text((50, 100), "Sample Bill of Sale", fontsize=20)
    page.insert_text((50, 150), "This is a sample bill of sale for demonstration.", fontsize=12)
    
    # Add signature placeholders
    page.insert_text((50, 600), "Employer Signature: ____________________", fontsize=12)
    page.insert_text((50, 650), "Employee Signature: ____________________", fontsize=12)

    # Save the PDF to a BytesIO stream
    sample_pdf = BytesIO()
    pdf_document.save(sample_pdf)
    pdf_document.close()

    sample_pdf.seek(0)
    print("Sample PDF created successfully.")
    return sample_pdf

# Function to add signature image from file to the PDF
def sign_pdf_with_image(pdf_bytes, image_path):
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    # Add signature at predefined locations
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")

        # Check if signature placeholders exist
        if "Employer Signature" in text:
            print("Found Employer Signature field.")
            # Move the image up by reducing the y-coordinates
            signature_rect = fitz.Rect(50, 570, 250, 620)  # Moved up by 20 pixels
            page.insert_image(signature_rect, filename=image_path)
            print(f"Employer signature image placed at coordinates: {50}, {570}, {250}, {620}")

    # Save the signed PDF
    signed_pdf = BytesIO()
    pdf_document.save(signed_pdf)
    pdf_document.close()

    signed_pdf.seek(0)
    print("PDF signed with image successfully.")
    return signed_pdf

# Route to sign and serve the signed document
@app.route('/sign-and-download', methods=['GET'])
def sign_and_download():
    # Step 1: Generate a sample PDF
    sample_pdf = create_sample_pdf()

    # Step 2: Path to the signature image (use absolute path to ensure it's found)
    # signature_image_path = os.path.join(os.getcwd(), 'templates', 'signature.png')

    # Step 3: Sign the document using the image
    signed_pdf = sign_pdf_with_image(sample_pdf, 'signature.png')

    # Step 4: Return the signed PDF
    return send_file(signed_pdf, as_attachment=True, download_name='signed_document.pdf')

if __name__ == '__main__':
    app.run(debug=True)
