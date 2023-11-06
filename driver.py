from flask import Flask, request, jsonify, render_template
from datetime import datetime
import pandas as pd
import re
import os.path
import base64
import PyPDF2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def download_attachment(service, user_id, msg_id, store_dir, count):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        for part in message['payload']['parts']:
            if part['filename'] and part['filename'].endswith('.pdf'):
                attachment = service.users().messages().attachments().get(userId=user_id, messageId=msg_id, id=part['body']['attachmentId']).execute()
                file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                file_path = os.path.join(store_dir, str(count))
                with open(file_path, 'wb') as f:
                    f.write(file_data)
                return file_path
    except HttpError as error:
        print(f'An error occurred while downloading attachment: {error}')
    return None

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()
    return text

def extract_transactions_from_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    opening_balance_pattern = r'([\d,.]+)\n([\d,.]+)\n([\d,.]+)\n([\d,.]+)\nCurrent Account'

    opening_balance_match = re.search(opening_balance_pattern, text)
    if opening_balance_match:
        opening_balance_value = opening_balance_match.group(1).replace(',', '')
        opening_balance = float(opening_balance_value)
    else:
        opening_balance = None

    transaction_pattern = r'(\d{2}/\d{2}/\d{4})\n([\w\s-]+)\n([\d,]+\.\d{2})\n([\d,]+\.\d{2})'
    transaction_matches = re.findall(transaction_pattern, text)

    transactions = []

    init_balance = opening_balance

    for match in transaction_matches:
        date, description, amount, balance = match
        amount = float(amount.replace(',', ''))
        balance = float(balance.replace(',', ''))
        
        transaction_type = 'Credit' if balance - init_balance > 0 else 'Debit'
        
        init_balance = balance
        
        transaction_data = {
            'date': date,
            'description': description.strip(),
            'amount': amount,
            'type': transaction_type,
            'balance': balance
        }
        transactions.append(transaction_data)

    if opening_balance:
        print(f'Opening Balance: {opening_balance}')
    else:
        print('Opening Balance not found in the text.')
        
    return opening_balance, transactions

def process_email():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'cred.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me', q='subject:"Bank statement"').execute()
        messages = results.get('messages', [])

        if not messages:
            print('No emails with the subject "Bank statement" found.')
            return

        print('Emails with the subject "Bank statement":')
        
        sendersList = []
        
        count = 0
        
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            subject = None
            for header in msg['payload']['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
                    break
            sender = None
            for header in msg['payload']['headers']:
                if header['name'] == 'From':
                    sender = header['value']
                    break
            if subject:
                # Download the PDF attachment
                pdf_path = download_attachment(service, 'me', message['id'], 'downloaded_pdfs', count)
                if pdf_path:
                    print(f'Subject: {subject}')
                    print(f'Sender: {sender}')
                    timestamp = int(msg['internalDate']) / 1000  # Convert milliseconds to seconds
                    email_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    print(f'Email Time: {email_time}')
                    print(f'PDF downloaded to: {pdf_path}')
                    sendersList.append(sender)
                    count += 1

    except HttpError as error:
        print(f'An error occurred: {error}')
        return jsonify({'error': str(error)})
    
    return sendersList
    
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/process_email', methods=['GET'])
def api_process_email():
    try:
        sendersList = process_email()
        return render_template('senders.html', senders=enumerate(sendersList))
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/process_email/<int:index>', methods=['GET'])
def sender_details(index):
    try:
        opening_balance, transactions = extract_transactions_from_pdf('downloaded_pdfs/' + str(index))
        if transactions:
            print('Extracted transactions:')
            for transaction in transactions:
                print(transaction)
        else:
            print('No transactions found.')
        if not transactions:
            return jsonify({'error': 'No transactions found'})
        return render_template('transactions.html', transactions=transactions, opening_balance=opening_balance)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
