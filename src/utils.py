from publitio import PublitioAPI
import os
# from imgurpython import ImgurClient


working_dir = os.getcwd()

GEN_KEY = "AIzaSyCEDJ1aaSEGimwoSgF-bSNY2PP4i-j4_Kc"
api_key = 'jP6avoTuQW3LhlQN6fkR'
api_secret = 'zQz5nJtbbNLJliVe5gLq8zVwfiRQvBLB'

current_directory = os.getcwd()
INPUT = os.path.join(current_directory, "artifacts", "Input.jpg")
OUTPUT = os.path.join(current_directory, "artifacts", "output.jpg")
OUTPUT_VEDIO = os.path.join(current_directory, "artifacts", "output_video.mp4")
OUTPUT_MEME = os.path.join(current_directory, "artifacts", "output_meme.jpg")
UPLOAD = os.path.join(current_directory, "artifacts")
FONT = os.path.join(current_directory, "artifacts", "impact.ttf")
VIDEOMEMEPATH = os.path.join(current_directory, "artifacts", "videomeme.mp4")
VIDEOMEMEPATHOUT = os.path.join(current_directory, "artifacts", "videomeme_out.mp4")


publitio_api = PublitioAPI(key=api_key , secret=api_secret)

def savenft(path):
    # client_id = 'eaa91a80f980b64'
    # client_secret = '06777683059c78566531dcb821a785d809382f1f'
    # client = ImgurClient(client_id, client_secret)
    # response = client.upload_from_path(path, anon=True)
    # image_link = response['link']
    # return image_link, image_link
    
    data = publitio_api.create_file(file=open(path, 'rb'),
                            title='My title',
                            description='My description')
            
    return data['url_preview'], data["url_download"]

template_paths = {
    "adam_coles_surprise_kiss": os.path.join(working_dir, "img_templates", "Adam_Coles_Surprise_Kiss_Catch_Wrestling_WWE_Bisou.jpeg"),
    "adam_sandler_chasing_woman": os.path.join(working_dir, "img_templates", "Adam_Sandler_Chasing_Woman_No_Purse_Uncut_Gem_Empty_Template_red_dress_robe_rouge_court_peur_crie_effrayee_rue_without_bagjpg.png"),
    "alien_god_looking_down": os.path.join(working_dir, "img_templates", "Alien_God_Looks_Down_at_Lower_Beings_Empty_Template.jpg"),
    "american_dad_threat_level": os.path.join(working_dir, "img_templates", "American_Dad_Threat_Level_Empty_Template_Stan_Looking_At_Terror_Threat_Level_Fleche_Niveau_Couleur_Color_Curseur.jpg"),
    "am_i_a_joke": os.path.join(working_dir, "img_templates", "Am_I_A_Joke_To_You.jpg"),
    "anthony_adams_rubbing_hands": os.path.join(working_dir, "img_templates", "Anthony_Adams_Rubbing_Hands_Coffin_Dance_Dancing_Pallbearers_Template_black_jaune_arbre.jpeg"),
    "batman_slapping_robin": os.path.join(working_dir, "img_templates", "Batman_Slapping_Robin_My_Parents_Are_Dead_Template_FULL_CLEAN_robin_baffe_claque.jpg"),
    "bending_streetlight": os.path.join(working_dir, "img_templates", "Bending_Streetlight_Mojtaba_Heidarpanah_Lamppost_Night_Light_Read_Book_Smartphone_lampadaire_lumire_nuit_clairer_lire_livre.png"),
    "big_bullet_small_gun": os.path.join(working_dir, "img_templates", "Big_Bullet_Small_Gun_Template_arme_cartouche_balle_munition.jpg"),
    "taking_notes": os.path.join(working_dir, "img_templates", "Black_Guys_Taking_Notes_Jamal_Randle_Loren_Cowling_and_Dave_Jackson_Notebook_Write_Notes_crire_cahier.jpg"),
    "blinking_white_guy": os.path.join(working_dir, "img_templates", "Blinking_White_Guy_Drew_Scanlon_Reaction_Template_Surprised_Shocked_regard_yeux.png"),
    "blue_red_pill": os.path.join(working_dir, "img_templates", "Bluered_pill.png"),
    "bugs_bunny_no": os.path.join(working_dir, "img_templates", "Bugs_Bunnys_No.png"),
    "camera_zoom_on_breasts": os.path.join(working_dir, "img_templates", "Camera_Zooming_on_Rosas_Breasts_Empty_Template_Anime_girl_nichons_seins_photo_boobs.jpg"),
    "deer_afraid_of_hand": os.path.join(working_dir, "img_templates", "Deer_Afraid_Of_Hand_Template_Biche_faon_Bambi_peur.png"),
    "disaster_girl_smiling": os.path.join(working_dir, "img_templates", "disaster_girl_smiling_burning_house_fillette_incendie_feu_maison_fille.jpg"),
    "distracted_boy": os.path.join(working_dir, "img_templates", "Distracted_boy.png"),
    "money_bucks_sleep": os.path.join(working_dir, "img_templates", "dollars_money_bucks_fat_black_sleep.png"),
    "domino_effect": os.path.join(working_dir, "img_templates", "Domino_effect.jpg"),
    "dont_hate_the_play": os.path.join(working_dir, "img_templates", "Dont_Hate_The_Play_Hate_The_game_Son_Rick_Sanchez_Rick_and_Morty.jpg"),
    "el_risitas_laughing": os.path.join(working_dir, "img_templates", "El_risitas_laughting_rire.jpg"),
    "fake_cake": os.path.join(working_dir, "img_templates", "fake_Bangladesh_cake_during_panels_gateau.jpg"),
    "false_start": os.path.join(working_dir, "img_templates", "False_Start_Empty_Template_Track_Race_Wrong_Way.png"),
    "fitness_passion_boy": os.path.join(working_dir, "img_templates", "Fitness_is_My_Passion_Boy_Whos_Passion_is_Fitness_Sharm_elSheikh.jpg"),
    "flex_tape_ad": os.path.join(working_dir, "img_templates", "Flex_tape_ad_Phil_swift_slaps_on_flex_scotch_eau_coule.jpg"),
    "girl_car": os.path.join(working_dir, "img_templates", "Girl_car_fille_voiture.jpg"),
    "grandma_hiding_knife": os.path.join(working_dir, "img_templates", "Grandma_hiding_knife_from_rabbit_mamie_grand_mere_couteau_lapin.jpg"),
    "gta_here_we_go_again": os.path.join(working_dir, "img_templates", "GTA_ah_shit_here_we_go_again.jpg"),
    "hamsters_carotte": os.path.join(working_dir, "img_templates", "hamsters_carotte.png"),
    "happy_cat": os.path.join(working_dir, "img_templates", "Happy_Cat_NEDM_Not_Even_Doom_Music_I_Can_Has_Cheezburger_Cat_Upscale_x.png"),
    "hello_darkness": os.path.join(working_dir, "img_templates", "hello_darkness.jpg"),
    "hide_the_pain_harold": os.path.join(working_dir, "img_templates", "Hide_The_Pain_Harold_Maurice.jpg"),
    "funny_guys_in_costumes": os.path.join(working_dir, "img_templates", "hommes_costumes_fou_rire_riches.jpg"),
    "honest_work": os.path.join(working_dir, "img_templates", "honest_work_paysan_fermier_agriculteur_travail.jpg"),
    "joint": os.path.join(working_dir, "img_templates", "joint_bdo_weed_splif.jpg"),
    "joker": os.path.join(working_dir, "img_templates", "Joker_you_wouldnt_get_it.jpg"),
    "just_light_it_cat": os.path.join(working_dir, "img_templates", "Just_Light_It_Linda_Depressed_Cat_In_Pot_On_Stove_Empty_Template.png"),
    "khaby_lame": os.path.join(working_dir, "img_templates", "khaby_lame_v.jpg"),
    "kid_stairs": os.path.join(working_dir, "img_templates", "Kid_stairs_enfant_marches_escalier_bateau.jpg"),
    "kirby_sign": os.path.join(working_dir, "img_templates", "Kirby_sign.jpg"),
    "man_smacking_cards": os.path.join(working_dir, "img_templates", "Man_smacking_cards_down_on_table_cartes.jpg"),
    "math_calculating": os.path.join(working_dir, "img_templates", "Math_calcul.png"),
    "modern_problems_solutions": os.path.join(working_dir, "img_templates", "Modern_Problems_Require_Modern_Solutions_Chappelles_show.png"),
    "narcos_boring": os.path.join(working_dir, "img_templates", "Narcos_boring_sad_pablo_denoisedenoise.png"),
    "parkour_michael": os.path.join(working_dir, "img_templates", "Parkour_Michael_Gary_Scott_The_Office.jpg"),
    "pathetic_cat": os.path.join(working_dir, "img_templates", "Pathetic_Cat_Full_Image.png"),
    "peter_parker_glasses": os.path.join(working_dir, "img_templates", "Peter_Parkers_Glasses_SpiderMan.jpg"),
    "piper_perri": os.path.join(working_dir, "img_templates", "Piper_Perri_Surrounded_Black_Men_White_Woman.png"),
    "polite_cat": os.path.join(working_dir, "img_templates", "Polite_Cat_He_Looks_Very_Polite_Template_Chat_Troll.png"),
    "happy_rat": os.path.join(working_dir, "img_templates", "rat_mouse_happy_hands.png"),
    "return_to_monkey": os.path.join(working_dir, "img_templates", "return_to_monkey_v.jpg"),
    "sad_birthday_cat": os.path.join(working_dir, "img_templates", "Sad_Birthday_Cat_Hat_Candle_Cake_Chat_Cat_Triste_Anniversaire_Bougie_Pat.jpg"),
    "salt_bae": os.path.join(working_dir, "img_templates", "Salt_Bae_Original.png"),
    "shrugging_tom": os.path.join(working_dir, "img_templates", "Shrugging_Tom_HD_Redraw_Tom_and_Jerry_u_Gibus_Squidward_on_Reddit.jpg"),
    "spiderman_pointing": os.path.join(working_dir, "img_templates", "SpiderMan_Pointing_At_SpiderMan_Pointing_At_SpiderMan_Template.png"),
    "surprised_reaction": os.path.join(working_dir, "img_templates", "Surprised_reaction_surprise_reaction.jpg"),
    "thinking_cat": os.path.join(working_dir, "img_templates", "Thinking_Cat_Enigmatic_Guy_Who_Is_Confused_Cat_Arrrgh.jpeg"),
    "triumph_cat": os.path.join(working_dir, "img_templates", "triumph_cat.jpg"),
    "unfortunate_events": os.path.join(working_dir, "img_templates", "Unfortunate_Events_Template_Events_Cat.png"),
    "very_angry": os.path.join(working_dir, "img_templates", "Very_Angry_White_Guy_Furious_Empty_Template.jpg"),
}



template_video_paths = {
    "modi_thakan_nahi_lag_rahi": os.path.join(working_dir, "video_templates/m2.mp4"),
    "kids_running_after_sighting": os.path.join(working_dir, "video_templates/m3.mp4"),
    "man_shocked_reaction": os.path.join(working_dir, "video_templates/m4.mp4"),
    "amazing_sighting_reaction": os.path.join(working_dir, "video_templates/m5.mp4"),
    "mischievous_laughter": os.path.join(working_dir, "video_templates/m6.mp4"),
    "guy_laughing_happily": os.path.join(working_dir, "video_templates/m7.mp4"),
    "achieving_without_effort": os.path.join(working_dir, "video_templates/m8.mp4"),
    "guy_losing_stability": os.path.join(working_dir, "video_templates/m9.mp4"),
    "scrolling_in_mood": os.path.join(working_dir, "video_templates/m10.mp4"),
    "stop_it_request": os.path.join(working_dir, "video_templates/m11.mp4"),
    "tumse_nahi_ho_payega": os.path.join(working_dir, "video_templates/m12.mp4"),
    "cat_dancing_chipi_chipi": os.path.join(working_dir, "video_templates/m13.mp4"),
    "dedh_sau_rupyee_dega": os.path.join(working_dir, "video_templates/m14.mp4"),
    "guy_dancing_in_dress": os.path.join(working_dir, "video_templates/m1.mp4"),
    "guy_confused_about_situation": os.path.join(working_dir, "video_templates/m15.mp4"),
    "guys_shouting_jaga_nahi": os.path.join(working_dir, "video_templates/m16.mp4"),
    "harsh_beniwal_meme": os.path.join(working_dir, "video_templates/m17.mp4"),
    "abba_nahi_manege": os.path.join(working_dir, "video_templates/m18.mp4"),
    "woman_haha_laugh": os.path.join(working_dir, "video_templates/m19.mp4"),
    "traumatized_cat": os.path.join(working_dir, "video_templates/m20.mp4"),
    "modi_dancing": os.path.join(working_dir, "video_templates/m21.mp4"),
    "hero_entry_in_south_movie": os.path.join(working_dir, "video_templates/m22.mp4"),
    "mujhe_chakka_lag_raha": os.path.join(working_dir, "video_templates/m23.mp4"),
    "tejashvi_log_hai": os.path.join(working_dir, "video_templates/m24.mp4"),
    "father_reaction_wrong_action": os.path.join(working_dir, "video_templates/m25.mp4"),
    "modi_with_meloni": os.path.join(working_dir, "video_templates/m26.mp4"),
    "happy_after_implementing_meme": os.path.join(working_dir, "video_templates/m5.mp4"),
    "crypto_portfolio_loss": os.path.join(working_dir, "video_templates/m15.mp4"),
    "mind_after_24hrs_hackathon": os.path.join(working_dir, "video_templates/m20.mp4"),
    "happy_after_seeing_coffee_machine": os.path.join(working_dir, "video_templates/m13.mp4"),
    "invigilator_instascroll": os.path.join(working_dir, "video_templates/m10.mp4"),
    "mind_before_exam_instascroll": os.path.join(working_dir, "video_templates/m10.mp4"),
}



