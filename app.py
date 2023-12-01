from flask import Flask, render_template, request, jsonify, redirect, url_for
import base64
import os
import random
from visionreasoning import question_generation, answer_generation

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
    image_path_original = os.path.join('static/original-image', images[current_image_index])

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    response = None
    i = 0
    while response is None:
        response = question_generation(image_path_original)
        if i > 3:
            break
        i = i + 1

    print(type(response))

    return render_template('reasoning.html', image_data=encoded_image, example_dict=response)

@app.route('/next_image', methods=['POST'])
def next_image():
    global current_image_index
    current_image_index += 1

    if current_image_index < len(images):
        image_path = os.path.join('static/modified-image', images[current_image_index])
        image_path_original = os.path.join('static/original-image', images[current_image_index])
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        response = None
        
        i = 0
        while response is None:
            response = question_generation(image_path_original)
            if i > 3:
                break
            i = i + 1

        return jsonify({'image_data': encoded_image, 'new_dict': response})
    else:
        return jsonify({'no_more_images': True})

@app.route('/send_text', methods=['POST'])
def send_text():
    global current_image_index
    text_data = request.form.get('textData', '')
    received_text = request.form.get('receivedText', '')  # Get the existing received text
    # Concatenate the new text with the existing received text
    concatenated_text = f"{received_text} {text_data}".strip()
    image_path_original = os.path.join('static/original-image', images[current_image_index])
    answer = answer_generation(image_path_original, concatenated_text)
    return jsonify({'received_text': answer})

@app.route('/thank_you')
def thank_you():
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
