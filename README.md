# ImageInquiryUI

# Deploying Flask App on AWS EC2 Instance

This guide provides detailed steps for deploying a Flask application on an Amazon EC2 instance, using Gunicorn as the WSGI server and Nginx as the web server.

## Prerequisites

- An AWS EC2 instance running.
- SSH access to your instance.
- Git installed on the instance.

## Steps

### 1. Connect to Your EC2 Instance
Use SSH to connect to your instance:
```
ssh -i "your-key.pem" ec2-user@ec2-xx-xxx-xxx-xxx.compute-1.amazonaws.com
```

### 2. Clone Your Repository
Clone your Flask app repository into the EC2 instance:
```
git clone https://github.com/yourusername/yourrepository.git
```

### 3. Set Up a Virtual Environment
Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
Install all required Python packages:
```
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Set the `FLASK_APP` environment variable:
```
export FLASK_APP=app.py
```

### 6. Start Flask Application
To run your Flask application:
```
flask run
```

### 7. Set Up Gunicorn
Install Gunicorn and run your Flask app as a WSGI application:
```
pip install gunicorn
gunicorn -b 0.0.0.0:8000 init:app
```

### 8. Create Systemd Service for Gunicorn
Create a systemd service file to manage your application with Gunicorn:
```
sudo nano /etc/systemd/system/ImageInquiryUI.service
```

Paste the following configuration:

```ini
[Unit]
Description=Gunicorn instance to serve ImageInquiryUI
After=network.target

[Service]
User=ec2-user
Group=www-data
WorkingDirectory=/home/ec2-user/ImageInquiryUI
ExecStart=/home/ec2-user/ImageInquiryUI/venv/bin/gunicorn -b localhost:8000 init:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Reload the systemd daemon and start your service:
```
sudo systemctl daemon-reload
sudo systemctl start ImageInquiryUI
sudo systemctl enable ImageInquiryUI
```

### 9. Install and Configure Nginx
Install Nginx and configure it to proxy requests to Gunicorn:
```
sudo yum install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
sudo nano /etc/nginx/nginx.conf
```

Refer to the official Flask documentation to properly configure Nginx with Flask:
[Configuring Nginx](https://flask.palletsprojects.com/en/2.3.x/deploying/nginx/)

## Conclusion

By following these steps, your Flask application should now be successfully running on an EC2 instance, served by Gunicorn, and managed by Nginx as the web server. This setup ensures that your application is robust and ready for production environments.
