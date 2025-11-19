from flask import Flask, render_template, request, jsonify
import requests
import smtplib
import time
import threading
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

app = Flask(__name__)

# Store active monitoring tasks
active_monitors = {}

class WebsiteMonitor:
    def __init__(self, monitor_id, url, receiver_email, check_interval=300):
        self.monitor_id = monitor_id
        self.url = url
        self.receiver_email = receiver_email
        self.check_interval = check_interval
        self.is_running = False
        self.last_status = None
        
        # Your Brevo SMTP Configuration (EXACTLY from your working code)
        self.brevo_username = "9be631001@smtp-brevo.com"
        self.brevo_password = "BcSxL73sjKHCbk1z"
        self.smtp_server = "smtp-relay.brevo.com"
        self.smtp_port = 587

    def check_website(self):
        """Check if website is reachable - EXACT logic from your working code"""
        if not self.url:
            return False, "No URL configured"
            
        try:
            start_time = time.time()
            if not self.url.startswith(('http://', 'https://')):
                url_to_check = 'https://' + self.url
            else:
                url_to_check = self.url
                
            response = requests.get(url_to_check, timeout=10, allow_redirects=True)
            response_time = round((time.time() - start_time) * 1000, 2)
            
            if response.status_code == 200:
                return True, f"UP - Status: {response.status_code}, Response Time: {response_time}ms"
            else:
                return False, f"DOWN - Status: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "DOWN - Request timeout (10s)"
        except requests.exceptions.ConnectionError:
            return False, "DOWN - Connection error"
        except requests.exceptions.RequestException as e:
            return False, f"DOWN - {str(e)}"

    def send_email_brevo(self, is_up):
        """Send email notification using Brevo - EXACT logic from your working code"""
        try:
            status = "UP" if is_up else "DOWN"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if is_up:
                subject = f"🚀 WEBSITE IS UP: {self.url}"
                body = f"""
🎉 WEBSITE STATUS ALERT 🎉

Good news! The website you're monitoring is now available.

📊 Monitoring Details:
• Website: {self.url}
• Status: {status}
• Time: {timestamp}

✅ The website is responding and reachable.

You can now access it at: {self.url}

---
Automated Monitoring System (Powered by Brevo)
"""
            else:
                subject = f"⚠️ WEBSITE STATUS CHANGE: {self.url}"
                body = f"""
🔔 WEBSITE STATUS ALERT 🔔

Website status has changed.

📊 Monitoring Details:
• Website: {self.url}
• Status: {status}
• Time: {timestamp}

We'll continue monitoring and notify you when it's back up.

---
Automated Monitoring System (Powered by Brevo)
"""
            
            print(f"📧 Attempting to send email to: {self.receiver_email}")
            
            msg = MIMEMultipart()
            # Use receiver email as From address (this worked in your command line version)
            msg['From'] = self.receiver_email
            msg['To'] = self.receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to Brevo SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.brevo_username, self.brevo_password)
            server.send_message(msg)
            server.quit()
            
            print("✅ Email sent successfully via Brevo!")
            return True
            
        except Exception as e:
            print(f"❌ Brevo email failed: {e}")
            return False

    def start_monitoring(self):
        """Start monitoring in a separate thread - EXACT logic from wait_until_reachable"""
        self.is_running = True
        
        def monitor_loop():
            check_count = 0
            while self.is_running:
                check_count += 1
                is_up, details = self.check_website()
                current_status = "UP" if is_up else "DOWN"
                
                print(f"Check #{check_count}: {self.url} is {current_status} - {details}")
                
                # Update active monitors status for UI
                active_monitors[self.monitor_id]['status'] = current_status
                active_monitors[self.monitor_id]['last_check'] = datetime.now().strftime("%H:%M:%S")
                active_monitors[self.monitor_id]['check_count'] = check_count
                
                # Send notification only when status changes to UP
                if current_status != self.last_status:
                    print(f"Status changed from {self.last_status} to {current_status}")
                    
                    if is_up:  # Only send email when site comes UP
                        print("🎯 Website is UP! Sending email notification...")
                        email_sent = self.send_email_brevo(is_up)
                        if email_sent:
                            print("✅ Email notification sent successfully!")
                        else:
                            print("❌ Failed to send email notification")
                    
                    self.last_status = current_status
                
                # Stop if website is up (your requirement: run until site is reached)
                if is_up and active_monitors[self.monitor_id].get('stop_when_up', True):
                    print("🏁 Website is reachable. Stopping monitor.")
                    self.stop_monitoring()
                    break
                
                time.sleep(self.check_interval)
        
        # Start monitoring in background thread
        thread = threading.Thread(target=monitor_loop)
        thread.daemon = True
        thread.start()
        print(f"🚀 Started monitoring: {self.url}")

    def stop_monitoring(self):
        """Stop the monitoring"""
        self.is_running = False
        print(f"🛑 Stopped monitoring: {self.url}")

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_monitor', methods=['POST'])
def start_monitor():
    try:
        data = request.json
        url = data.get('url')
        receiver_email = data.get('email')
        check_interval = int(data.get('interval', 5)) * 60  # Convert to seconds
        stop_when_up = data.get('stop_when_up', True)
        
        if not url or not receiver_email:
            return jsonify({'success': False, 'error': 'URL and email are required'})
        
        # Generate unique monitor ID
        monitor_id = f"monitor_{int(time.time())}"
        
        # Create monitor instance (using your exact Python logic)
        monitor = WebsiteMonitor(monitor_id, url, receiver_email, check_interval)
        
        # Store in active monitors
        active_monitors[monitor_id] = {
            'monitor': monitor,
            'url': url,
            'email': receiver_email,
            'status': 'STARTING',
            'last_check': 'Never',
            'check_count': 0,
            'stop_when_up': stop_when_up,
            'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Start monitoring (this runs your exact Python program logic)
        monitor.start_monitoring()
        
        return jsonify({
            'success': True,
            'monitor_id': monitor_id,
            'message': f'Started monitoring {url}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/stop_monitor', methods=['POST'])
def stop_monitor():
    try:
        data = request.json
        monitor_id = data.get('monitor_id')
        
        if monitor_id in active_monitors:
            active_monitors[monitor_id]['monitor'].stop_monitoring()
            active_monitors[monitor_id]['status'] = 'STOPPED'
            return jsonify({'success': True, 'message': 'Monitoring stopped'})
        else:
            return jsonify({'success': False, 'error': 'Monitor not found'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_status', methods=['GET'])
def get_status():
    """Get status of all active monitors"""
    monitors_data = {}
    for monitor_id, info in active_monitors.items():
        monitors_data[monitor_id] = {
            'url': info['url'],
            'email': info['email'],
            'status': info['status'],
            'last_check': info['last_check'],
            'check_count': info['check_count'],
            'start_time': info['start_time']
        }
    return jsonify(monitors_data)

@app.route('/stop_all', methods=['POST'])
def stop_all():
    """Stop all active monitors"""
    for monitor_id in active_monitors:
        active_monitors[monitor_id]['monitor'].stop_monitoring()
        active_monitors[monitor_id]['status'] = 'STOPPED'
    return jsonify({'success': True, 'message': 'All monitors stopped'})

@app.route('/test_email', methods=['POST'])
def test_email():
    """Test Brevo email configuration"""
    try:
        data = request.json
        test_email = data.get('email')
        
        if not test_email:
            return jsonify({'success': False, 'error': 'Email is required'})
        
        # Test Brevo configuration (using your exact credentials)
        brevo_username = "9be631001@smtp-brevo.com"
        brevo_password = "BcSxL73sjKHCbk1z"
        smtp_server = "smtp-relay.brevo.com"
        smtp_port = 587
        
        try:
            # Test connection and login
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(brevo_username, brevo_password)
            
            # Test email send
            msg = MIMEMultipart()
            msg['From'] = test_email  # Use the same email as From
            msg['To'] = test_email
            msg['Subject'] = "📧 Test Email from Website Monitor"
            msg.attach(MIMEText("This is a test email from your Website Monitor system. If you receive this, Brevo SMTP is working correctly!", 'plain'))
            
            server.send_message(msg)
            server.quit()
            
            return jsonify({'success': True, 'message': 'Test email sent successfully! Please check your inbox.'})
            
        except smtplib.SMTPAuthenticationError:
            return jsonify({'success': False, 'error': 'Brevo authentication failed. Check username/password.'})
        except Exception as e:
            return jsonify({'success': False, 'error': f'Email test failed: {str(e)}'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 Starting Website Monitor Flask App...")
    print("📧 Using Brevo SMTP with your working credentials")
    print("🌐 Access the web UI at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)