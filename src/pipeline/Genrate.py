from PIL import Image
import requests
import io
from src.components.memefy import understand
import cv2
from src.utils import savenft
import src.utils as utils
from src.logger import logging
import cv2
import google.generativeai as genai

template_paths = utils.template_paths


class Gen:
    def __init__(self):
        pass

    def genimg(self, prompt, animate=False, normal=False, photo=False):
        try:
            logging.info("Generating image from prompt: " + prompt)
    
            image_des, top_text, bottom_text = understand(prompt, animate, normal, photo)

            if animate:
                logging.info("Generating animate meme")
                API_URL = "https://api-inference.huggingface.co/models/cagliostrolab/animagine-xl-3.1"
                headers = {
                    "Authorization": "Bearer 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"
                }
            elif normal:
                logging.info("Generating normal meme")
                # API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
                API_URL = "https://api-inference.huggingface.co/models/fluently/Fluently-XL-Final"
                headers = {
                    "Authorization": "Bearer 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"
                }
            else:
                logging.error("Please specify either animate or normal mode")
                return None
            
            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.content

            image_bytes = query({"inputs": image_des})
            image = Image.open(io.BytesIO(image_bytes))
            image.save(utils.INPUT)
            image.save(utils.OUTPUT)
            image.close()

            return top_text, bottom_text

        except Exception as e:
            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.content
            image_bytes = query({"inputs": image_des})
            image = Image.open(io.BytesIO(image_bytes))
            image.save(utils.INPUT)
            image.save(utils.OUTPUT)
            image.close()
            logging.error("Error while generating image: " + str(e))
            return "Error while generating meme!, please try again."

    def drawimage(self, top_text, bottom_text, photo=False, normal=False):

        if photo:
            top_text, bottom_text = understand(prompt="", photo=True)

        # image = cv2.imread(utils.INPUT)
        def load_meme_template(template_path):
            img = cv2.imread(template_path)
            if img is None:
                raise FileNotFoundError(f"Image not found at {template_path}")
            return img

        # Function to add text to the image
        def add_text_to_image(img, top_text, bottom_text, font=cv2.FONT_HERSHEY_SIMPLEX):
                image_height, image_width, _ = img.shape

                # Function to wrap text
                def wrap_text(text, font, font_scale, max_width):
                    words = text.split()
                    lines = []
                    while words:
                        line = ''
                        while words and cv2.getTextSize(line + words[0], font, font_scale, 1)[0][0] <= max_width:
                            line = line + (words.pop(0) + ' ')
                        lines.append(line.strip())
                    return lines

                # Wrap top and bottom text
                font_scale = 1
                max_text_width = image_width - 20
                wrapped_top_text = wrap_text(top_text, font, font_scale, max_text_width)
                wrapped_bottom_text = wrap_text(bottom_text, font, font_scale, max_text_width)

                # Calculate positions for top text
                y_offset = 10
                shadow_offset = 2  # Offset for the shadow
                for line in wrapped_top_text:
                    text_size = cv2.getTextSize(line, font, font_scale, 1)[0]
                    text_x = (image_width - text_size[0]) // 2
                    text_y = y_offset + text_size[1]

                    # Add black shadow
                    cv2.putText(img, line, (text_x + shadow_offset, text_y + shadow_offset), font, font_scale, (0, 0, 0), 2, lineType=cv2.LINE_AA)

                    # Add white text
                    cv2.putText(img, line, (text_x, text_y), font, font_scale, (255, 255, 255), 2, lineType=cv2.LINE_AA)

                    y_offset += text_size[1] + 10

                # Calculate positions for bottom text
                y_offset = image_height - 10
                for line in reversed(wrapped_bottom_text):
                    text_size = cv2.getTextSize(line, font, font_scale, 1)[0]
                    text_x = (image_width - text_size[0]) // 2
                    text_y = y_offset

                    # Add black shadow
                    cv2.putText(img, line, (text_x + shadow_offset, text_y + shadow_offset), font, font_scale, (0, 0, 0), 2, lineType=cv2.LINE_AA)

                    # Add white text
                    cv2.putText(img, line, (text_x, text_y), font, font_scale, (255, 255, 255), 2, lineType=cv2.LINE_AA)

                    y_offset -= text_size[1] + 10
            
                    # return img
        meme = load_meme_template(utils.INPUT)
        add_text_to_image(meme, top_text, bottom_text)
        
        cv2.imwrite(utils.OUTPUT, meme)
        
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
            while words and cv2.getTextSize(line + words[0], self.font, self.font_scale, 1)[0][0] <= self.max_width:
                line = line + (words.pop(0) + ' ')
            lines.append(line.strip())
        return lines

class MemeGenerator:
    def __init__(self, api_key, template_paths):
        self.template_paths = template_paths
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

        import time

    def analyze_prompt(self, prompt, retries=8):
            for _ in range(retries):
                try:
                    data = (f"Based on the prompt: '{prompt}', which meme template would be most suitable from the following options: "
                            f"{', '.join(self.template_paths.keys())}? Also, generate a suitable top and bottom text for the meme "
                            "from your own don't just copy the user prompt, Make sure the answer you are giving the key name should be "
                            "**meme_template** and funny as possible")

                    response = self.model.generate_content(data)
                    response_text = response.text.strip().split('\n')
                    response_text = [item for item in response_text if item]

                    template_choice = response_text[0].replace("**meme_template**:", "").strip().lower().replace(" ", "_")
                    top_text = response_text[1] if len(response_text) > 1 else ""
                    top_text = top_text.replace("**Top text**:", "").replace("**top text**:","").replace("**Bottom text**:", "").replace("**bottom text**:","")
                    bottom_text = response_text[2] if len(response_text) > 2 else ""
                    bottom_text = bottom_text.replace("**Bottom text**:", "").replace("**bottom text**:","").replace("**Top text**:", "").replace(" **top text**: ","")

                    template_choice = self.clean_template_choice(template_choice)
                    template_path = self.template_paths.get(template_choice, self.template_paths[template_choice])
                    template_path = template_path.replace("\\", "/")
                    template_path = template_path.replace("/notebooks", "")

                    return template_path, top_text, bottom_text

                except Exception as e:
                    logging(f"An error occurred: {e}")
                    if retries > 0:
                        print(f"{retries}. Retrying...")
                    else:
                        print("Retries exhausted, returning None")
                        return None, None, None


    @staticmethod
    def clean_template_choice(template_choice):
        for char in ":,-'`.?!**":
            template_choice = template_choice.replace(char, "")
        template_choice = template_choice.strip()
        if template_choice.startswith('_'):
            template_choice = template_choice[1:]
        return template_choice

    @staticmethod
    def load_meme_template(template_path):
        img = cv2.imread(template_path)
        if img is None:
            raise FileNotFoundError(f"Image not found at {template_path}")
        return img

    def add_text_to_image(self, img, top_text, bottom_text, font=cv2.FONT_HERSHEY_SIMPLEX):
        image_height, image_width, _ = img.shape
        
        top_text_1 = top_text.replace("**Top text:**", "").replace("**Top text**:", "").replace("**Top Text**:", "")
        bottom_text_1 = bottom_text.replace("**Bottom text:**", "").replace("**Bottom text**:", "").replace("**Bottom Text**:", "")

        wrapper = TextWrapper(font, 1, image_width - 20)
        wrapped_top_text = wrapper.wrap_text(top_text_1)
        wrapped_bottom_text = wrapper.wrap_text(bottom_text_1)

        # Define shadow parameters
        shadow_offset = 2
        shadow_color = (0, 0, 0)  # Black shadow color

        # Calculate positions for top text
        y_offset = 10
        for line in wrapped_top_text:
            text_size = cv2.getTextSize(line, font, 1, 1)[0]
            text_x = (image_width - text_size[0]) // 2
            text_y = y_offset + text_size[1]
            # Draw shadow first
            cv2.putText(img, line, (text_x + shadow_offset, text_y + shadow_offset), font, 1, shadow_color, 2, lineType=cv2.LINE_AA)
            # Then draw text
            cv2.putText(img, line, (text_x, text_y), font, 1, (255, 255, 255), 2, lineType=cv2.LINE_AA)
            y_offset += text_size[1] + 10

        # Calculate positions for bottom text
        y_offset = image_height - 10
        for line in reversed(wrapped_bottom_text):
            text_size = cv2.getTextSize(line, font, 1, 1)[0]
            text_x = (image_width - text_size[0]) // 2
            text_y = y_offset
            # Draw shadow first
            cv2.putText(img, line, (text_x + shadow_offset, text_y - shadow_offset), font, 1, shadow_color, 2, lineType=cv2.LINE_AA)
            # Then draw text
            cv2.putText(img, line, (text_x, text_y), font, 1, (255, 255, 255), 2, lineType=cv2.LINE_AA)
            y_offset -= text_size[1] + 10
        
        cv2.imwrite(utils.OUTPUT_MEME, img)
        link = utils.savenft(utils.OUTPUT_MEME)
        return link

    def create_meme(self, prompt):
        template_path, top_text, bottom_text = self.analyze_prompt(prompt)
        img = self.load_meme_template(template_path)
        
        return self.add_text_to_image(img, top_text, bottom_text)


