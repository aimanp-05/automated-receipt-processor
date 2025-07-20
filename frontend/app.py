from flask import Flask, request, render_template
import boto3
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'receipt' not in request.files:
        return 'No file part'

    file = request.files['receipt']

    if file.filename == '':
        return 'No selected file'

    filename = secure_filename(file.filename)
    s3.upload_fileobj(file, BUCKET_NAME, filename)
    return 'File uploaded to S3 successfully!'

if __name__ == "__main__":
    app.run(debug=True)
