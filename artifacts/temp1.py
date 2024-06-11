import cv2
import google.generativeai as genai
import os

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

    def analyze_prompt(self, prompt):
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
        template_path = self.template_paths.get(template_choice, template_paths[template_choice])
        template_path = template_path.replace("\\", "/")
        template_path = template_path.replace("/notebooks", "")

        return template_path, top_text, bottom_text

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

        # Calculate positions for top text
        y_offset = 10
        for line in wrapped_top_text:
            text_size = cv2.getTextSize(line, font, 1, 1)[0]
            text_x = (image_width - text_size[0]) // 2
            text_y = y_offset + text_size[1]
            cv2.putText(img, line, (text_x, text_y), font, 1, (255, 255, 255), 2, lineType=cv2.LINE_AA)
            y_offset += text_size[1] + 10

        # Calculate positions for bottom text
        y_offset = image_height - 10
        for line in reversed(wrapped_bottom_text):
            text_size = cv2.getTextSize(line, font, 1, 1)[0]
            text_x = (image_width - text_size[0]) // 2
            text_y = y_offset
            cv2.putText(img, line, (text_x, text_y), font, 1, (255, 255, 255), 2, lineType=cv2.LINE_AA)
            y_offset -= text_size[1] + 10

        return img

    def create_meme(self, prompt):
        template_path, top_text, bottom_text = self.analyze_prompt(prompt)
        img = self.load_meme_template(template_path)
        return self.add_text_to_image(img, top_text, bottom_text)

# Example usage
if __name__ == "__main__":
    template_paths = {
    "aerial_view_of_a_car_driving_down_a_road_in_the_middle_of_a_forest_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/aerial_view_of_a_car_driving_down_a_road_in_the_middle_of_a_forest_1.jpg",
    "anime_boy_with_black_hair_and_a_black_jacket_looking_up_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/anime_boy_with_black_hair_and_a_black_jacket_looking_up_1.jpg",
    "anime_girl_with_long_hair_and_red_eyes_with_a_black_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/anime_girl_with_long_hair_and_red_eyes_with_a_black_background_1.jpg",
    "an_iceberg_floating_in_the_ocean_with_a_blue_sky_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/an_iceberg_floating_in_the_ocean_with_a_blue_sky_1.jpg",
    "arafed_girl_in_a_pink_bikini_standing_on_the_beach_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_girl_in_a_pink_bikini_standing_on_the_beach_1.jpg",
    "arafed_girl_in_a_yellow_bikini_standing_in_front_of_a_pool_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_girl_in_a_yellow_bikini_standing_in_front_of_a_pool_1.jpg",
    "arafed_image_of_a_couple_in_a_car_with_a_woman_in_the_back_seat_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_image_of_a_couple_in_a_car_with_a_woman_in_the_back_seat_1.jpg",
    "arafed_image_of_a_man_in_a_red_jacket_talking_on_a_cell_phone_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_image_of_a_man_in_a_red_jacket_talking_on_a_cell_phone_1.jpg",
    "arafed_image_of_a_man_in_a_red_jacket_talking_on_a_cell_phone_2": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_image_of_a_man_in_a_red_jacket_talking_on_a_cell_phone_2.jpg",
    "arafed_image_of_a_man_in_a_red_jacket_talking_on_a_cell_phone_3": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_image_of_a_man_in_a_red_jacket_talking_on_a_cell_phone_3.jpg",
    "arafed_image_of_a_man_in_a_suit_and_tie_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_image_of_a_man_in_a_suit_and_tie_1.jpg",
    "arafed_image_of_a_man_in_a_suit_and_tie_in_the_dark_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_image_of_a_man_in_a_suit_and_tie_in_the_dark_1.jpg",
    "arafed_image_of_a_man_in_a_suit_and_two_other_men_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_image_of_a_man_in_a_suit_and_two_other_men_1.jpg",
    "arafed_image_of_a_man_in_a_tuxedo_and_bow_tie_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_image_of_a_man_in_a_tuxedo_and_bow_tie_1.jpg",
    "arafed_image_of_a_man_sitting_on_a_swing_with_a_woman_standing_in_the_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_image_of_a_man_sitting_on_a_swing_with_a_woman_standing_in_the_background_1.jpg",
    "arafed_image_of_a_man_standing_in_a_yard_next_to_a_woman_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_image_of_a_man_standing_in_a_yard_next_to_a_woman_1.jpg",
    "arafed_image_of_a_man_with_a_black_shirt_and_a_black_shirt_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_image_of_a_man_with_a_black_shirt_and_a_black_shirt_1.jpg",
    "arafed_man_and_two_women_hugging_each_other_in_a_bathroom_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_and_two_women_hugging_each_other_in_a_bathroom_1.jpg",
    "arafed_man_and_woman_hugging_each_other_in_a_black_and_white_photo_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_and_woman_hugging_each_other_in_a_black_and_white_photo_1.jpg",
    "arafed_man_holding_a_wallet_and_a_wallet_with_a_wallet_in_it_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_holding_a_wallet_and_a_wallet_with_a_wallet_in_it_1.jpg",
    "arafed_man_in_a_black_and_white_shirt_sitting_in_front_of_a_motorcycle_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_black_and_white_shirt_sitting_in_front_of_a_motorcycle_1.jpg",
    "arafed_man_in_a_black_shirt_and_tie_smiling_in_a_bathroom_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_black_shirt_and_tie_smiling_in_a_bathroom_1.jpg",
    "arafed_man_in_a_red_shirt_is_playing_a_video_game_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_red_shirt_is_playing_a_video_game_1.jpg",
    "arafed_man_in_a_suit_and_tie_holding_a_hat_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_suit_and_tie_holding_a_hat_1.jpg",
    "arafed_man_in_a_suit_and_tie_holding_his_head_in_his_hand_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_suit_and_tie_holding_his_head_in_his_hand_1.jpg",
    "arafed_man_in_a_suit_and_tie_is_stretching_his_arms_out_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_suit_and_tie_is_stretching_his_arms_out_1.jpg",
    "arafed_man_in_a_suit_and_tie_sitting_in_a_chair_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_suit_and_tie_sitting_in_a_chair_1.jpg",
    "arafed_man_in_a_suit_and_tie_standing_in_front_of_a_bulletin_board_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_suit_and_tie_standing_in_front_of_a_bulletin_board_1.jpg",
    "arafed_man_in_a_suit_and_tie_standing_in_front_of_a_window_with_numbers_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_suit_and_tie_standing_in_front_of_a_window_with_numbers_1.jpg",
    "arafed_man_in_a_suit_and_tie_standing_on_the_beach_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_suit_and_tie_standing_on_the_beach_1.jpg",
    "arafed_man_in_a_suit_kneeling_next_to_a_grave_with_a_sign_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_suit_kneeling_next_to_a_grave_with_a_sign_1.jpg",
    "arafed_man_in_a_tie_smoking_a_cigarette_in_an_office_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_tie_smoking_a_cigarette_in_an_office_1.jpg",
    "arafed_man_in_a_tie_talking_on_a_cell_phone_in_an_office_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_tie_talking_on_a_cell_phone_in_an_office_1.jpg",
    "arafed_man_in_a_yellow_jacket_leaning_against_a_tree_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_a_yellow_jacket_leaning_against_a_tree_1.jpg",
    "arafed_man_in_red_shirt_sitting_in_chair_with_his_hands_on_his_face_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_red_shirt_sitting_in_chair_with_his_hands_on_his_face_1.jpg",
    "arafed_man_in_red_shirt_standing_on_a_road_with_a_name_tag_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_red_shirt_standing_on_a_road_with_a_name_tag_1.jpg",
    "arafed_man_in_white_shirt_and_khaki_pants_holding_a_belt_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_white_shirt_and_khaki_pants_holding_a_belt_1.jpg",
    "arafed_man_in_yellow_jacket_leaning_against_a_tree_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_in_yellow_jacket_leaning_against_a_tree_1.jpg",
    "arafed_man_pointing_at_a_can_of_soda_with_a_cigarette_in_his_hand_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_pointing_at_a_can_of_soda_with_a_cigarette_in_his_hand_1.jpg",
    "arafed_man_pointing_at_something_with_his_right_hand_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_pointing_at_something_with_his_right_hand_1.jpg",
    "arafed_man_sitting_at_a_table_with_a_sign_on_it_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_sitting_at_a_table_with_a_sign_on_it_1.jpg",
    "arafed_man_sitting_on_a_bench_talking_on_a_cell_phone_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_sitting_on_a_bench_talking_on_a_cell_phone_1.jpg",
    "arafed_man_sitting_on_a_chair_talking_to_a_man_with_a_bloody_face_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_sitting_on_a_chair_talking_to_a_man_with_a_bloody_face_1.jpg",
    "arafed_man_sitting_on_a_red_chair_with_his_hands_up_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_sitting_on_a_red_chair_with_his_hands_up_1.jpg",
    "arafed_man_talking_on_a_cell_phone_while_holding_a_microphone_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_talking_on_a_cell_phone_while_holding_a_microphone_1.jpg",
    "arafed_man_with_arms_raised_in_the_air_in_front_of_a_sunset_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_with_arms_raised_in_the_air_in_front_of_a_sunset_1.jpg",
    "arafed_man_with_a_beard_and_a_smile_on_his_face_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_with_a_beard_and_a_smile_on_his_face_1.jpg",
    "arafed_man_with_a_beard_and_a_white_beard_holding_his_hands_up_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_with_a_beard_and_a_white_beard_holding_his_hands_up_1.jpg",
    "arafed_man_with_a_beard_and_a_white_beard_holding_his_hands_up_2": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_with_a_beard_and_a_white_beard_holding_his_hands_up_2.jpg",
    "arafed_man_with_a_black_shirt_and_a_black_sweater_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_with_a_black_shirt_and_a_black_sweater_1.jpg",
    "arafed_man_with_a_black_shirt_and_a_black_sweater_2": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_with_a_black_shirt_and_a_black_sweater_2.jpg",
    "arafed_man_with_a_pink_mohawk_and_a_unicorn_tail_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_with_a_pink_mohawk_and_a_unicorn_tail_1.jpg",
    "arafed_man_with_a_shaved_head_and_a_shaved_face_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_with_a_shaved_head_and_a_shaved_face_1.jpg",
    "arafed_man_with_a_shirtless_face_and_a_shirtless_torso_laughing_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_with_a_shirtless_face_and_a_shirtless_torso_laughing_1.jpg",
    "arafed_man_with_glasses_and_no_shirt_brushing_his_teeth_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_man_with_glasses_and_no_shirt_brushing_his_teeth_1.jpg",
    "arafed_scene_of_a_star_wars_scene_with_a_man_and_a_woman_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_scene_of_a_star_wars_scene_with_a_man_and_a_woman_1.jpg",
    "arafed_skeleton_sitting_on_a_chair_in_the_ocean_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_skeleton_sitting_on_a_chair_in_the_ocean_1.jpg",
    "arafed_wolf_with_a_large_grin_on_its_face_in_front_of_a_building_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_wolf_with_a_large_grin_on_its_face_in_front_of_a_building_1.jpg",
    "arafed_woman_holding_a_balloon_and_a_happy_birthday_sign_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_woman_holding_a_balloon_and_a_happy_birthday_sign_1.jpg",
    "arafed_woman_in_a_black_and_white_photo_with_a_man_in_a_suit_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_woman_in_a_black_and_white_photo_with_a_man_in_a_suit_1.jpg",
    "arafed_woman_in_red_top_and_jeans_is_being_fucked_by_a_group_of_black_men_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_woman_in_red_top_and_jeans_is_being_fucked_by_a_group_of_black_men_1.jpg",
    "arafed_woman_with_a_beard_and_a_man_with_a_beard_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_woman_with_a_beard_and_a_man_with_a_beard_1.jpg",
    "arafed_woman_with_a_black_shirt_and_a_black_shirt_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_woman_with_a_black_shirt_and_a_black_shirt_1.jpg",
    "arafed_woman_with_blindfold_kissing_a_man_with_a_blindfold_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_woman_with_blindfold_kissing_a_man_with_a_blindfold_1.jpg",
    "arafed_woman_with_glasses_and_a_black_top_holding_a_cell_phone_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_woman_with_glasses_and_a_black_top_holding_a_cell_phone_1.jpg",
    "arafed_woman_yelling_in_car_with_child_in_backseat_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/arafed_woman_yelling_in_car_with_child_in_backseat_1.jpg",
    "araffes_in_a_black_lingerie_is_sitting_on_a_blanket_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/araffes_in_a_black_lingerie_is_sitting_on_a_blanket_1.jpg",
    "araffes_in_a_futuristic_space_station_with_a_giant_window_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/araffes_in_a_futuristic_space_station_with_a_giant_window_1.jpg",
    "araffes_of_a_man_standing_in_front_of_a_fountain_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/araffes_of_a_man_standing_in_front_of_a_fountain_1.jpg",
    "araffe_cat_sitting_at_a_table_with_a_cupcake_and_a_candle_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/araffe_cat_sitting_at_a_table_with_a_cupcake_and_a_candle_1.jpg",
    "araffe_dog_sitting_in_a_car_with_a_pink_collar_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/araffe_dog_sitting_in_a_car_with_a_pink_collar_1.jpg",
    "araffe_dressed_as_a_man_holding_a_glass_of_wine_and_baguet_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/araffe_dressed_as_a_man_holding_a_glass_of_wine_and_baguet_1.jpg",
    "araffe_man_in_a_white_shirt_is_bending_over_to_look_at_a_toilet_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/araffe_man_in_a_white_shirt_is_bending_over_to_look_at_a_toilet_1.jpg",
    "araffe_with_a_very_large_belly_sitting_on_a_blanket_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/araffe_with_a_very_large_belly_sitting_on_a_blanket_1.jpg",
    "araffe_woman_in_a_red_costume_smoking_a_hook_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/araffe_woman_in_a_red_costume_smoking_a_hook_1.jpg",
    "araffe_woman_in_white_underwear_and_red_stockings_sitting_on_the_ground_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/araffe_woman_in_white_underwear_and_red_stockings_sitting_on_the_ground_1.jpg",
    "a_3d_man_holding_a_sign_in_the_air_with_his_hands_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_3d_man_holding_a_sign_in_the_air_with_his_hands_1.jpg",
    "a_black_and_white_drawing_of_a_smiling_face_with_sunglasses_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_black_and_white_drawing_of_a_smiling_face_with_sunglasses_1.jpg",
    "a_black_and_white_image_of_a_cross_with_a_chain_on_it_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_black_and_white_image_of_a_cross_with_a_chain_on_it_1.jpg",
    "a_black_and_white_image_of_a_face_with_a_frown_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_black_and_white_image_of_a_face_with_a_frown_1.jpg",
    "a_black_and_white_map_of_the_uk_with_dots_on_it_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_black_and_white_map_of_the_uk_with_dots_on_it_1.jpg",
    "a_black_and_white_photo_of_a_man_with_a_beard_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_black_and_white_photo_of_a_man_with_a_beard_1.jpg",
    "a_black_and_white_photo_of_a_man_with_a_hand_on_his_chin_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_black_and_white_photo_of_a_man_with_a_hand_on_his_chin_1.jpg",
    "a_black_and_white_photo_of_a_tank_in_a_desert_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_black_and_white_photo_of_a_tank_in_a_desert_1.jpg",
    "a_black_and_white_sign_with_a_green_arrow_and_a_green_arrow_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_black_and_white_sign_with_a_green_arrow_and_a_green_arrow_1.jpg",
    "a_black_and_white_spiral_design_with_a_black_and_white_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_black_and_white_spiral_design_with_a_black_and_white_background_1.jpg",
    "a_black_and_white_striped_rug_with_a_white_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_black_and_white_striped_rug_with_a_white_background_1.jpg",
    "a_cartoon_image_of_a_man_in_a_hoodie_with_a_mask_on_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_cartoon_image_of_a_man_in_a_hoodie_with_a_mask_on_1.jpg",
    "a_cartoon_image_of_a_red_and_blue_smiley_face_with_a_hammer_and_sick_face_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_cartoon_image_of_a_red_and_blue_smiley_face_with_a_hammer_and_sick_face_1.jpg",
    "a_cartoon_of_a_man_and_a_dog_talking_to_each_other_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_cartoon_of_a_man_and_a_dog_talking_to_each_other_1.jpg",
    "a_cartoon_of_a_man_and_a_woman_with_a_curve_of_a_graph_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_cartoon_of_a_man_and_a_woman_with_a_curve_of_a_graph_1.jpg",
    "a_cartoon_of_a_man_holding_a_balloon_and_a_woman_reaching_for_it_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_cartoon_of_a_man_holding_a_balloon_and_a_woman_reaching_for_it_1.jpg",
    "a_cartoon_of_a_man_with_a_red_button_on_his_forehead_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_cartoon_of_a_man_with_a_red_button_on_his_forehead_1.jpg",
    "a_cartoon_of_a_person_laying_in_bed_with_a_speech_bubble_above_them_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_cartoon_of_a_person_laying_in_bed_with_a_speech_bubble_above_them_1.jpg",
    "a_cartoon_of_a_polar_bear_with_a_blue_hat_on_its_head_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_cartoon_of_a_polar_bear_with_a_blue_hat_on_its_head_1.jpg",
    "a_cartoon_of_two_men_with_beards_and_glasses_on_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_cartoon_of_two_men_with_beards_and_glasses_on_1.jpg",
    "a_cartoon_picture_of_a_man_kicking_a_door_with_a_gun_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_cartoon_picture_of_a_man_kicking_a_door_with_a_gun_1.jpg",
    "a_certificate_with_a_blue_border_and_a_gold_seal_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_certificate_with_a_blue_border_and_a_gold_seal_1.jpg",
    "a_close_up_of_a_baby_bib_with_a_bunny_on_it_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_baby_bib_with_a_bunny_on_it_1.jpg",
    "a_close_up_of_a_baby_with_a_very_big_smile_on_his_face_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_baby_with_a_very_big_smile_on_his_face_1.jpg",
    "a_close_up_of_a_black_and_white_drawing_of_a_face_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_black_and_white_drawing_of_a_face_1.jpg",
    "a_close_up_of_a_black_and_white_picture_of_a_cat_wearing_a_vest_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_black_and_white_picture_of_a_cat_wearing_a_vest_1.jpg",
    "a_close_up_of_a_black_and_white_picture_of_a_person_with_a_sword_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_black_and_white_picture_of_a_person_with_a_sword_1.jpg",
    "a_close_up_of_a_black_ink_splatter_on_a_white_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_black_ink_splatter_on_a_white_background_1.jpg",
    "a_close_up_of_a_blue_and_black_logo_with_a_light_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_blue_and_black_logo_with_a_light_1.jpg",
    "a_close_up_of_a_bouquet_of_red_roses_on_a_white_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_bouquet_of_red_roses_on_a_white_background_1.jpg",
    "a_close_up_of_a_cartoon_character_with_a_big_smile_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_cartoon_character_with_a_big_smile_1.jpg",
    "a_close_up_of_a_cartoon_character_with_a_big_smile_on_his_face_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_cartoon_character_with_a_big_smile_on_his_face_1.jpg",
    "a_close_up_of_a_cartoon_character_with_a_mustache_on_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_cartoon_character_with_a_mustache_on_1.jpg",
    "a_close_up_of_a_cartoon_character_with_a_tie_and_a_tie_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_cartoon_character_with_a_tie_and_a_tie_1.jpg",
    "a_close_up_of_a_cartoon_lion_sitting_on_a_rock_with_a_sunset_in_the_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_cartoon_lion_sitting_on_a_rock_with_a_sunset_in_the_background_1.jpg",
    "a_close_up_of_a_cartoon_of_a_man_in_a_top_hat_and_a_woman_in_a_cape_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_cartoon_of_a_man_in_a_top_hat_and_a_woman_in_a_cape_1.jpg",
    "a_close_up_of_a_cartoon_of_a_person_laying_in_bed_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_cartoon_of_a_person_laying_in_bed_1.jpg",
    "a_close_up_of_a_cartoon_pikachu_with_a_tree_in_the_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_cartoon_pikachu_with_a_tree_in_the_background_1.jpg",
    "a_close_up_of_a_cat_with_its_mouth_open_and_its_paws_up_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_cat_with_its_mouth_open_and_its_paws_up_1.jpg",
    "a_close_up_of_a_chicken_in_a_game_with_a_keyboard_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_chicken_in_a_game_with_a_keyboard_1.jpg",
    "a_close_up_of_a_creepy_face_with_red_eyes_and_a_tooth_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_creepy_face_with_red_eyes_and_a_tooth_1.jpg",
    "a_close_up_of_a_face_with_a_black_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_face_with_a_black_background_1.jpg",
    "a_close_up_of_a_face_with_a_galaxy_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_face_with_a_galaxy_background_1.jpg",
    "a_close_up_of_a_frog_with_a_flower_on_its_head_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_frog_with_a_flower_on_its_head_1.jpg",
    "a_close_up_of_a_green_alien_head_with_horns_and_a_halo_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_green_alien_head_with_horns_and_a_halo_1.jpg",
    "a_close_up_of_a_group_of_men_standing_on_a_sidewalk_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_group_of_men_standing_on_a_sidewalk_1.jpg",
    "a_close_up_of_a_man_flexing_his_arm_with_another_man_in_the_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_flexing_his_arm_with_another_man_in_the_background_1.jpg",
    "a_close_up_of_a_man_hugging_a_chimpan_in_a_forest_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_hugging_a_chimpan_in_a_forest_1.jpg",
    "a_close_up_of_a_man_in_a_black_shirt_and_tie_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_in_a_black_shirt_and_tie_1.jpg",
    "a_close_up_of_a_man_in_a_red_jacket_making_a_peace_sign_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_in_a_red_jacket_making_a_peace_sign_1.jpg",
    "a_close_up_of_a_man_in_a_tuxedo_smoking_a_cigarette_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_in_a_tuxedo_smoking_a_cigarette_1.jpg",
    "a_close_up_of_a_man_in_a_white_underwear_posing_for_a_picture_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_in_a_white_underwear_posing_for_a_picture_1.jpg",
    "a_close_up_of_a_man_in_a_wrestling_ring_with_a_referee_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_in_a_wrestling_ring_with_a_referee_1.jpg",
    "a_close_up_of_a_man_laughing_and_wearing_a_suit_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_laughing_and_wearing_a_suit_1.jpg",
    "a_close_up_of_a_man_with_a_beard_and_a_smile_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_with_a_beard_and_a_smile_1.jpg",
    "a_close_up_of_a_man_with_a_beard_and_a_tie_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_with_a_beard_and_a_tie_1.jpg",
    "a_close_up_of_a_man_with_a_long_beard_and_a_helmet_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_with_a_long_beard_and_a_helmet_1.jpg",
    "a_close_up_of_a_man_with_a_smile_on_his_face_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_with_a_smile_on_his_face_1.jpg",
    "a_close_up_of_a_man_with_a_tattoo_on_his_chest_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_with_a_tattoo_on_his_chest_1.jpg",
    "a_close_up_of_a_man_with_boxing_gloves_on_posing_for_a_picture_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_man_with_boxing_gloves_on_posing_for_a_picture_1.jpg",
    "a_close_up_of_a_person's_face_with_different_parts_of_the_body_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person's_face_with_different_parts_of_the_body_1.jpg",
    "a_close_up_of_a_person's_hand_with_a_finger_up_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person's_hand_with_a_finger_up_1.jpg",
    "a_close_up_of_a_person_holding_a_bloody_heart_in_their_hand_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_holding_a_bloody_heart_in_their_hand_1.jpg",
    "a_close_up_of_a_person_holding_a_gun_in_front_of_a_cartoon_character_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_holding_a_gun_in_front_of_a_cartoon_character_1.jpg",
    "a_close_up_of_a_person_holding_a_tennis_racket_on_a_black_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_holding_a_tennis_racket_on_a_black_background_1.jpg",
    "a_close_up_of_a_person_holding_two_guns_in_their_hands_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_holding_two_guns_in_their_hands_1.jpg",
    "a_close_up_of_a_person_in_a_red_jacket_with_a_cell_phone_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_in_a_red_jacket_with_a_cell_phone_1.jpg",
    "a_close_up_of_a_person_in_a_suit_with_a_head_on_a_stock_market_chart_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_in_a_suit_with_a_head_on_a_stock_market_chart_1.jpg",
    "a_close_up_of_a_person_kissing_a_small_child_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_kissing_a_small_child_1.jpg",
    "a_close_up_of_a_person_sitting_on_a_bench_with_a_child_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_sitting_on_a_bench_with_a_child_1.jpg",
    "a_close_up_of_a_person_standing_in_front_of_a_red_sign_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_standing_in_front_of_a_red_sign_1.jpg",
    "a_close_up_of_a_person_wearing_a_black_shirt_with_a_cross_on_it_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_wearing_a_black_shirt_with_a_cross_on_it_1.jpg",
    "a_close_up_of_a_person_wearing_a_jacket_and_pants_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_wearing_a_jacket_and_pants_1.jpg",
    "a_close_up_of_a_person_with_a_cell_phone_in_their_hand_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_with_a_cell_phone_in_their_hand_1.jpg",
    "a_close_up_of_a_person_with_a_knife_in_their_hand_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_with_a_knife_in_their_hand_1.jpg",
    "a_close_up_of_a_person_with_a_red_ball_in_their_mouth_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_with_a_red_ball_in_their_mouth_1.jpg",
    "a_close_up_of_a_person_with_a_tie_and_a_jacket_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_with_a_tie_and_a_jacket_1.jpg",
    "a_close_up_of_a_person_with_a_weird_face_and_a_weird_nose_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_with_a_weird_face_and_a_weird_nose_1.jpg",
    "a_close_up_of_a_person_with_clown_makeup_and_clown_makeup_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_with_clown_makeup_and_clown_makeup_1.jpg",
    "a_close_up_of_a_person_with_glasses_on_staring_at_something_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_with_glasses_on_staring_at_something_1.jpg",
    "a_close_up_of_a_person_with_long_hair_and_a_wet_face_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_person_with_long_hair_and_a_wet_face_1.jpg",
    "a_close_up_of_a_red_and_black_background_with_a_red_light_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_red_and_black_background_with_a_red_light_1.jpg",
    "a_close_up_of_a_scary_face_with_a_big_mouth_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_scary_face_with_a_big_mouth_1.jpg",
    "a_close_up_of_a_shark_with_its_mouth_open_and_a_man_swimming_in_the_water_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_shark_with_its_mouth_open_and_a_man_swimming_in_the_water_1.jpg",
    "a_close_up_of_a_skeleton_sitting_on_a_bench_with_a_grass_field_in_the_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_skeleton_sitting_on_a_bench_with_a_grass_field_in_the_background_1.jpg",
    "a_close_up_of_a_skeleton_sitting_on_a_chair_with_a_laptop_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_skeleton_sitting_on_a_chair_with_a_laptop_1.jpg",
    "a_close_up_of_a_small_doll_holding_a_cell_phone_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_small_doll_holding_a_cell_phone_1.jpg",
    "a_close_up_of_a_smiley_face_on_a_yellow_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_smiley_face_on_a_yellow_background_1.jpg",
    "a_close_up_of_a_smiley_face_with_thumbs_up_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_smiley_face_with_thumbs_up_1.jpg",
    "a_close_up_of_a_smiley_face_with_two_crossed_eyes_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_smiley_face_with_two_crossed_eyes_1.jpg",
    "a_close_up_of_a_square_object_on_a_black_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_square_object_on_a_black_background_1.jpg",
    "a_close_up_of_a_square_object_on_a_black_background_2": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_square_object_on_a_black_background_2.jpg",
    "a_close_up_of_a_square_object_with_a_square_in_the_middle_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_square_object_with_a_square_in_the_middle_1.jpg",
    "a_close_up_of_a_statue_of_a_person_holding_a_small_object_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_statue_of_a_person_holding_a_small_object_1.jpg",
    "a_close_up_of_a_street_sign_with_a_person_walking_on_it_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_street_sign_with_a_person_walking_on_it_1.jpg",
    "a_close_up_of_a_toy_man_with_a_hat_on_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_toy_man_with_a_hat_on_1.jpg",
    "a_close_up_of_a_toy_of_a_boy_wearing_a_hat_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_toy_of_a_boy_wearing_a_hat_1.jpg",
    "a_close_up_of_a_vase_with_a_bunch_of_red_roses_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_vase_with_a_bunch_of_red_roses_1.jpg",
    "a_close_up_of_a_white_square_frame_with_a_black_border_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_white_square_frame_with_a_black_border_1.jpg",
    "a_close_up_of_a_woman_in_a_black_bra_top_posing_for_a_picture_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_woman_in_a_black_bra_top_posing_for_a_picture_1.jpg",
    "a_close_up_of_a_woman_wearing_a_black_jacket_and_a_white_shirt_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_woman_wearing_a_black_jacket_and_a_white_shirt_1.jpg",
    "a_close_up_of_a_woman_wearing_glasses_and_a_black_tank_top_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_a_woman_wearing_glasses_and_a_black_tank_top_1.jpg",
    "a_close_up_of_two_men_in_hats_on_a_boat_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_two_men_in_hats_on_a_boat_1.jpg",
    "a_close_up_of_two_pictures_of_a_monkey_with_a_green_shirt_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_close_up_of_two_pictures_of_a_monkey_with_a_green_shirt_1.jpg",
    "a_couple_of_people_standing_next_to_each_other_in_a_dark_room_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_couple_of_people_standing_next_to_each_other_in_a_dark_room_1.jpg",
    "a_couple_of_people_that_are_kissing_each_other_in_a_room_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_couple_of_people_that_are_kissing_each_other_in_a_room_1.jpg",
    "a_couple_of_pictures_of_a_lion_and_a_lion_cub_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_couple_of_pictures_of_a_lion_and_a_lion_cub_1.jpg",
    "a_couple_of_pictures_of_a_man_driving_a_car_with_another_man_in_the_back_seat_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_couple_of_pictures_of_a_man_driving_a_car_with_another_man_in_the_back_seat_1.jpg",
    "a_cross_stitch_pattern_of_a_woman_with_glasses_and_a_hat_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_cross_stitch_pattern_of_a_woman_with_glasses_and_a_hat_1.jpg",
    "a_drawing_of_a_man_with_a_red_eye_and_a_white_shirt_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_drawing_of_a_man_with_a_red_eye_and_a_white_shirt_1.jpg",
    "a_drawing_of_a_person_sitting_in_a_chair_with_a_bird_in_their_hand_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_drawing_of_a_person_sitting_in_a_chair_with_a_bird_in_their_hand_1.jpg",
    "a_drawing_of_a_woman_with_a_sad_face_and_a_tooth_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_drawing_of_a_woman_with_a_sad_face_and_a_tooth_1.jpg",
    "a_drawing_of_two_men_shaking_hands_with_one_another_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_drawing_of_two_men_shaking_hands_with_one_another_1.jpg",
    "a_group_of_banners_with_a_man_on_a_mountain_top_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_group_of_banners_with_a_man_on_a_mountain_top_1.jpg",
    "a_group_of_cartoon_characters_sitting_on_top_of_a_bed_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_group_of_cartoon_characters_sitting_on_top_of_a_bed_1.jpg",
    "a_group_of_men_in_leather_jackets_and_hats_standing_in_a_bar_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_group_of_men_in_leather_jackets_and_hats_standing_in_a_bar_1.jpg",
    "a_man's_torso_with_a_large_amount_of_muscles_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_man's_torso_with_a_large_amount_of_muscles_1.jpg",
    "a_man_and_woman_standing_next_to_each_other_in_a_room_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_man_and_woman_standing_next_to_each_other_in_a_room_1.jpg",
    "a_man_in_a_black_shirt_holding_a_knife_in_front_of_a_window_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_man_in_a_black_shirt_holding_a_knife_in_front_of_a_window_1.jpg",
    "a_man_in_a_hoodie_is_crying_in_front_of_a_crowd_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_man_in_a_hoodie_is_crying_in_front_of_a_crowd_1.jpg",
    "a_man_in_a_leather_jacket_and_sunglasses_standing_in_front_of_a_building_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_man_in_a_leather_jacket_and_sunglasses_standing_in_front_of_a_building_1.jpg",
    "a_man_in_a_suit_and_tie_is_holding_a_gun_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_man_in_a_suit_and_tie_is_holding_a_gun_1.jpg",
    "a_man_with_a_beard_and_hat_logo_for_sale_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_man_with_a_beard_and_hat_logo_for_sale_1.jpg",
    "a_man_with_long_hair_and_a_beard_in_a_cave_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_man_with_long_hair_and_a_beard_in_a_cave_1.jpg",
    "a_man_with_long_hair_and_a_beard_standing_next_to_another_man_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_man_with_long_hair_and_a_beard_standing_next_to_another_man_1.jpg",
    "a_man_with_long_hair_holding_two_swords_in_his_hands_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_man_with_long_hair_holding_two_swords_in_his_hands_1.jpg",
    "a_man_with_tattoos_and_a_face_mask_on_his_chest_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_man_with_tattoos_and_a_face_mask_on_his_chest_1.jpg",
    "a_painting_of_jesus_and_demon_hands_in_front_of_a_man_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_painting_of_jesus_and_demon_hands_in_front_of_a_man_1.jpg",
    "a_picture_of_a_baby_in_a_green_shirt_is_holding_a_fist_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_picture_of_a_baby_in_a_green_shirt_is_holding_a_fist_1.jpg",
    "a_picture_of_a_picture_of_a_square_with_a_face_on_it_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_picture_of_a_picture_of_a_square_with_a_face_on_it_1.jpg",
    "a_picture_taken_from_a_picture_of_a_potato_in_a_head_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_picture_taken_from_a_picture_of_a_potato_in_a_head_1.jpg",
    "a_poster_of_a_movie_with_a_bunch_of_different_titles_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_poster_of_a_movie_with_a_bunch_of_different_titles_1.jpg",
    "a_poster_of_a_nun_with_a_cross_and_a_chain_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_poster_of_a_nun_with_a_cross_and_a_chain_1.jpg",
    "a_purple_background_with_a_grungy_stripe_in_the_middle_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_purple_background_with_a_grungy_stripe_in_the_middle_1.jpg",
    "a_red_and_black_image_of_a_scary_mask_with_a_big_smile_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_red_and_black_image_of_a_scary_mask_with_a_big_smile_1.jpg",
    "a_screenshot_of_a_minecraft_village_with_a_mountain_in_the_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_screenshot_of_a_minecraft_village_with_a_mountain_in_the_background_1.jpg",
    "a_silhouette_of_a_person_in_a_hoodie_holding_a_knife_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_silhouette_of_a_person_in_a_hoodie_holding_a_knife_1.jpg",
    "a_woman_in_a_black_leather_outfit_is_being_fucked_by_a_man_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_woman_in_a_black_leather_outfit_is_being_fucked_by_a_man_1.jpg",
    "a_woman_in_a_black_top_and_black_pants_with_a_necklace_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_woman_in_a_black_top_and_black_pants_with_a_necklace_1.jpg",
    "a_woman_in_a_panties_is_holding_a_piece_of_tape_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_woman_in_a_panties_is_holding_a_piece_of_tape_1.jpg",
    "a_woman_with_a_veil_on_her_head_and_a_man_in_a_suit_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_woman_with_a_veil_on_her_head_and_a_man_in_a_suit_1.jpg",
    "a_yellow_ticket_with_a_picture_of_a_world_pass_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/a_yellow_ticket_with_a_picture_of_a_world_pass_1.jpg",
    "blond_girl_sitting_on_a_couch_with_a_group_of_men_in_white_shirts_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/blond_girl_sitting_on_a_couch_with_a_group_of_men_in_white_shirts_1.jpg",
    "blond_woman_with_blue_eyes_and_blue_eyes_laying_on_a_bed_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/blond_woman_with_blue_eyes_and_blue_eyes_laying_on_a_bed_1.jpg",
    "boy_in_white_shirt_sitting_on_a_couch_with_a_remote_control_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/boy_in_white_shirt_sitting_on_a_couch_with_a_remote_control_1.jpg",
    "boy_with_headphones_on_laughing_and_holding_a_skateboard_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/boy_with_headphones_on_laughing_and_holding_a_skateboard_1.jpg",
    "cartoon_cat_sitting_on_a_chair_with_a_telephone_and_a_desk_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_cat_sitting_on_a_chair_with_a_telephone_and_a_desk_1.jpg",
    "cartoon_dog_sitting_in_a_chair_in_front_of_a_fire_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_dog_sitting_in_a_chair_in_front_of_a_fire_1.jpg",
    "cartoon_drawing_of_a_group_of_people_with_faces_and_a_dog_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_drawing_of_a_group_of_people_with_faces_and_a_dog_1.jpg",
    "cartoon_image_of_a_yellow_and_blue_monster_with_a_cigarette_in_its_mouth_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_image_of_a_yellow_and_blue_monster_with_a_cigarette_in_its_mouth_1.jpg",
    "cartoon_of_a_cat_riding_a_bike_with_a_big_smile_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_cat_riding_a_bike_with_a_big_smile_1.jpg",
    "cartoon_of_a_man_and_a_woman_sitting_on_a_couch_with_a_baby_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_man_and_a_woman_sitting_on_a_couch_with_a_baby_1.jpg",
    "cartoon_of_a_man_holding_a_shovel_in_front_of_a_grave_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_man_holding_a_shovel_in_front_of_a_grave_1.jpg",
    "cartoon_of_a_man_in_a_white_shirt_and_a_group_of_people_in_different_colors_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_man_in_a_white_shirt_and_a_group_of_people_in_different_colors_1.jpg",
    "cartoon_of_a_man_sitting_in_front_of_a_computer_with_a_broken_screen_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_man_sitting_in_front_of_a_computer_with_a_broken_screen_1.jpg",
    "cartoon_of_a_man_sitting_in_front_of_a_computer_with_a_broken_screen_2": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_man_sitting_in_front_of_a_computer_with_a_broken_screen_2.jpg",
    "cartoon_of_a_man_sitting_on_a_couch_with_a_cup_of_coffee_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_man_sitting_on_a_couch_with_a_cup_of_coffee_1.jpg",
    "cartoon_of_a_man_sleeping_in_bed_with_a_woman_sleeping_in_the_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_man_sleeping_in_bed_with_a_woman_sleeping_in_the_background_1.jpg",
    "cartoon_of_a_man_standing_in_front_of_a_crowd_of_people_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_man_standing_in_front_of_a_crowd_of_people_1.jpg",
    "cartoon_of_a_man_with_a_beard_and_a_beardless_face_using_a_laptop_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_man_with_a_beard_and_a_beardless_face_using_a_laptop_1.jpg",
    "cartoon_of_a_man_with_a_hat_and_a_tie_on_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_man_with_a_hat_and_a_tie_on_1.jpg",
    "cartoon_of_a_person_laying_on_a_puddle_of_water_with_a_head_in_the_air_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_person_laying_on_a_puddle_of_water_with_a_head_in_the_air_1.jpg",
    "cartoon_of_a_woman_sitting_in_front_of_a_computer_on_a_desk_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_woman_sitting_in_front_of_a_computer_on_a_desk_1.jpg",
    "cartoon_of_a_woman_sitting_in_front_of_a_computer_screen_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/cartoon_of_a_woman_sitting_in_front_of_a_computer_screen_1.jpg",
    "chess_pieces_are_sitting_on_a_checkered_floor_with_a_mirror_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/chess_pieces_are_sitting_on_a_checkered_floor_with_a_mirror_1.jpg",
    "dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_1.jpg",
    "dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_2": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_dora_2.jpg",
    "drawing_of_a_dog_with_a_mustache_and_a_nose_ring_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/drawing_of_a_dog_with_a_mustache_and_a_nose_ring_1.jpg",
    "drawing_of_a_horse_with_a_bow_on_its_head_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/drawing_of_a_horse_with_a_bow_on_its_head_1.jpg",
    "five_cartoon_characters_are_standing_on_a_stage_with_a_guitar_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/five_cartoon_characters_are_standing_on_a_stage_with_a_guitar_1.jpg",
    "futuristic_city_with_skyscrapers_and_a_fountain_in_the_middle_of_it_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/futuristic_city_with_skyscrapers_and_a_fountain_in_the_middle_of_it_1.jpg",
    "jesus_standing_in_the_clouds_with_his_arms_outstretched_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/jesus_standing_in_the_clouds_with_his_arms_outstretched_1.jpg",
    "painting_of_a_group_of_men_fighting_an_elephant_with_spears_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/painting_of_a_group_of_men_fighting_an_elephant_with_spears_1.jpg",
    "painting_of_a_man_holding_a_wine_glass_in_front_of_a_plate_of_food_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/painting_of_a_man_holding_a_wine_glass_in_front_of_a_plate_of_food_1.jpg",
    "painting_of_a_man_holding_a_woman's_arm_in_a_fist_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/painting_of_a_man_holding_a_woman's_arm_in_a_fist_1.jpg",
    "penguin_with_gun_and_cowboy_hat_royalty_photo_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/penguin_with_gun_and_cowboy_hat_royalty_photo_1.jpg",
    "people_are_gathered_around_a_hole_in_the_ground_to_dig_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/people_are_gathered_around_a_hole_in_the_ground_to_dig_1.jpg",
    "people_are_riding_on_a_bus_with_their_hands_in_the_windows_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/people_are_riding_on_a_bus_with_their_hands_in_the_windows_1.jpg",
    "people_standing_around_a_hole_with_a_man_digging_a_hole_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/people_standing_around_a_hole_with_a_man_digging_a_hole_1.jpg",
    "pirates_of_the_caribbean_2012_dual_audio_-_dvdrip_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/pirates_of_the_caribbean_2012_dual_audio_-_dvdrip_1.jpg",
    "pregnant_woman_eating_pizza_and_eating_a_box_of_chicken_wings_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/pregnant_woman_eating_pizza_and_eating_a_box_of_chicken_wings_1.jpg",
    "red_and_black_carbon_background_with_diagonal_stripes_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/red_and_black_carbon_background_with_diagonal_stripes_1.jpg",
    "several_men_are_playing_violin_and_violin_on_a_stage_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/several_men_are_playing_violin_and_violin_on_a_stage_1.jpg",
    "several_people_are_huddled_around_a_woman_on_the_street_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/several_people_are_huddled_around_a_woman_on_the_street_1.jpg",
    "silhouette_of_a_man_in_a_top_hat_and_tails_holding_a_cane_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/silhouette_of_a_man_in_a_top_hat_and_tails_holding_a_cane_1.jpg",
    "skeleton_sitting_on_a_table_with_a_laptop_computer_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/skeleton_sitting_on_a_table_with_a_laptop_computer_1.jpg",
    "smiling_man_sitting_at_a_desk_with_a_laptop_and_a_cup_of_coffee_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/smiling_man_sitting_at_a_desk_with_a_laptop_and_a_cup_of_coffee_1.jpg",
    "someone_is_holding_a_toy_dinosaur_in_their_hand_in_a_store_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/someone_is_holding_a_toy_dinosaur_in_their_hand_in_a_store_1.jpg",
    "someone_is_touching_a_button_on_a_black_background_with_a_hand_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/someone_is_touching_a_button_on_a_black_background_with_a_hand_1.jpg",
    "spider_-_man_and_spider_-_woman_fighting_in_a_room_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/spider_-_man_and_spider_-_woman_fighting_in_a_room_1.jpg",
    "spider_-_man_in_a_train_with_his_arms_outstretched_out_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/spider_-_man_in_a_train_with_his_arms_outstretched_out_1.jpg",
    "spongebob_waving_his_hands_in_front_of_a_rainbow_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/spongebob_waving_his_hands_in_front_of_a_rainbow_1.jpg",
    "there_are_many_men_riding_horses_in_a_field_with_a_sword_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_are_many_men_riding_horses_in_a_field_with_a_sword_1.jpg",
    "there_are_two_men_shaking_hands_in_an_office_setting_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_are_two_men_shaking_hands_in_an_office_setting_1.jpg",
    "there_are_two_people_sitting_in_a_dark_room_looking_at_a_cell_phone_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_are_two_people_sitting_in_a_dark_room_looking_at_a_cell_phone_1.jpg",
    "there_are_two_people_standing_on_the_sidewalk_talking_on_their_cell_phones_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_are_two_people_standing_on_the_sidewalk_talking_on_their_cell_phones_1.jpg",
    "there_are_two_people_that_are_eating_food_together_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_are_two_people_that_are_eating_food_together_1.jpg",
    "there_are_two_pictures_of_a_dog_sitting_at_a_desk_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_are_two_pictures_of_a_dog_sitting_at_a_desk_1.jpg",
    "there_are_two_pictures_of_a_white_bird_with_a_red_background_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_are_two_pictures_of_a_white_bird_with_a_red_background_1.jpg",
    "there_are_two_vases_of_flowers_sitting_on_a_stone_grave_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_are_two_vases_of_flowers_sitting_on_a_stone_grave_1.jpg",
    "there_is_a_blue_alien_with_green_eyes_and_a_black_nose_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_is_a_blue_alien_with_green_eyes_and_a_black_nose_1.jpg",
    "there_is_a_cartoon_face_with_a_big_smile_on_it_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_is_a_cartoon_face_with_a_big_smile_on_it_1.jpg",
    "there_is_a_cat_that_is_looking_at_the_camera_from_underneath_a_chair_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_is_a_cat_that_is_looking_at_the_camera_from_underneath_a_chair_1.jpg",
    "there_is_a_little_girl_that_is_wearing_a_black_shirt_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_is_a_little_girl_that_is_wearing_a_black_shirt_1.jpg",
    "there_is_a_man_in_a_shirt_and_tie_making_a_funny_face_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_is_a_man_in_a_shirt_and_tie_making_a_funny_face_1.jpg",
    "there_is_a_man_sitting_on_a_swing_with_a_laptop_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_is_a_man_sitting_on_a_swing_with_a_laptop_1.jpg",
    "there_is_a_man_that_is_brushing_his_teeth_in_front_of_a_blackboard_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_is_a_man_that_is_brushing_his_teeth_in_front_of_a_blackboard_1.jpg",
    "there_is_a_man_that_is_holding_a_donut_in_his_hand_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_is_a_man_that_is_holding_a_donut_in_his_hand_1.jpg",
    "there_is_a_man_that_is_standing_in_front_of_a_laptop_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_is_a_man_that_is_standing_in_front_of_a_laptop_1.jpg",
    "there_is_a_picture_of_a_pink_and_yellow_background_with_sprinkles_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_is_a_picture_of_a_pink_and_yellow_background_with_sprinkles_1.jpg",
    "there_is_a_small_stuffed_animal_with_a_toothbrush_in_its_mouth_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/there_is_a_small_stuffed_animal_with_a_toothbrush_in_its_mouth_1.jpg",
    "the_logo_for_the_band,_the_band,_is_shown_in_white_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/the_logo_for_the_band,_the_band,_is_shown_in_white_1.jpg",
    "three_cartoon_snakes_with_their_mouths_open_and_tongue_out_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/three_cartoon_snakes_with_their_mouths_open_and_tongue_out_1.jpg",
    "three_girls_in_school_uniforms_are_sitting_on_a_bench_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/three_girls_in_school_uniforms_are_sitting_on_a_bench_1.jpg",
    "two_emoticions_of_a_man_and_woman_with_different_colors_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/two_emoticions_of_a_man_and_woman_with_different_colors_1.jpg",
    "two_men_are_talking_to_each_other_while_one_is_yelling_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/two_men_are_talking_to_each_other_while_one_is_yelling_1.jpg",
    "two_pictures_of_a_cheetah_and_a_turtle_running_together_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/two_pictures_of_a_cheetah_and_a_turtle_running_together_1.jpg",
    "two_women_in_bunny_ears_are_putting_their_hands_together_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/two_women_in_bunny_ears_are_putting_their_hands_together_1.jpg",
    "two_young_girls_in_colorful_swimsuits_standing_next_to_each_other_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/two_young_girls_in_colorful_swimsuits_standing_next_to_each_other_1.jpg",
    "uncle_in_a_top_hat_pointing_at_the_camera_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/uncle_in_a_top_hat_pointing_at_the_camera_1.jpg",
    "woman_holding_a_stack_of_money_in_her_hand_and_handing_it_to_a_man_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/woman_holding_a_stack_of_money_in_her_hand_and_handing_it_to_a_man_1.jpg",
    "yoda_is_the_most_popular_character_in_star_wars_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/yoda_is_the_most_popular_character_in_star_wars_1.jpg"
}

    prompt = "We got investment"
    api_key = "AIzaSyCEDJ1aaSEGimwoSgF-bSNY2PP4i-j4_Kc"

    meme_generator = MemeGenerator(api_key, template_paths)
    try:
        meme = meme_generator.create_meme(prompt)
        cv2.imwrite("output_meme.jpg", meme)
    except FileNotFoundError as e:
        print(e)
