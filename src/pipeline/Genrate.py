from PIL import Image
import requests
import io
from src.components.memefy import understand
import cv2
from src.utils import savenft
import src.utils as utils
from src.logger import logging


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


if __name__ == "__main__":
    gen = Gen()
    gen.genimg("rivers")
