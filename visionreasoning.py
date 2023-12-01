import base64
from io import BytesIO
from PIL import Image
import requests
import json
import re
import json



api_key = "sk-h15jsz6j9hq2WUtBPaOPT3BlbkFJsL8GHS4O6fN0BTCueMs"

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
    return response






