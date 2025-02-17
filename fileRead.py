# app.py
from flask import Flask, request, jsonify
import pdfplumber
from docx import Document
import win32com.client as win32

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_extension = file.filename.split('.')[-1].lower()
        if file_extension == 'pdf':
            content = read_pdf(file)
        elif file_extension in ['doc', 'docx']:
            content = read_doc(file, file_extension)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        return jsonify({'content': content}), 200

def read_pdf(file):
    content = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content += page.extract_text() + "\n"
    return content

def read_doc(file, file_extension):
    if file_extension == 'docx':
        doc = Document(file)
        content = "\n".join([para.text for para in doc.paragraphs])
    elif file_extension == 'doc':
        word = win32.gencache.EnsureDispatch('Word.Application')
        word.Visible = False
        doc = word.Documents.Open(file)
        content = doc.Content.Text
        doc.Close(False)
        word.Quit()
    return content

if __name__ == '__main__':
    app.run(debug=True)