from flask import Flask, render_template, request
import os
import PyPDF2
from transformers import pipeline

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            file.save(os.path.join("uploads", file.filename))
            pdf_text = extract_text_from_pdf(file)
            return render_template('index.html', text=pdf_text)
    return render_template('index.html')

def extract_text_from_pdf(file):
    with open(os.path.join("uploads", file.filename), 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = [page.extract_text() for page in reader.pages]
        return ' '.join(text)

@app.route('/ask', methods=['POST'])
def ask():
    context = request.form['text']
    question = request.form['question']
    answer = generate_answer(context, question)
    return render_template('index.html', text=context, question=question, answer=answer)

def generate_answer(context, question):
    nlp = pipeline("question-answering")
    result = nlp({
        'question': question,
        'context': context
    })
    return result['answer']

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
