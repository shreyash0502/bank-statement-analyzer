# Welcome to Bank Statement Analyzer - Made by _Shreyash Vaish_
> Analyze your bank statements received through Gmail!

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
