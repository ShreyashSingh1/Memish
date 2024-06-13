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

            text = understand(prompt, animate, normal, photo)

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

            image_bytes = query({"inputs": text})
            image = Image.open(io.BytesIO(image_bytes))
            image.save(utils.INPUT)
            image.save(utils.OUTPUT)
            image.close()

            return text

        except Exception as e:
            image_bytes = query({"inputs": text})
            image = Image.open(io.BytesIO(image_bytes))
            image.save(utils.INPUT)
            image.save(utils.OUTPUT)
            image.close()
            logging.error("Error while generating image: " + str(e))
            return "Error while generating meme!, please try again."

    def drawimage(self, text1, photo=False, normal=False):

        if photo:
            text = understand(prompt="", photo=True)

        else:
            text = text1.replace('"', "")
            text = text1.replace("*", "")

        image = cv2.imread(utils.INPUT)

        # Calculate font scale based on image width and desired maximum text height
        max_text_height = 0.2 * image.shape[0]  # Adjust the value as needed
        font_scale = 1
        while True:
            # Choose font
            font = cv2.FONT_HERSHEY_SIMPLEX

            # Determine text size
            text_size, _ = cv2.getTextSize(text, font, font_scale, thickness=2)

            # Break the loop if the text height is within the desired maximum height
            if text_size[1] <= max_text_height:
                break

            # Reduce font scale if text height exceeds the maximum
            font_scale -= 0.05

        # Calculate text position (centered horizontally and at the top)
        text_x = (image.shape[1] - text_size[0]) // 2
        text_y = text_size[1] + 50  # Adjust the value to position the text

        # Add drop shadow effect (black outline)
        shadow_offset = 4

        # Split text into lines
        words = text.split()
        lines = [""]
        current_line_index = 0
        for word in words:
            # Check if adding this word would exceed 4 words per line
            if len(lines[current_line_index].split()) < 4:
                lines[current_line_index] += word + " "
            else:
                lines.append(word + " ")
                current_line_index += 1

        # Add the title lines to the image
        for i, line in enumerate(lines):
            # Determine text size for the current line
            text_size, _ = cv2.getTextSize(line, font, font_scale, thickness=2)

            # Calculate text position for the current line (centered horizontally)
            text_x = (image.shape[1] - text_size[0]) // 2
            text_y += text_size[1] + 10  # Adjust the value to set line spacing

            # Add drop shadow effect (black outline)
            cv2.putText(
                image,
                line,
                (text_x + shadow_offset, text_y + shadow_offset),
                font,
                font_scale,
                (0, 0, 0),  # Black color for drop shadow
                thickness=2,
                lineType=cv2.LINE_AA,
            )

            # Add the text
            cv2.putText(
                image,
                line,
                (text_x, text_y),
                font,
                font_scale,
                (255, 255, 255),  # White color for the text
                thickness=2,
                lineType=cv2.LINE_AA,
            )

        # Save the image with the text
        cv2.imwrite(utils.OUTPUT, image)

        value = savenft(path=utils.OUTPUT)

        return value
    

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

    def analyze_prompt(self, prompt, retries=5):
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


