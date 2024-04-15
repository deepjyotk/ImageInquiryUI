import base64
import hashlib
import io
import os
from flask import flash, jsonify
import http
import json
from flask import Flask, request, render_template, redirect, url_for
import boto3
import requests
import logging
from requests_toolbelt.multipart.encoder import MultipartEncoder
from PIL import Image



app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Necessary for using 'flash' in Flask

conn = http.client.HTTPSConnection("nre8g0zfrc.execute-api.us-east-1.amazonaws.com")
payload = json.dumps({
    "query": "show images of cat and dog"
})
headers = {
    'Content-Type': 'application/json'
}


@app.route('/')
def index():
    return render_template('search.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            file = request.files['file']
            custom_labels = request.form.get('customLabels', '')
            filename = file.filename
            file_ext = os.path.splitext(filename)[1].lower()

            if file_ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                return jsonify({'error': 'File format not supported.'}), 400

            # Check if the image can be opened by PIL
            try:
                img = Image.open(file.stream)
                img.verify()  # Verify that it is, in fact, an image
            except Exception as e:
                return jsonify({'error': 'Invalid image file: ' + str(e)}), 400

            # Optionally reset file stream position if other operations are needed
            file.seek(0)

            # Calculate file checksum
            hash_md5 = hashlib.md5()
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
            file_md5 = hash_md5.hexdigest()

            # Reset file stream position to the beginning before uploading
            file.seek(0)
            headers = {
                'Content-Type': file.content_type,  # Use the content type of the file uploaded
                'x-amazon-apigateway-binary-media-types': 'image/jpeg',
                'x-amz-meta-customLabels' : f'{custom_labels}'
            }


            # Proceed with upload
            api_url = f'https://nre8g0zfrc.execute-api.us-east-1.amazonaws.com/dev/upload/{filename}'
            file_data = file.read()
            response = requests.put(api_url,file_data, headers=headers)

            if response.status_code == 200:
                return jsonify({'message': 'File uploaded successfully', 'md5': file_md5})
            else:
                return jsonify({'error': 'Failed to upload file'}), 500
        
        except requests.exceptions.RequestException as e:
            # This will catch any error related to the requests library
            logging.error(f'Request failed: {e}')
            flash('Failed to make request to the server. Please try again later.', 'error')
        except Exception as e:
            # General exception for any other errors
            logging.error(f'An error occurred: {e}')
            flash('An unexpected error occurred. Please try again.', 'error')
            return redirect(url_for('index'))
       

    return render_template('upload.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        payload = json.dumps({
            "q": query
        })
        
        conn.request("GET", "/dev/search", body=payload, headers=headers)

        # Get the response
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        response_json = json.loads(data)
        body_string = response_json['body']
        urls = json.loads(body_string)
        print(data)
     
        return render_template('search.html',image_urls=urls)
        # return redirect(url_for('index'))
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
