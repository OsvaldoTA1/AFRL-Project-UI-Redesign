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

6. Set up the database:
   ```
   flask db upgrade
   ```

7. Run the Flask server:
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
