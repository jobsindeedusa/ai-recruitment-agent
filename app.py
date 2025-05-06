from flask import Flask, request, render_template
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    job_description = request.form.get('job_description')
    resume = request.form.get('resume')
    # Dummy match logic
    score = 87
    return render_template('result.html', score=score)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, render_template, request
import fitz  # PyMuPDF
import docx
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(filepath):
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files.get('resume')
        if uploaded_file and allowed_file(uploaded_file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(filepath)

            if filepath.endswith('.pdf'):
                resume_text = extract_text_from_pdf(filepath)
            else:
                resume_text = extract_text_from_docx(filepath)

            # You can now run matching logic here using resume_text
            return render_template('result.html', extracted=resume_text)

        return "Invalid file format", 400

    return render_template('index.html')
