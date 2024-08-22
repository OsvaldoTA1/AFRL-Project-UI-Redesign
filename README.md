# TrustVest Media Flask Application

## Description

This is an investment assessment website built with Flask and Jinja templates. The standout feature of this app is the implementation of the OCEAN model of personality traits. Each user completes a personality test based on this model, and their results are stored and displayed on their profile. Based on the results, the website will route you automatically to your personalized investment strategy so that you can gain insights on how you invest and what methods resonate with your style. 

*TrustVest does NOT offer real investment advice and should you feel like you need some, we recommend seeing a licensed financial advisor.*

## How to Install

1. Clone the repository:
   ```
   git clone https://github.com/Fabeo10/AFRL-Project.git
   ```

2. Navigate to the project directory:
   ```
   cd AFRL
   ```

3. Create a virtual environment:
   ```
   python3 -m venv myenv
   ```

4. Activate the virtual environment:
   - On Mac/Linux:
     ```
     source myenv/bin/activate
     ```

5. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

6. Open the codebase with your IDE
   - Visual Studio Code:
      ```
      code .
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

10. Open the terminal in your IDE and enter your virtual environment:
   - On Mac/Linux:
     ```
     source myenv/bin/activate
     ```

11. Set up the database:
   ```
   flask db stamp head
   flask db migrate -m "Resetting migrations"
   flask db upgrade
   ```

12. Run the Flask server:
   ```
   flask run
   ```

## How to Contribute

1. Fork the project on GitHub.
2. Clone your own forked version of the project.
3. Create a new branch for your feature or bug fix.
4. Commit your changes and push your branch to your GitHub repository.
5. Open a Pull Request from your forked repository to the original one.

Please ensure all code is properly commented and all tests pass before submitting your pull request.

We appreciate every contributor and every contribution, big or small. We look forward to working together to improve this app and adding more features soon!
