import base64
from io import BytesIO
from PIL import Image
import requests
import json
import re
import json



api_key = "sk-h15jsz6j9hq2WUtBPaOPT3BlbkFJsL8GHS4O6fN0BTCueM"

def call_gpt4_with_image(base64_image, prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{prompt}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response = response.json()
    message_content = response['choices'][0]['message']['content']
    return message_content



def convert_string_to_dict(input_string):
    start_index = input_string.find('{')
    end_index = input_string.rfind('}')

    if start_index != -1 and end_index != -1:
        json_string = input_string[start_index:end_index + 1]

        # Replace single quotes with double quotes to make it valid JSON
        json_compatible_string = json_string.replace("'", '"').replace('\\"', '"')

        # Parse the JSON-compatible string as a dictionary
        try:
            result_dict = json.loads(json_compatible_string)
            return result_dict
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None
    else:
        print("JSON content not found in the input string.")
        return None



def question_gpt(img_data):
    prompt = f"""
    Task : Create multiple questions about this image that might comes to the mind if vision people see this image. 
    Output Format: Give your answer in python dictonary format. 
    Example format: 'question_1': 'How many animals are in this image?', 'question_2': 'What the dog is doing with the cat?', 'question_3': 'How many boxes are there?'
    Don't give extra inforamtion other than the dictonary format.
    Question Topic: Commonsense reasoning, arithmatic reasoning,  creative reasoning, probabilistic reasoning, deductive reasoning ,inductive reasoning ,abductive reasoning ,analogical reasoning, spatial reasoning, temporal reasoning, causal reasoning,moral and Ethical reasoning, metacognitive reasoning,social reasoning, diagnostic reasoning ,strategic reasoning,intuitive reasoning, explanatory reasoning
    """
    response = call_gpt4_with_image(img_data, prompt)
    # print("question_gpt response", response)
    questions_about_image = convert_string_to_dict(response)

    return questions_about_image




def encode_image(image_path: str):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
    
def question_generation(image_path):
    # print("this is the image path", image_path)
    base64_image = encode_image(image_path)
    response = question_gpt(base64_image)

    return response

def answer_generation(image_path, prompt):
    base64_image = encode_image(image_path)
    response = call_gpt4_with_image(base64_image, prompt)
    print("answer_gpt response", response)
    return response

def brute_dictonary(image_path):
    if image_path == "static/original-image/image-1.jpg":
        return {'question_1': 'What is the large animal in the image?', 'question_2': 'What time of day does the image seem to depict?', 'question_3': 'How many motorcycles can be seen in the image?', 'question_4': 'Why might the elephant be in an urban setting?', 'question_5': 'What emotions might people in the image feel upon seeing the elephant?', 'question_6': 'Are the vehicles in motion or parked?', 'question_7': 'What kind of businesses might be in the buildings in the background?','question_8': 'Could the presence of the elephant pose a danger in this environment?', 'question_9': 'How might the elephant have come to be in this location?', 'question_10': 'What is the probable relationship between the elephant and the people around?'
}
    if image_path == "static/original-image/image-2.jpg":
        return {'question_1': 'How many tents are visible in this image?', 'question_2': 'Is this location indoors or outdoors?', 'question_3': 'What is the condition of the building shown in the image?', 'question_4': 'What might be the reason for the puddles on the floor?', 'question_5': 'Are there any people in the image?', 'question_6': 'What time of day does it appear to be?', 'question_7': 'What might have caused the building to be in this state?', 'question_8': 'Is there any furniture visible in the space?', 'question_9': 'What could be the purpose of the tents in this setting?', 'question_10': 'Does the building appear to be currently inhabited?', 'question_11': 'What seems to be the emotional state of the person in the image?', 'question_12': 'Can you see any form of lighting equipment inside the room?', 'question_13': 'Is there evidence of recent human activity in the space?', 'question_14': 'What could the writings on the wall suggest?', 'question_15': 'Assuming the person in the image is standing in the center, what is the approximate size of the room based on the positioning of the tents?'}
    if image_path == "static/original-image/image-3.jpg":
        return {'question_1': 'Why might the person be in the water with the dog?', 'question_2': 'Is the person helping the dog or are they both engaged in an activity?', 'question_3': 'Does the dog appear to be enjoying the activity?', 'question_4': 'What safety measures are visible for both the human and the dog?', 'question_5': 'How effective do those safety measures seem?', 'question_6': 'What is the likely relationship between the human and the dog?', 'question_7': 'Is this scenario more likely to be a rescue training or a leisure activity?', 'question_8': 'Why might the person have chosen to wear a wetsuit?', 'question_9': 'What could be the purpose of the colorful item the dog is attached to?', 'question_10': 'What time of day does this activity appear to be taking place?'}
    if image_path == "static/original-image/image-4.jpg":
        return {'question_1': 'What are the people doing in the image?', 'question_2': 'How many people are visible in the image?', 'question_3': 'What type of vehicle is in the background?', 'question_4': 'Are the people facing towards or away from the camera?', 'question_5': 'What is the possible reason for the hand gestures of the people?', 'question_6': 'What time of day does the lighting suggest?', 'question_7': 'What might the individuals be looking at?', 'question_8': 'Is the location next to a road, and can it be inferred from the image?', 'question_9': 'Are there any identifiable emotions on the faces of the people?', 'question_10': 'What type of environment are the people in (urban, rural)?'}  
    if image_path == "static/original-image/image-5.jpg":
        return {'question_1': 'What is the object located at the bottom of the image?', 'question_2': 'Is the elephant actually in the water or is it an edited image?', 'question_3': 'What might be the purpose of showing an elephant with this object?', 'question_4': 'Can an elephant really swim like depicted in the image?', 'question_5': 'What does the splash around the elephant suggest?', 'question_6': 'What kind of product is being advertised?', 'question_7': 'Is the size ratio between the elephant and the bottle realistic?', 'question_8': 'What reasoning could be behind using an elephant in this advertisement?', 'question_9': 'How does the image try to convey the effectiveness of the product?', 'question_10': 'What kind of reasoning might one use to interpret the message of this advertisement?'}
    if image_path == "static/original-image/image-6.jpg":
        return {'question_1': 'What is the relationship between the two individuals in the image?', 'question_2': 'What is the weather like in the scene depicted in the image?', 'question_3': 'What are the two individuals looking at?', 'question_4': 'What time of day does it appear to be?', 'question_5': 'Are the individuals dressed appropriately for the weather?', 'question_6': 'What might the conversation between the two individuals be about?', 'question_7': 'Is the terrain flat or sloped where the individuals are standing?', 'question_8': 'What decade does the fashion in the image suggest it belongs to?', 'question_9': 'Why might the image be in black and white?', 'question_10': 'Based on the body language, how do the two individuals seem to be feeling?'}
    if image_path == "static/original-image/image-7.jpg":
        return {'question_1': 'What is the man doing in the image?', 'question_2': 'Which era does the image likely come from based on the man’s attire and the cash register design?', 'question_3': 'How many items can be seen on the counter?', 'question_4': 'What might be the price of the watermelon?', 'question_5': 'Is this a contemporary setting or a historical one?', 'question_6': 'Why might the person be wearing a badge?', 'question_7': 'What would happen if the cash register stops working?', 'question_8': 'Based on the items on the counter, what kind of store might this be?', 'question_9': 'What is the significance of the number displayed on the cash register?', 'question_10': 'If the man is the cashier, what kind of responsibilities does he have?', 'question_11': 'Based on the image, can we deduce if the man is happy in his job?', 'question_12': 'What could the tubular object next to the cash register be?', 'question_13': 'Is the man interacting with someone outside the frame?', 'question_14': 'How is the man’s posture related to his task?', 'question_15': 'If the image was taken in the morning, what could the man be preparing for?'}
    else:
        return {'error': 'error '}





