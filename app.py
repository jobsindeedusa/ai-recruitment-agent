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
