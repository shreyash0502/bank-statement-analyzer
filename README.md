# Welcome to Bank Statement Analyzer - Made by _Shreyash Vaish_
> Analyze your bank statements received through Gmail!

### What is this app for?
The app can access the user's gmail account, parse the emails containing bank statements, analyze those bank statements, and extract the transactions present in those bank statements.

### Step-by-step guide to run this application:

1. Start by cloning the repo in your system using CMD:
```
git clone https://github.com/shreyash0502/bank-statement-analyzer.git
```
2. Create a python virtual environment:
```
py -m venv myvenv
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```

The following steps are needed to connect and parse emails received through Gmail:

4. Go to https://console.cloud.google.com/welcome and create a new project.
5. Enable Gmail API for this newly created project.
6. Create the "OAuth Client ID" credentials. If prompted, configure the consent screen with your personal Gmail ID. Remember to add your personal Gmail ID in the test users (while configuring the consent screen).
7. Download the credentials as 'cred.json' and save them in the root directory.

Now that the initial setup is done, we need to set-up some emails that match our requirements:

8. Visit https://templatelab.com/bank-statement/ and choose the first template. Generate two or three bank statements using this template by filling some numbers and dates.
9. Send these bank statements to your personal Gmail ID. Sender Ids should be unique (can be same as well, unique preferred). Each email should necessarily have "Bank statement" in Subject line.
![image](https://github.com/shreyash0502/bank-statement-analyzer/assets/56553419/73230316-b207-4267-a4c3-8be1c3683307)
10. Run the application using:
```
py driver.py
```

### APIs Description:
1. ('/', method = 'GET') - Takes the user to the homepage where they can find the button to process the emails.
![image](https://github.com/shreyash0502/bank-statement-analyzer/assets/56553419/fce83a23-f019-4140-8c7e-0e02fdbf6d81)

2. ('/process_email', method = 'GET') - Parse the emails of the user, find mails with subject "Bank statement" and download the PDFs. The page also contains the buttons to take the user to the processed transactions.
![image](https://github.com/shreyash0502/bank-statement-analyzer/assets/56553419/427a7465-2e2f-4bab-b17a-433137fbd1f1)

3. ('/process_email/<int:index>', method = 'GET') - Displays the transactions extracted from the bank statement corresponding to a particular PDF represented by index.
![image](https://github.com/shreyash0502/bank-statement-analyzer/assets/56553419/d7e2de36-3fac-4c6b-8410-acb458576cdb)


### Explanation of the code structure:

* The process_email() function gets called as soon as the '/process_email' API is hit. This function takes care of establishing connection with Gmail, parsing the emails having subject "Bank statement", downloading and saving the attached PDFs. This function returns the list of senders corresponding to the parsed emails, which is then displayed to the front end as seen in the above attached images.
* The process_email() funtion makes use of a helper function download_attachment() to download and save the PDFs attached with the retrieved emails based on subject "Bank statement".
* When the user requests for transactions from a particular sender by hitting '/process_email/<int:index>', the extract_transactions_from_pdf() function gets called which makes use of a helper function extract_text_from_pdf() to extract and return the opening balance and all the transactions in the form of a python dictionary.

### Live demo: https://www.youtube.com/watch?v=DLe9ZP51fhE
