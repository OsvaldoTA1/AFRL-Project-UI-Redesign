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

5. Activate the virtual environment:
   - On Mac/Linux:
     ```
     source myenv/bin/activate
     ```

6. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

7. In the main directory, create a file named `cred.py`

8. In `cred.py`, include the following:
   ```
   RECAPTCHA_SITE_KEY = ''
   RECAPTCHA_SECRET_KEY = ''
   MAIL_USERNAME = ''
   MAIL_PASSWORD = ''
   ```

9. Create the following keys:
   - **ReCaptcha:**
     - [ReCaptcha Documentation](https://cloud.google.com/security/products/recaptcha)
     - [Signing up for ReCaptcha](https://www.google.com/recaptcha/admin/create) (*Note: For ReCaptcha type, select "Challenge" and "I'm not a robot" checkbox. For the domain, add both localhost and 127.0.0.1*)
     - [YouTube Video Walkthrough for Signing Up for ReCaptcha API Keys](https://www.youtube.com/watch?v=KqDW69BSdEo)
   - Once you have signed up for ReCaptcha, paste the keys into their respective variables in the `cred.py` file.

   - **Flask Mailman:**
     - [Application Password Documentation](https://support.google.com/accounts/answer/185833?hl=en)
     - [Creating Application Password](https://myaccount.google.com/apppasswords) (*Note: Save the application password.*)
   - In the `cred.py` file, paste the application password into the "MAIL_PASSWORD" variable, and use the associated email address for the "MAIL_USERNAME" variable.

10. Set up the database:
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

## How to Contribute

1. Fork the project on GitHub.
2. Clone your own forked version of the project.
3. Create a new branch for your feature or bug fix.
4. Commit your changes and push your branch to your GitHub repository.
5. Open a Pull Request from your forked repository to the original one.

Please ensure all code is properly commented and all tests pass before submitting your pull request.

We appreciate every contributor and every contribution, big or small. We look forward to working together to improve this app and adding more features soon!
