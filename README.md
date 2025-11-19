🌐 Website Monitor
A powerful web-based application that monitors websites and sends email notifications when they become available. Built with Python Flask backend and a beautiful responsive frontend.

✨ Features
🔍 Real-time Website Monitoring: Continuously checks website availability

📧 Email Notifications: Sends alerts via Brevo SMTP when sites become reachable

🎯 Web Interface: Beautiful, responsive UI for easy management

⚡ Multiple Monitors: Run multiple website monitors simultaneously

🛑 Smart Stopping: Automatically stops when website becomes reachable

📊 Live Status Updates: Real-time monitoring status in the web interface

🚀 Quick Start
Prerequisites
Python 3.7+

Brevo SMTP account (free tier available)

Installation
Clone or download the project files:

bash
mkdir website-monitor
cd website-monitor
Create the project structure:

text
website-monitor/
│
├── app.py
├── requirements.txt
└── templates/
    └── index.html
Set up virtual environment (recommended):

bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
Install dependencies:

bash
pip install -r requirements.txt
Run the application:

bash
python app.py
Access the web interface:
Open your browser and navigate to: http://localhost:5000

📧 Email Configuration
This application uses Brevo SMTP for sending email notifications:

Brevo SMTP Settings (Pre-configured):
text
SMTP Server: smtp-relay.brevo.com
Port: 587
Username: 9be631001@smtp-brevo.com
Password: BcSxL73sjKHCbk1z
To use your own Brevo account:
Sign up at brevo.com

Get your SMTP credentials from the Brevo dashboard

Update the credentials in app.py:

python
self.brevo_username = "your_brevo_username"
self.brevo_password = "your_brevo_password"
🎯 How to Use
Starting a Monitor
Open the web interface at http://localhost:5000

Fill in the monitoring details:

Website URL: The website you want to monitor (e.g., https://example.com)

Notification Email: Where to send alerts when the site becomes available

Check Interval: How often to check the website (in minutes)

Stop when reachable: Automatically stop monitoring when site becomes available

Click "Start Monitoring"

Monitor the status in the Active Monitors section

Features in the Web Interface
📊 Real-time Status: See current status of all monitors (UP/DOWN/STARTING/STOPPED)

⏰ Last Check Time: When each monitor last checked the website

🔢 Check Count: Total number of checks performed

🛑 Stop Controls: Stop individual monitors or all monitors at once

🧪 Email Test: Test your email configuration before starting monitors

🔧 API Endpoints
The application provides these REST API endpoints:

GET / - Serve the web interface

POST /start_monitor - Start a new website monitor

POST /stop_monitor - Stop a specific monitor

POST /stop_all - Stop all active monitors

GET /get_status - Get status of all monitors

POST /test_email - Test email configuration

🐛 Troubleshooting
Email Not Sending
Test email configuration using the "Test Email Configuration" button

Check Brevo credentials in app.py

Verify sender email is configured in your Brevo account

Check spam folder for test emails

Website Not Being Monitored
Verify URL format - include http:// or https://

Check internet connection

Verify the website is actually down (try accessing it manually)

Application Not Starting
Check Python version (python --version)

Verify all dependencies are installed (pip list)

Check port 5000 is not being used by another application

📁 Project Structure
text
website-monitor/
│
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── website_monitor.log   # Application logs (auto-generated)
└── templates/
    └── index.html        # Web interface frontend
🔒 Security Notes
The application runs on localhost:5000 by default

Brevo SMTP credentials are hardcoded - consider using environment variables for production

Monitor only websites you own or have permission to monitor

🌟 Usage Examples
Monitor a single website:
json
{
  "url": "https://my-website.com",
  "email": "admin@mycompany.com",
  "interval": 5,
  "stop_when_up": true
}
Monitor multiple websites simultaneously:
Start multiple monitors from the web interface

Each monitor runs independently in its own thread

Receive separate notifications for each website

📄 License
This project is open source and available under the MIT License.

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check issues page.

📞 Support
If you encounter any problems or have questions:

Check the terminal output for error messages

Verify all installation steps were followed

Test email configuration separately

Check the generated website_monitor.log file for detailed logs

Happy Monitoring! 🎉
