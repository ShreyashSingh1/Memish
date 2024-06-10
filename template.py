import google.generativeai as genai
import cv2
import numpy as np
import os

# Get the current working directory
current_directory = os.getcwd()

# Construct the template paths dynamically
template_paths = {
    "i_will_find_you_and_i_will_kill_you": os.path.join(current_directory, "Templates", "m1.jpg"),
    "its_a_surprise_tool_that_will_helps_us_later_mickey_mouse_clubhouse": os.path.join(current_directory, "Templates", "m2.jpg"),
    "default": os.path.join(current_directory, "Templates", "def.png"),
    "portrait_of_a_man_with_a_wide_genuine_smile_wearing_a_motorcycle_helmet_close_up_wearing_a_red_jacket": os.path.join(current_directory, "Templates", "m3.jpg"),
    "sad_man": os.path.join(current_directory, "Templates", "m4.jpg"),
    "waiting_skeleton": os.path.join(current_directory, "Templates", "m5.jpg")
}

# Function to interact with Gemini API
def analyze_prompt_with_gemini(prompt):
    data = f"Based on the prompt: '{prompt}', which meme template would be most suitable from the following options: {', '.join(template_paths.keys())}? Also, generate a suitable top and bottom text for the meme from your own don't just copy the user prompt, Make sure the answer you are giving the key name should be **meme_template** and funny as possible"

    genai.configure(api_key="AIzaSyBa5b8ZuK83ehPi52ua4Ly724ofJHTT5Zk")
    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(data)
    
    response_text = response.text.strip().split('\n')
    response_text = [item for item in response_text if item]

    template_choice = response_text[0].replace("**meme_template**:", "").strip().lower().replace(" ", "_")
    top_text = response_text[1] if len(response_text) > 1 else ""
    top_text = top_text.replace("**Top text**:", "").replace(" **Top text**: ","")
    bottom_text = response_text[2] if len(response_text) > 2 else ""
    bottom_text = bottom_text.replace("**Bottom text**:", "").replace(" **Bottom text**: ","").replace("**Top text**:", "")
    
    # Ensure template_choice matches our keys
    template_choice = template_choice.replace(":", "").replace(",", "").replace("-", "_").replace("'", "").replace(".", "").replace("`", "").replace("?", "").replace("!", "").replace("**meme_template**", "").strip()
    if template_choice.startswith('_'):
        template_choice = template_choice[1:]

    print(template_choice)
    # Safely get the template path
    template_path = template_paths.get(template_choice, template_paths[template_choice])
    template_path = template_path.replace("\\", "/")
    template_path = template_path.replace("/notebooks", "")
    
    return template_path, top_text, bottom_text

# Function to load the chosen meme template
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
    for line in wrapped_top_text:
        text_size = cv2.getTextSize(line, font, font_scale, 1)[0]
        text_x = (image_width - text_size[0]) // 2
        text_y = y_offset + text_size[1]
        cv2.putText(img, line, (text_x, text_y), font, font_scale, (255, 255, 255), 2, lineType=cv2.LINE_AA)
        y_offset += text_size[1] + 10

    # Calculate positions for bottom text
    y_offset = image_height - 10
    for line in reversed(wrapped_bottom_text):
        text_size = cv2.getTextSize(line, font, font_scale, 1)[0]
        text_x = (image_width - text_size[0]) // 2
        text_y = y_offset
        cv2.putText(img, line, (text_x, text_y), font, font_scale, (255, 255, 255), 2, lineType=cv2.LINE_AA)
        y_offset -= text_size[1] + 10
    
    return img

# Function to create a meme based on the user's prompt
def create_meme(prompt):
    template_path, top_text, bottom_text = analyze_prompt_with_gemini(prompt)
    img = load_meme_template(template_path)
    return add_text_to_image(img, top_text, bottom_text)

# Example usage
if __name__ == "__main__":
    prompt = "We got investment"
    try:
        meme = create_meme(prompt)
        cv2.imwrite("output_meme.jpg", meme)
        cv2.imshow("Meme", meme)
    except FileNotFoundError as e:
        print(e)