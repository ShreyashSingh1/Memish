import requests
import google.generativeai as genai
from src.logger import logging
import src.utils as utils


def understand(prompt, animate=False, normal=False, photo=False):
    try:
        genai.configure(api_key="AIzaSyBa5b8ZuK83ehPi52ua4Ly724ofJHTT5Zk")
        model = genai.GenerativeModel("gemini-pro")

        if animate:
            try:
                response = model.generate_content(
                    f"Context provided by the user: {prompt}, write a hilarious meme caption in 7-10 words, in the style of popular memers, meme should be relevent to anime community."
                )
            except Exception as e:
                 response = model.generate_content(
                    f"Context provided by the user: {prompt}, write a hilarious meme caption in 7-10 words, in the style of popular memers, meme should be relevent to anime community."
                )
        elif normal:
            try:
                response = model.generate_content(
                    f"Context provided by the user: {prompt}, write a hilarious meme caption in 7-10 words, in the style of popular memes."
                )
            except Exception as e:
                response = model.generate_content(
                    f"Context provided by the user: {prompt}, write a hilarious meme caption in 7-10 words, in the style of popular memes."
                )
        elif photo:
            API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
            headers = {"Authorization": "Bearer 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"}

            ## Image understanding
            def query(filename):
                with open(filename, "rb") as f:
                    data = f.read()
                response = requests.post(API_URL, headers=headers, data=data)
                return response.json()

            output = query(utils.INPUT)
            
            try: 
                response = model.generate_content(
                    f"Write a funny meme caption in 7-10 words, in the style of popular Indian internet humor, based on the following description of a photo :{output[0]['generated_text']}"
                )
            except Exception as e:
                response = model.generate_content(
                    f"Write a funny meme caption in 7-10 words, in the style of popular Indian internet humor, based on the following description of a photo :{output[0]['generated_text']}"
                )

        if animate:
            text = str(response.text)
            text = text.replace("Caption:", "")
            text = text.replace("Meme", "")
            text = text.replace("*", "")
            print(text)

        else:
            text = str(response.text)
            text = text.replace("Caption:", "")
            text = text.replace("*", "")
            print(text + 'NOR<AL')

        return text

    except Exception as e:
        logging.error(f"Error in understand function: {str(e)}")
        return "Error: Please try again!"
