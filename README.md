# Simple-Banking-System
This is a simple banking system implemented in Python using Flask for the backend and Gradio for the user interface. The system allows users to register, log in, check their balance, and transfer funds between accounts.

#Features:
*User Registration: Users can register by providing a username and password.
*User Authentication: Registered users can log in using their username and password.
*Balance Inquiry: Users can check their account balance after logging in.
*Fund Transfer: Users can transfer funds to other accounts after logging in.

#Requirements
*Python 3.x
*Flask
*Gradio
*SQLite3
*Requests

#Installation:
1.Clone the repository:
git clone https://github.com/your_username/simple-banking-system.git
2.Navigate to the project directory:
cd simple-banking-system
3.Install the required dependencies:
pip install -r requirements.txt
4.Run the Flask server:
python app.py
5.Access the application through your web browser at http://localhost:5000.

#Usage:
*Register: Access the registration interface through the provided link or navigate to http://localhost:7860. Enter a username and password to register.
*Login: Access the login interface through the provided link or navigate to http://localhost:7861. Enter your registered username and password to log in.
*Transfer: Access the transfer interface through the provided link or navigate to http://localhost:7862. Enter the required details (sender username, sender password, receiver username, and amount) to transfer funds.
*Balance Inquiry: Access the balance inquiry interface through the provided link or navigate to http://localhost:7863. Enter your username and password to check your account balance.

#Contributing:
Contributions are welcome! Please feel free to fork the repository and submit pull requests to suggest improvements or add new features.
