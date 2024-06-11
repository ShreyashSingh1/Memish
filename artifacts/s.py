import cv2
import subprocess
import google.generativeai as genai


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

class VedioGenerator:
    def __init__(self, api_key, template_paths):
        self.template_paths = template_paths
        self.font = cv2.FONT_HERSHEY_SIMPLEX
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
                top_text = top_text.replace("**Top text:**", "").replace("**Top text**:", "").replace("**Top Text**:", "")

                bottom_text = response_text[2] if len(response_text) > 2 else ""
                bottom_text = bottom_text.replace("**Bottom text:**", "").replace("**Bottom text**:", "").replace("**Bottom Text**:", "")


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
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        out = None
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        wrapper = TextWrapper(self.font, 1, frame_width - 20)
        wrapped_top_text = wrapper.wrap_text(top_text)
        wrapped_bottom_text = wrapper.wrap_text(bottom_text)

        # Define shadow parameters
        shadow_offset = 2
        shadow_color = (0, 0, 0)  # Black shadow color

        for frame_num in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break
            if out is None:
                out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
            image_height, image_width, _ = frame.shape

            # Calculate positions for top text
            y_offset = 10
            for line in wrapped_top_text:
                text_size = cv2.getTextSize(line, self.font, 1, 1)[0]
                text_x = (image_width - text_size[0]) // 2
                text_y = y_offset + text_size[1]
                # Draw shadow first
                cv2.putText(frame, line, (text_x + shadow_offset, text_y + shadow_offset), self.font, 1, shadow_color, 2, lineType=cv2.LINE_AA)
                # Then draw text
                cv2.putText(frame, line, (text_x, text_y), self.font, 1, (255, 255, 255), 2, lineType=cv2.LINE_AA)
                y_offset += text_size[1] + 10

            # Calculate positions for bottom text
            y_offset = image_height - 10
            for line in reversed(wrapped_bottom_text):
                text_size = cv2.getTextSize(line, self.font, 1, 1)[0]
                text_x = (image_width - text_size[0]) // 2
                text_y = y_offset
                # Draw shadow first
                cv2.putText(frame, line, (text_x + shadow_offset, text_y - shadow_offset), self.font, 1, shadow_color, 2, lineType=cv2.LINE_AA)
                # Then draw text
                cv2.putText(frame, line, (text_x, text_y), self.font, 1, (255, 255, 255), 2, lineType=cv2.LINE_AA)
                y_offset -= text_size[1] + 10

            out.write(frame)

        cap.release()
        if out:
            out.release()

    def create_video_meme(self, prompt, output_path):
        template_path, top_text, bottom_text = self.analyze_prompt(prompt)
        self.add_text_to_video(template_path, top_text, bottom_text, output_path)
        
        # Use FFmpeg to mux the video with the audio
        video_file = output_path
        audio_file = 'audio.mp3'  # Replace with your audio file path
        output_file = 'output.mp4'  # Replace with your output file path

        ffmpeg_command = f'ffmpeg -i {video_file} -i {audio_file} -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 {output_file}'
        subprocess.run(ffmpeg_command, shell=True)