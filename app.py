from flask import Flask, render_template, request, jsonify, redirect, url_for
import base64
import os
import random

app = Flask(__name__)

images = ["image-1.jpg", "image-2.jpg", "image-3.jpg", "image-4.jpg", "image-5.jpg", "image-6.jpg", "image-7.jpg"]
current_image_index = 0

def generate_random_dict():
    return {f"key{num}": f"value{random.randint(1, 100)}" for num in range(1, 4)}

@app.route('/')
def consent():
    return render_template('consent.html')

@app.route('/next_page', methods=['POST'])
def next_page():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    global current_image_index
    current_image_index = 0
    image_path = os.path.join('static/modified-image', images[current_image_index])
    
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    example_dict = generate_random_dict()
    return render_template('reasoning.html', image_data=encoded_image, example_dict=example_dict)

@app.route('/next_image', methods=['POST'])
def next_image():
    global current_image_index
    current_image_index += 1

    if current_image_index < len(images):
        image_path = os.path.join('static/modified-image', images[current_image_index])
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        new_dict = generate_random_dict()
        return jsonify({'image_data': encoded_image, 'new_dict': new_dict})
    else:
        return jsonify({'no_more_images': True})

@app.route('/send_text', methods=['POST'])
def send_text():
    text_data = request.form.get('textData', '')
    return jsonify({'received_text': text_data})

@app.route('/thank_you')
def thank_you():
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
