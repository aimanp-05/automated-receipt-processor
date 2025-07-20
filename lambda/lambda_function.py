import boto3
import re
import json
from datetime import datetime

# Initialize AWS clients
ses = boto3.client('ses')
textract = boto3.client('textract')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ReceiptSummaries')

# Replace with your verified SES email
TO_EMAIL = "aimanp055@gmail.com"
FROM_EMAIL = "aimanp055@gmail.com"

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    response = textract.analyze_document(
        Document={'S3Object': {'Bucket': bucket, 'Name': key}},
        FeatureTypes=['FORMS']
    )

    lines = []
    vendor = "Not identified"
    date = "Not found"

    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text = block['Text']
            lines.append(text)

            # Attempt to detect vendor (first line heuristic)
            if vendor == "Not identified":
                vendor = text

            # Look for date
            date_match = re.search(r'\b\d{2}[/-]\d{2}[/-]\d{2,4}\b', text)
            if date_match:
                date = date_match.group(0)

    # Save to DynamoDB
    table.put_item(
        Item={
            'receipt_id': key,
            'uploaded_at': datetime.now().isoformat(),
            'vendor': vendor,
            'date': date,
            'lines': lines
        }
    )

    # Prepare HTML body for email
    html_body = f"""
    <html>
    <body>
        <h2>🧾 Receipt Summary</h2>
        <p><strong>Vendor:</strong> {vendor}</p>
        <p><strong>Date:</strong> {date}</p>
        <hr/>
        <h4>Full Extracted Text:</h4>
        <ul>
            {''.join(f'<li>{line}</li>' for line in lines)}
        </ul>
        <p style="color: #888;">Uploaded: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </body>
    </html>
    """

    # Send email using SES
    ses.send_email(
        Source=FROM_EMAIL,
        Destination={'ToAddresses': [TO_EMAIL]},
        Message={
            'Subject': {'Data': '🧾 New Receipt Processed'},
            'Body': {
                'Html': {'Data': html_body}
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Receipt processed successfully!')
    }
