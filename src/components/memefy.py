import requests
import google.generativeai as genai  # Assuming this is your library import
from src.logger import logging  # Assuming this is your logger import
import src.utils as utils  # Assuming this is your utility module

def understand(prompt, animate=False, normal=False, photo=False):
    try:
        genai.configure(api_key="AIzaSyBa5b8ZuK83ehPi52ua4Ly724ofJHTT5Zk")
        model = genai.GenerativeModel("gemini-pro")

        def generate_caption(prompt_text):
            max_attempts = 8
            response = None
            for _ in range(max_attempts):
                try:
                    response = model.generate_content(prompt_text)
                    response_text = response.text.strip().split('\n')
                    response_text = [item for item in response_text if item]

                    image_description = response_text[0].replace("**image_description:**", "").strip().lower()
                    top_text = response_text[1] if len(response_text) > 1 else ""
                    top_text = top_text.replace("**top_text:**", "")
                    bottom_text = response_text[2] if len(response_text) > 2 else ""
                    bottom_text = str(bottom_text).replace("**bottom_text:**", "").replace("**Bottom text:**", "").replace("\\", "")
                    
                    return image_description, top_text, bottom_text
           
                except Exception as e:
                    logging.error(f"Error generating content: {str(e)}")
                    pass  # Retry on exception

            raise Exception(f"Failed to generate content after {max_attempts} attempts.")
            
        if normal or animate:
            prompt_text = f"Based on the prompt: '{prompt}', generate suitable image description top and bottom text for the image meme. Make sure the answer includes the key name as **image_description:**,**top_text**, **bottom_text:** key should same as given above and is as funny as possible."
            image_des, top_t, bottom_t = generate_caption(prompt_text)
        elif photo:
            API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
            headers = {"Authorization": "Bearer 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"}

            def query_api(filename):
                max_attempts = 8
                for _ in range(max_attempts):
                    try:
                        with open(filename, "rb") as f:
                            data = f.read()
                        response = requests.post(API_URL, headers=headers, data=data)
                        if response.status_code == 200:
                            return response.json()
                    except Exception as e:
                        logging.error(f"Error querying API: {str(e)}")
                        pass  # Retry on exception

                raise Exception(f"Failed to query API after {max_attempts} attempts.")

            try:
                output = query_api(utils.INPUT)
                data = f"Based on the image description '{output[0]['generated_text']}', generate suitable toop  and bottom text for the image meme. Make sure the answer includes the key name as **top_text**, **bottom_text:** key should same as given above and is as funny as possible."

                response = model.generate_content(data)
                    
                response_text = response.text.strip().split('\n')
                response_text = [item for item in response_text if item]

                # image_description = response_text[0].replace("**image_description:**", "").strip().lower()
                top_text_photo = response_text[0] if len(response_text) > 1 else ""
                top_text_photo = top_text_photo.replace("**top_text:**", "")
                bottom_text_photo = response_text[1] if len(response_text) > 1 else ""
                bottom_text_photo = str(bottom_text_photo).replace("**bottom_text:**", "").replace("**Bottom text:**", "").replace("\\", "")
                
                return top_text_photo, bottom_text_photo
                
                
            except Exception as query_exception:
                logging.error(f"Failed to query API: {str(query_exception)}")
                return "Error: Failed to query API"
            
            
        return image_des, top_t, bottom_t
            


    except Exception as e:
        logging.error(f"Error in understand function: {str(e)}")
        return "Error: Please try again!"
