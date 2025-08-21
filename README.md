# TrustVest Media Flask Application

## Description

This is an investment assessment website built with Flask and Jinja templates. The standout feature of this app is the implementation of the OCEAN model of personality traits. Each user completes a personality test based on this model, and their results are stored and displayed on their profile. Based on the results, the website will route you automatically to your personalized investment strategy so that you can gain insights on how you invest and what methods resonate with your style. 

*TrustVest does NOT offer real investment advice and should you feel like you need some, we recommend seeing a licensed financial advisor.*

## How to Install
1. Open the terminal in your IDE and navigate to where you want the project located.

2. Clone the repository, in your terminal run:
   ```
   git clone https://github.com/Fabeo10/AFRL-Project.git
   ```

3. Navigate to the project directory:
   ```
   cd AFRL_Project
   ```

4. Create a virtual environment:
   ```
   python3 -m venv myenv
   ```
   Keep in mind if you have multiple Python versions installed you might run into some issues.
   Make sure your environment variables are set up correctly OR delete other Python versions.
   For stability try Python 3.12.10 since that's the version this was made on. However, it is possible other versions could work! 
   If this still doesn't work force venv to use your Python 3.12.10 version by explictly pointing to it. For example:
   ```
   "C:\Program Files\Python312\python.exe" -m venv myenv
   ```
6. Activate the virtual environment:
   - On Mac/Linux:
     ```
     source myenv/bin/activate
     ```

7. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
   Double Check your venv folder or venv subfolders to see if it installed correctly, you do not want to install these on your system to avoid errors with your other projects.

   **If it didn't install correctly run this command:**
   ```
   python -m pip uninstall -r requirements.txt -y
   ```
   and remake your env and run pip install -r requirements.txt again.
   
9. In the main directory, create a file named `cred.py`

10. In `cred.py`, include the following:
   ```
   RECAPTCHA_SITE_KEY = ''
   RECAPTCHA_SECRET_KEY = ''
   MAIL_USERNAME = ''
   MAIL_PASSWORD = ''
   REPLICATE_API_TOKEN = ''
   ```
   If you're doing the optional APIS:
   ```
   RECAPTCHA_SITE_KEY = ''
   RECAPTCHA_SECRET_KEY = ''
   MAIL_USERNAME = ''
   MAIL_PASSWORD = ''
   REPLICATE_API_TOKEN = ''

   REPLICATE_API_TOKEN = ''

   IPINFO_TOKEN = ''
   COLLECT_IPS = True
   IP_ENCRYPTION_KEY=""
   ```

11. Create the following keys:
   - **ReCaptcha:**
     - [ReCaptcha Documentation](https://cloud.google.com/security/products/recaptcha)
     - [Signing up for ReCaptcha](https://www.google.com/recaptcha/admin/create) (*Note: For ReCaptcha type, select "Challenge" and "I'm not a robot" checkbox. For the domain, add both localhost and 127.0.0.1*)
     - [YouTube Video Walkthrough for Signing Up for ReCaptcha API Keys](https://www.youtube.com/watch?v=KqDW69BSdEo)
   - Once you have signed up for ReCaptcha, paste the keys into their respective variables in the `cred.py` file.

   - **Flask Mailman:**
     - [Application Password Documentation](https://support.google.com/accounts/answer/185833?hl=en)
     - [Creating Application Password](https://myaccount.google.com/apppasswords) (*Note: Save the application password.*)
   - In the `cred.py` file, paste the application password into the "MAIL_PASSWORD" variable, and use the associated email address for the "MAIL_USERNAME" variable.

   **OPTIONAL NOT REQUIRED TO RUN THE PROGRAM**
   - **Replicate:**
      - [Replicate Documentation](https://replicate.com/docs)
      - [Signing up for Replicate](https://replicate.com/signin)
      - [API Token](https://replicate.com/account/api-tokens)
   - After setting up your billing information locate your API token and paste it into the `cred.py` file. "REPLICATE_API_TOKEN"
   - **Keep in mind this is not needed and the app _will_ work without this. However you will not get generated images, only the default fallback images.**

   - **IPInfo:**
      - [IPInfo Documentation](https://ipinfo.io/developers)
      - [Signing up for IPInfo](https://ipinfo.io/signup)
      - [API Token](https://ipinfo.io/dashboard/token)
   -  In the `cred.py` file, paste the API token into the "IPINFO_TOKEN" variable.
   -  **Keep in mind this is not needed and the app _will_ work without this. However you will not get geo data**

   - **COLLECT_IPS:**
      - This is **NOT** an API token, this is for developers. If you want to keep tracking on leave it as is, you can set it as False if you don't want it.

   - **IP_ENCRYPTION_KEY**
      - This is also **NOT** an API token but it is sensitive and you need to keep this safe. If you want geo data then you need to include this to encrypt sensitive information.
      - To generate an encryption key run this command (after activating your virtual environment since it requires a library already included in requirements.txt)
         -
           ```
           python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
           ```
      - After doing this, in the `cred.py` file, paste the generated encryption key into the "IP_ENCRYPTION_KEY" variable.
      - **Keep in mind this is not needed and the app _will_ work without this. However you will not get geo data since this is required to store IP data even if you have the IPInfo API token**

11. Set up the database:
   ```
   flask db stamp head
   flask db migrate -m "Resetting migrations"
   flask db upgrade
   ```

11. (macOS only) If you encounter an SSL certificate error when logging in or during reCAPTCHA validation, run this once to install the necessary certificates:

   ```
   /Applications/Python\ 3.11/Install\ Certificates.command

   ```

12. Run the Flask server:
   ```
   flask run
   ```

**===========================OPTIONAL===========================**

13. To make sure the chatbot works on your local you need to do the following:
   - Download ollama on your local machine (choose the right version for your local machine): https://ollama.com/ 
   - Run the installer and follow the on-screen instructions
   - After installation confirm that you successfully installed ollama by running this command on a **new** terminal/command prompt window.
        ```
        ollama --version
        ```
   - Restart your workspace and reactivate your virtual environment (Only if you haven't already, otherwise skip this step)
   - In your virtual environment download the llama3 model with this command. This might take several minutes depending on your internet connection.
        ```
        ollama pull llama3
        ```
   - Verify that llama3 was downloaded by running:
        ```
        ollama3
        ```
   - Restart the Flask Server and enjoy!

14. If you completed all the optional parts in step 10 and 11:
    You can now run a script that will return your database tables.
    Simply run this (In your virtual environment):
    ```
    python display_tables.py
    ```
    OR
    ```
    python display_tables.py --decrypt
    ```
    KEEP IN MIND SINCE THIS YOU ARE RUNNING A LOCAL DATABASE THE ONLY INFORMATION DISPLAYED ARE USERS YOU CREATED!

## How to Contribute

1. Fork the project on GitHub.
2. Clone your own forked version of the project.
3. Create a new branch for your feature or bug fix.
4. Commit your changes and push your branch to your GitHub repository.
5. Open a Pull Request from your forked repository to the original one.

Please ensure all code is properly commented and all tests pass before submitting your pull request.

We appreciate every contributor and every contribution, big or small. We look forward to working together to improve this app and adding more features soon!
