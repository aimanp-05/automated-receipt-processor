# 🧾 Automated Receipt Processing System

This is a cloud-based receipt processing solution that allows users to upload receipts through a Flask frontend. Upon upload, the receipt image is stored in AWS S3, automatically processed by AWS Textract via a Lambda function, and summarized data is saved to DynamoDB. An email summary is also sent using AWS SES.

---

## 🚀 Features

- 🖼️ Upload receipt images via simple web interface
- ☁️ Images are stored securely in Amazon S3
- 🧠 AWS Textract extracts text from uploaded receipts
- 💸 Total amounts and receipt lines are parsed automatically
- 📬 Summary email sent via AWS SES
- 🗃️ Extracted data stored in DynamoDB
- 🐳 Flask frontend containerized using Docker

---

## 🧩 Tech Stack

- **Frontend:** Flask (Python), HTML/CSS
- **Cloud:** AWS S3, Lambda, Textract, DynamoDB, SES
- **Containerization:** Docker
- **Others:** Boto3, Regex

---

## 🗂️ Project Structure

```
receipt-processing-app/
├── frontend/
│   ├── app.py                 # Flask app
│   ├── templates/             # HTML templates
│   └── Dockerfile             # For containerization
├── lambda/
│   └── lambda_function.py     # AWS Lambda code
├── screenshots/
│   ├── architecture_diagram.png           
│   └── email-screenshot.png
├── README.md                  # Project documentation
```


## 📦 How It Works

1. User uploads a receipt via the Flask frontend.
2. Flask app uploads the image to AWS S3.
3. An S3 event triggers a Lambda function.
4. Lambda uses Textract to extract receipt content.
5. The parsed data is stored in DynamoDB.
6. A summary email is sent to the user via SES.

---

## 🛠️ Deployment (Optional)

You can deploy the frontend using Docker on an EC2 instance:

```bash
# In the frontend/ directory
docker build -t receipt-app .
docker run -p 5000:5000 receipt-app
```

Make sure to configure your `.env` file with AWS credentials and region.

---

## 🧳 Future Improvements

- Add user login/authentication
- Show uploaded receipts on dashboard

---

