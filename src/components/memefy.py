import google.generativeai as genai  
from src.logger import logging  
import src.utils as utils  
from PIL import Image


def understand(prompt, animate=False, normal=False, photo=False):
    try:
        genai.configure(api_key="AIzaSyBa5b8ZuK83ehPi52ua4Ly724ofJHTT5Zk")
        model = genai.GenerativeModel("gemini-pro")

        def generate_caption(prompt_text, max_attempts=8):
            for _ in range(max_attempts):
                try:
                    response = model.generate_content(prompt_text)
                    response_text = [item.strip() for item in response.text.split('\n') if item]
                    
                    if len(response_text) >= 2:
                        image_description = response_text[0].replace("**image_description:**", "").lower().strip()
                        top_text = response_text[1].replace("**top_text:**", "").replace("**top_text**:", "")
                        bottom_text = response_text[2].replace("**bottom_text:**", "").replace("\\", "").replace("**bottom_text**:", "") if len(response_text) > 2 else ""
                        return image_description, top_text, bottom_text
                except Exception as e:
                    logging.error(f"Error generating content: {e}")
            
            raise Exception(f"Failed to generate content after {max_attempts} attempts.")

        def enhance_prompt(base_prompt, context):
            return (f"{base_prompt} The meme should be witty, engaging, and include very good humor, you are free to pick any type of humor best suited for the image. "
                    f"Here’s some context for better understanding: {context}. "
                    "Make sure to format the response with the keys **image_description**, **top_text**, and **bottom_text** for clarity. make sure top and bottom text are of 4-6 words each and funny.")
            
        if normal or animate:
            prompt_text = enhance_prompt(
                f"Create a humorous meme based on the prompt: '{prompt}'.", 
                "This is for an image meme. Provide a funny and fitting image description make sure it humor should be relavenat to top and bottom text, top text, and bottom text."
            )
            return generate_caption(prompt_text)

        elif photo:
            def get_gemini_response(input, image_path):
                
                image = Image.open(image_path) 
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                if input != "":
                    response = model.generate_content([input, image])
                else:
                    response = model.generate_content(image)
                
                return response.text

            try:
                output = get_gemini_response("This photo is going to be used as a meme give a description of it do our accordling so that at next request to gemini model can make good meme of it ", utils.INPUT)
                prompt_text = f"The meme should be witty, engaging, and include humor,you are free to pick any type of humor best suited for the image.. Based on the image description: '{output}', generate a meme. The user's feelings about the image are: '{prompt}'. This is for an image meme with both top and bottom text.Format the response using the keys **top_text** and **bottom_text**. Ensure both texts are funny and consist of 5-6 words each."
                
                for _ in range(8):
                    try:
                        response = model.generate_content(prompt_text)
                        response_text = [item.strip() for item in response.text.split('\n') if item]
                        
                        top_text = response_text[0].replace("**top_text:**", "").replace("**top_text**:", "") if len(response_text) > 0 else ""
                        bottom_text = response_text[1].replace("**bottom_text:**", "").replace("\\", "").replace("**bottom_text**:", "") if len(response_text) > 1 else ""
                        return top_text, bottom_text
                    except Exception as e:
                        logging.error(f"Error generating meme content: {e}")
            
            except Exception as e:
                logging.error(f"Error querying API: {e}")
                return e
                
    except Exception as e:
        logging.error(f"Error in understand function: {e}")
        return "Error: Please try again!"
