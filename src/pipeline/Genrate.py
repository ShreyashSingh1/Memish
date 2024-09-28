from PIL import Image
import requests
import io
from PIL import Image, ImageFont, ImageDraw
from src.components.memefy import understand
import cv2
from src.utils import savenft
import src.utils as utils
from src.logger import logging
import cv2
import google.generativeai as genai
import numpy as np

template_paths = utils.template_paths
   
class GenPhoto:
    def __init__(self):
        pass

    def genimg(self, prompt, animate=False, normal=False, photo=False):
        try:
            logging.info(f"Generating image from prompt: {prompt}")
            result = understand(prompt, animate, normal, photo)
            logging.info(f"Understand function returned: {result}")
            
            if len(result) != 3:
                logging.error(f"Unexpected return value from understand function: {result}")
                return "Error: Failed to generate meme."
            
            image_des, top_text, bottom_text = result

            if animate or normal:
                model_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
                if animate:
                        self.query_and_generate_image(model_url, image_des+ " "+ "make this image look like anime", top_text, bottom_text)
                else:
                        self.query_and_generate_image(model_url, image_des, top_text, bottom_text)
                return top_text, bottom_text
            
            logging.error("Neither 'animate' nor 'normal' mode specified")
            return "Error: Please specify a valid mode."

        except Exception as e:
            logging.error(f"Error in genimg function: {e}")
            return "Error: Failed to generate meme."

    def query_and_generate_image(self, api_url, image_des, top_text, bottom_text):
        try:
            headers = {"Authorization": "Bearer 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"}
            # Query the API to generate the image
            response = requests.post(api_url, headers=headers, json={"inputs": image_des})
            response.raise_for_status()  # Raises an error for unsuccessful status codes

            # Alternative: Directly decode image bytes using OpenCV
            np_arr = np.frombuffer(response.content, np.uint8)  # Convert the byte content to a numpy array
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # Decode the numpy array to an image

            # Ensure image decoding was successful
            if image is None:
                raise Exception("Failed to decode the image from response bytes.")

            # Save the image using OpenCV
            cv2.imwrite(utils.INPUT, image)  # Save the input for further processing
            cv2.imwrite(utils.OUTPUT, image)  # Save the output for later use
    
            return "Image generated successfully!"
        except Exception as e:
            logging.error(f"Error querying API: {e}")
            return "Error: Failed to generate image."


    def drawimage(self, top_text, bottom_text, photo=False, normal=False, prompt=" "):
        if photo:
            top_text, bottom_text = understand(prompt=prompt, photo=True)

        def load_meme_template(template_path):
            img = cv2.imread(template_path)
            if img is None:
                raise FileNotFoundError(f"Image not found at {template_path}")
            return img

        def add_text_to_image(img, top_text, bottom_text, font_path, font_size=45):
            image_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(image_pil)
            font = ImageFont.truetype(font_path, font_size)

            def wrap_text(text, font, max_width):
                words = text.split()
                lines = []
                while words:
                    line = ''
                    while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
                        line = line + (words.pop(0) + ' ')
                    lines.append(line.strip())
                return lines

            image_width, image_height = image_pil.size
            max_text_width = image_width - 20

            wrapped_top_text = wrap_text(top_text, font, max_text_width)
            wrapped_bottom_text = wrap_text(bottom_text, font, max_text_width)

            y_offset = image_height // 16  # Shift the top text down slightly more
            shadow_offset = 2

            for line in wrapped_top_text:
                text_bbox = draw.textbbox((0, 0), line, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = (image_width - text_width) // 2
                text_y = y_offset

                draw.text((text_x + shadow_offset, text_y + shadow_offset), line, font=font, fill=(0, 0, 0))
                draw.text((text_x, text_y), line, font=font, fill=(255, 255, 255))

                y_offset += text_height + 10

            y_offset = image_height * 5.3 // 6 # Shift the bottom text up slightly more
            for line in wrapped_bottom_text:
                text_bbox = draw.textbbox((0, 0), line, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = (image_width - text_width) // 2
                text_y = y_offset

                draw.text((text_x + shadow_offset, text_y + shadow_offset), line, font=font, fill=(0, 0, 0))
                draw.text((text_x, text_y), line, font=font, fill=(255, 255, 255))

                y_offset += text_height + 10

            img = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
            return img
        if photo:
            size = 142
        else:
            size = 45
        meme = load_meme_template(utils.INPUT)
        meme_with_text = add_text_to_image(meme, top_text, bottom_text, utils.FONT, font_size=size)
        
        cv2.imwrite(utils.OUTPUT, meme_with_text)
        
        return savenft(utils.OUTPUT)






class TextWrapper:
    def __init__(self, font, font_scale, max_width):
        self.font = font
        self.font_scale = font_scale
        self.max_width = max_width

    def wrap_text(self, text):
        words = text.split()
        lines = []
        while words:
            line = ''
            while words and self.get_text_width(line + words[0]) <= self.max_width:
                line = line + (words.pop(0) + ' ')
            lines.append(line.strip())
        return lines

    def get_text_width(self, text):
        return self.font.getsize(text)[0]


class MemeGenerator:
    def __init__(self, api_key, template_paths):
        self.template_paths = template_paths
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def analyze_prompt(self, prompt, retries=3):
        query_template = (
            f"Based on the prompt: '{prompt}', suggest the most suitable meme template "
            f"from the following options: {', '.join(self.template_paths.keys())}. "
            "Also, generate a suitable top and bottom text for the meme. you are free to use any type of humor you like but make sure it's funny."
            "Make sure the response includes **meme_template**, **top_text**, and **bottom_text**, and make it funny. the to text and bottom text should be of 1-7 words. not more than that."
        )

        for attempt in range(retries):
            try:
                response = self.model.generate_content(query_template)
                response_text = response.text.strip().split('\n')

                # Clean and extract template choice and texts
                template_choice = response_text[0].replace("**meme_template**:", "").strip().lower().replace(" ", "_")
                top_text = response_text[1].replace("**top_text**:", "").strip()
                bottom_text = response_text[2].replace("**bottom_text**:", "").strip()

                template_choice = self.clean_template_choice(template_choice)
                template_path = self.template_paths.get(template_choice)
                if not template_path:
                    raise ValueError(f"Template '{template_choice}' not found.")

                return template_path, top_text, bottom_text
            except Exception as e:
                logging.error(f"Error in generating meme content: {e}. Retrying ({retries - attempt - 1} attempts left)...")
                if attempt == retries - 1:
                    return None, None, None

    @staticmethod
    def clean_template_choice(template_choice):
        # Remove unwanted characters from template choice
        for char in ":,-'`.?!**":
            template_choice = template_choice.replace(char, "")
        template_choice = template_choice.strip('_')
        return template_choice

    @staticmethod
    def load_meme_template(template_path):
        img = cv2.imread(template_path)
        if img is None:
            raise FileNotFoundError(f"Image not found at {template_path}")
        return img

    def add_text_to_image(self, img, top_text, bottom_text, font_path, font_size=45):
        image_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image_pil)
        font = ImageFont.truetype(font_path, font_size)

        def wrap_text(text, max_width):
            words = text.split()
            lines = []
            while words:
                line = ''
                while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
                    line = line + (words.pop(0) + ' ')
                lines.append(line.strip())
            return lines

        image_width, image_height = image_pil.size
        max_text_width = image_width - 20

        # Wrapping the top and bottom text
        wrapped_top_text = wrap_text(top_text, max_text_width)
        wrapped_bottom_text = wrap_text(bottom_text, max_text_width)

        y_offset = 10
        shadow_offset = 2

        # Add top text
        for line in wrapped_top_text:
            self.draw_shadowed_text(draw, line, font, y_offset, image_width, shadow_offset)
            text_height = draw.textbbox((0, 0), line, font=font)[3]
            y_offset += text_height + 15

        # Adjust y_offset for bottom text and add bottom text
        y_offset = image_height - 30  # Adjust this value for text placement
        for line in reversed(wrapped_bottom_text):
            y_offset -= draw.textbbox((0, 0), line, font=font)[3] + 5
            self.draw_shadowed_text(draw, line, font, y_offset, image_width, shadow_offset)

        # Convert back to OpenCV format and save
        img = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        cv2.imwrite(utils.OUTPUT, img)
        return savenft(utils.OUTPUT)

    @staticmethod
    def draw_shadowed_text(draw, text, font, y, image_width, shadow_offset):
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (image_width - text_width) // 2

        # Draw shadow
        draw.text((text_x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0))
        # Draw text
        draw.text((text_x, y), text, font=font, fill=(255, 255, 255))

    def create_meme(self, prompt, font_path, font_size=45):
        template_path, top_text, bottom_text = self.analyze_prompt(prompt)
        if not template_path:
            raise ValueError("No suitable template found.")

        meme = self.load_meme_template(template_path)
        return self.add_text_to_image(meme, top_text, bottom_text, font_path, font_size)
