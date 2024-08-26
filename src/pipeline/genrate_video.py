import cv2
import subprocess
import os
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import src.utils as utils

class TextWrapper:
    def __init__(self, font, max_width):
        self.font = font
        self.max_width = max_width

    def wrap_text(self, text):
        words = text.split()
        lines = []
        while words:
            line = ''
            while words and ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), line + words[0], font=self.font)[2] <= self.max_width:
                line = line + (words.pop(0) + ' ')
            lines.append(line.strip())
        return lines

class VedioGenerator:
    def __init__(self, api_key, template_paths, font_path):
        self.template_paths = template_paths
        self.font_path = font_path
        self.font = ImageFont.truetype(font_path, 30)  
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def analyze_prompt(self, prompt, retries=15):
        for _ in range(retries):
            try:
                data = (f"Based on the prompt: '{prompt}', which video template would be most suitable from the following options: "
                        f"{', '.join(self.template_paths.keys())}? Also, generate suitable top and bottom text for the video meme. "
                        "Make sure the answer includes the key name as **meme_template** key should same as given above and is as funny as possible.")

                response = self.model.generate_content(data)
                response_text = response.text.strip().split('\n')
                response_text = [item for item in response_text if item]

                template_choice = response_text[0].replace("**meme_template**:", "").strip().lower().replace(" ", "_")
                top_text = response_text[1] if len(response_text) > 1 else ""
                top_text = top_text.replace("**Top text:**", "").replace("**Top text**:", "").replace("**Top Text**:", "").replace("**top_text:**", "").replace("**top_text**:", "")

                bottom_text = response_text[2] if len(response_text) > 2 else ""
                bottom_text = bottom_text.replace("**Bottom text:**", "").replace("**Bottom text**:", "").replace("**Bottom Text**:", "").replace("**bottom_text:**", "").replace("**bottom_text**:", "")

                template_choice = self.clean_template_choice(template_choice)
                template_path = self.template_paths.get(template_choice, self.template_paths[template_choice])
                template_path = template_path.replace("\\", "/")

                return template_path, top_text, bottom_text

            except Exception as e:
                print(f"An error occurred: {e}")
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
    def load_video_template(template_path):
        cap = cv2.VideoCapture(template_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"Video not found at {template_path}")
        return cap

    def add_text_to_video(self, video_path, top_text, bottom_text, output_path):
        cap = self.load_video_template(video_path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = None
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        wrapper = TextWrapper(self.font, frame_width - 20)
        wrapped_top_text = wrapper.wrap_text(top_text)
        wrapped_bottom_text = wrapper.wrap_text(bottom_text)

        for frame_num in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break
            if out is None:
                out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

            # Convert frame to PIL image
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_image)

            # Calculate positions and draw top text
            y_offset = 10
            for line in wrapped_top_text:
                text_size = draw.textbbox((0, 0), line, font=self.font)
                text_x = (frame_width - text_size[2]) // 2
                text_y = y_offset
                draw.text((text_x, text_y), line, font=self.font, fill="white", stroke_width=2, stroke_fill="black")
                y_offset += text_size[3] + 10

            # Calculate positions and draw bottom text
            y_offset = frame_height - 50  # Adjust based on font size
            for line in reversed(wrapped_bottom_text):
                text_size = draw.textbbox((0, 0), line, font=self.font)
                text_x = (frame_width - text_size[2]) // 2
                text_y = y_offset - text_size[3]
                draw.text((text_x, text_y), line, font=self.font, fill="white", stroke_width=2, stroke_fill="black")
                y_offset -= text_size[3] + 10

            # Convert back to OpenCV frame
            frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            out.write(frame)

        cap.release()
        if out:
            out.release()

    def create_video_meme(self, prompt, output_path):
        template_path, top_text, bottom_text = self.analyze_prompt(prompt)
        self.add_text_to_video(template_path, top_text, bottom_text, output_path)

        # Use FFmpeg to extract audio from the original template video
        audio_file = 'temp_audio.aac'
        extract_audio_command = f'ffmpeg -i {template_path} -q:a 0 -map a {audio_file}'
        try:
            subprocess.run(extract_audio_command, shell=True, check=True)

            # Combine the new video with the extracted audio
            temp_output_file = 'temp_output_with_audio.mp4'
            combine_command = f'ffmpeg -i {output_path} -i {audio_file} -c copy -map 0:v:0 -map 1:a:0 {temp_output_file}'
            subprocess.run(combine_command, shell=True, check=True)

            # Clean up and replace the final output
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(temp_output_file, output_path)

            # Remove the temporary audio file
            os.remove(audio_file)
            # os.remove('temp_output_with_audio.mp4')
            
            return utils.savenft(utils.OUTPUT_VEDIO)

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e}")

import cv2
import subprocess
import os
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import src.utils as utils


class TextWrapper1:
    def __init__(self, font, max_width):
        self.font = font
        self.max_width = max_width

    def wrap_text(self, text):
        lines = []
        words = text.split()
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = self.font.getbbox(test_line)
            text_width = bbox[2] - bbox[0]
            if text_width <= self.max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines


class VideoMeme:
    def __init__(self, api_key, font_path):
        self.font_path = font_path
        self.font = ImageFont.truetype(font_path, 30)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def analyze_prompt(self, prompt, retries=15):
        for _ in range(retries):
            try:
                data = (f"Based on the prompt: '{prompt}' "
                        "generate suitable top and bottom text for the video meme. "
                        "Make sure the answer includes the key name as **Top text:**, **Bottom text:** key should same as given above and is as funny and crazy as possible")

                response = self.model.generate_content(data)
                response_text = response.text.strip().split('\n')
                response_text = [item for item in response_text if item]

                top_text = response_text[0] if len(response_text) > 0 else ""
                top_text = top_text.replace("**Top text:**", "").replace("**Top text**:", "").replace("**Top Text**:", "").strip()

                bottom_text = response_text[1] if len(response_text) > 1 else ""
                bottom_text = bottom_text.replace("**Bottom text:**", "").replace("**Bottom text**:", "").replace("**Bottom Text**:", "").strip()

                return top_text, bottom_text

            except Exception as e:
                print(f"An error occurred: {e}")
                retries -= 1
                if retries > 0:
                    print(f"{retries} retries left...")
                else:
                    print("Retries exhausted, returning None")
                    return None, None

    @staticmethod
    def load_video_template(video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"Video not found at {video_path}")
        return cap

    def add_text_to_video(self, video_path, top_text, bottom_text, output_path):
        cap = self.load_video_template(video_path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = None
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Wrap text for top and bottom
        wrapper = TextWrapper1(self.font, frame_width - 20)
        wrapped_top_text = wrapper.wrap_text(top_text)
        wrapped_bottom_text = wrapper.wrap_text(bottom_text)

        for frame_num in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break
            if out is None:
                out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

            # Convert frame to PIL image for text drawing
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_image)

            # Draw top text
            y_offset = 10
            for line in wrapped_top_text:
                text_size = draw.textbbox((0, 0), line, font=self.font)
                text_x = (frame_width - text_size[2]) // 2
                text_y = y_offset
                draw.text((text_x, text_y), line, font=self.font, fill="white", stroke_width=2, stroke_fill="black")
                y_offset += text_size[3] + 10

            # Draw bottom text
            y_offset = frame_height - 50
            for line in reversed(wrapped_bottom_text):
                text_size = draw.textbbox((0, 0), line, font=self.font)
                text_x = (frame_width - text_size[2]) // 2
                text_y = y_offset - text_size[3]
                draw.text((text_x, text_y), line, font=self.font, fill="white", stroke_width=2, stroke_fill="black")
                y_offset -= text_size[3] + 10

            # Convert back to OpenCV frame
            frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            out.write(frame)

        cap.release()
        if out:
            out.release()

    def create_video_meme(self, prompt, video_path, output_path):
        top_text, bottom_text = self.analyze_prompt(prompt)
        if not top_text or not bottom_text:
            print("Error: No text returned.")
            return

        self.add_text_to_video(video_path, top_text, bottom_text, output_path)

        # Check if the video has an audio stream
        audio_file = 'temp_audio.aac'
        audio_check_command = f'ffprobe -i {video_path} -show_streams -select_streams a -loglevel error'
        audio_stream_exists = subprocess.run(audio_check_command, shell=True, stdout=subprocess.PIPE).stdout != b''

        if audio_stream_exists:
            try:
                # Extract audio from the original video
                extract_audio_command = f'ffmpeg -i {video_path} -q:a 0 -map a {audio_file}'
                subprocess.run(extract_audio_command, shell=True, check=True)

                # Combine the new video with the extracted audio
                temp_output_file = 'temp_output_with_audio.mp4'
                combine_command = f'ffmpeg -i {output_path} -i {audio_file} -c copy -map 0:v:0 -map 1:a:0 {temp_output_file}'
                subprocess.run(combine_command, shell=True, check=True)

                # Clean up and replace the final output
                if os.path.exists(output_path):
                    os.remove(output_path)
                os.rename(temp_output_file, output_path)

                # Remove the temporary audio file
                os.remove(audio_file)

                print("Video meme created successfully.")
                return utils.savenft(utils.VIDEOMEMEPATHOUT)

            except subprocess.CalledProcessError as e:
                print(f"FFmpeg error: {e}")

        else:
            print("No audio stream found in the video. Skipping audio extraction.")
            return utils.savenft(utils.VIDEOMEMEPATHOUT)



