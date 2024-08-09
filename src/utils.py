import cv2
from publitio import PublitioAPI
import os

working_dir = os.getcwd()

GEN_KEY = "AIzaSyCEDJ1aaSEGimwoSgF-bSNY2PP4i-j4_Kc"
# GEN_KEY = "AIzaSyBa5b8ZuK83ehPi52ua4Ly724ofJHTT5Zk"
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
    
    from imgurpython import ImgurClient

    # Replace these with your Imgur client ID and secret
    # client_id = '7f25a5359417cee'
    client_id = "3e33f272860472d"
    # client_secret = '7f25a5359417cee'
    client_secret = '0fe0243f351ff6779ca2bbbc71254f70e8a4b221'

    # Create an ImgurClient instance
    client = ImgurClient(client_id, client_secret)

    # Upload the image
    response = client.upload_from_path(path, anon=True)

    # Get the link to the uploaded image
    image_link = response['link']
    print(f"Image uploaded successfully. Link: {image_link}")
    return image_link, image_link
    
    # print(f"Image uploaded successfully. Link: {image_link}")
    # data = publitio_api.create_file(file=open(path, 'rb'),
    #                         title='My title',
    #                         description='My description')
            
    # return data['url_preview'], data["url_download"]

template_paths = {
    "adam_coles_surprise_kiss_catch_wrestling_wwe_bisou": os.path.join(working_dir, "img_templates", "Adam_Coles_Surprise_Kiss_Catch_Wrestling_WWE_Bisou.jpeg"),
    "adam_sandler_chasing_woman_no_purse_uncut_gem_empty_template_red_dress_robe_rouge_court_peur_crie_effrayee_rue_without_bagjpg": os.path.join(working_dir, "img_templates", "Adam_Sandler_Chasing_Woman_No_Purse_Uncut_Gem_Empty_Template_red_dress_robe_rouge_court_peur_crie_effrayee_rue_without_bagjpg.png"),
    "alien_god_looks_down_at_lower_beings_empty_template": os.path.join(working_dir, "img_templates", "Alien_God_Looks_Down_at_Lower_Beings_Empty_Template.jpg"),
    "american_dad_threat_level_empty_template_stan_looking_at_terror_threat_level_fleche_niveau_couleur_color_curseur": os.path.join(working_dir, "img_templates", "American_Dad_Threat_Level_Empty_Template_Stan_Looking_At_Terror_Threat_Level_Fleche_Niveau_Couleur_Color_Curseur.jpg"),
    "am_i_a_joke_to_you": os.path.join(working_dir, "img_templates", "Am_I_A_Joke_To_You.jpg"),
    "anthony_adams_rubbing_hands_coffin_dance_dancing_pallbearers_template_black_jaune_arbre": os.path.join(working_dir, "img_templates", "Anthony_Adams_Rubbing_Hands_Coffin_Dance_Dancing_Pallbearers_Template_black_jaune_arbre.jpeg"),
    "batman_slapping_robin_my_parents_are_dead_template_full_clean_robin_baffe_claque": os.path.join(working_dir, "img_templates", "Batman_Slapping_Robin_My_Parents_Are_Dead_Template_FULL_CLEAN_robin_baffe_claque.jpg"),
    "bending_streetlight_mojtaba_heidarpanah_lamppost_night_light_read_book_smartphone_lampadaire_lumire_nuit_clairer_lire_livre": os.path.join(working_dir, "img_templates", "Bending_Streetlight_Mojtaba_Heidarpanah_Lamppost_Night_Light_Read_Book_Smartphone_lampadaire_lumire_nuit_clairer_lire_livre.png"),
    "big_bullet_small_gun_template_arme_cartouche_balle_munition": os.path.join(working_dir, "img_templates", "Big_Bullet_Small_Gun_Template_arme_cartouche_balle_munition.jpg"),
    "taking_notes_jamal_randle_loren_cowling_and_dave_jackson_notebook_write_notes_crire_cahier": os.path.join(working_dir, "img_templates", "Black_Guys_Taking_Notes_Jamal_Randle_Loren_Cowling_and_Dave_Jackson_Notebook_Write_Notes_crire_cahier.jpg"),
    "blinking_white_guy_drew_scanlon_reaction_template_surprised_shocked_regard_yeux": os.path.join(working_dir, "img_templates", "Blinking_White_Guy_Drew_Scanlon_Reaction_Template_Surprised_Shocked_regard_yeux.png"),
    "bluered_pill": os.path.join(working_dir, "img_templates", "Bluered_pill.png"),
    "bugs_bunnys_no": os.path.join(working_dir, "img_templates", "Bugs_Bunnys_No.png"),
    "camera_zooming_on_rosas_breasts_empty_template_anime_girl_nichons_seins_photo_boobs": os.path.join(working_dir, "img_templates", "Camera_Zooming_on_Rosas_Breasts_Empty_Template_Anime_girl_nichons_seins_photo_boobs.jpg"),
    "deer_afraid_of_hand_template_biche_faon_bambi_peur": os.path.join(working_dir, "img_templates", "Deer_Afraid_Of_Hand_Template_Biche_faon_Bambi_peur.png"),
    "disaster_girl_smiling_burning_house_fillette_incendie_feu_maison_fille": os.path.join(working_dir, "img_templates", "disaster_girl_smiling_burning_house_fillette_incendie_feu_maison_fille.jpg"),
    "distracted_boy": os.path.join(working_dir, "img_templates", "Distracted_boy.png"),
    "dollars_money_bucks_fat_black_sleep": os.path.join(working_dir, "img_templates", "dollars_money_bucks_fat_black_sleep.png"),
    "domino_effect": os.path.join(working_dir, "img_templates", "Domino_effect.jpg"),
    "dont_hate_the_play_hate_the_game_son_rick_sanchez_rick_and_morty": os.path.join(working_dir, "img_templates", "Dont_Hate_The_Play_Hate_The_game_Son_Rick_Sanchez_Rick_and_Morty.jpg"),
    "el_risitas_laughting_rire": os.path.join(working_dir, "img_templates", "El_risitas_laughting_rire.jpg"),
    "fake_bangladesh_cake_during_panels_gateau": os.path.join(working_dir, "img_templates", "fake_Bangladesh_cake_during_panels_gateau.jpg"),
    "false_start_empty_template_track_race_wrong_way": os.path.join(working_dir, "img_templates", "False_Start_Empty_Template_Track_Race_Wrong_Way.png"),
    "fitness_is_my_passion_boy_whos_passion_is_fitness_sharm_elsheikh": os.path.join(working_dir, "img_templates", "Fitness_is_My_Passion_Boy_Whos_Passion_is_Fitness_Sharm_elSheikh.jpg"),
    "flex_tape_ad_phil_swift_slaps_on_flex_scotch_eau_coule": os.path.join(working_dir, "img_templates", "Flex_tape_ad_Phil_swift_slaps_on_flex_scotch_eau_coule.jpg"),
    "girl_car_fille_voiture": os.path.join(working_dir, "img_templates", "Girl_car_fille_voiture.jpg"),
    "grandma_hiding_knife_from_rabbit_mamie_grand_mere_couteau_lapin": os.path.join(working_dir, "img_templates", "Grandma_hiding_knife_from_rabbit_mamie_grand_mere_couteau_lapin.jpg"),
    "gta_ah_shit_here_we_go_again": os.path.join(working_dir, "img_templates", "GTA_ah_shit_here_we_go_again.jpg"),
    "hamsters_carotte": os.path.join(working_dir, "img_templates", "hamsters_carotte.png"),
    "happy_cat_nedm_not_even_doom_music_i_can_has_cheezburger_cat_upscale_x": os.path.join(working_dir, "img_templates", "Happy_Cat_NEDM_Not_Even_Doom_Music_I_Can_Has_Cheezburger_Cat_Upscale_x.png"),
    "hello_darkness": os.path.join(working_dir, "img_templates", "hello_darkness.jpg"),
    "hide_the_pain_harold_maurice": os.path.join(working_dir, "img_templates", "Hide_The_Pain_Harold_Maurice.jpg"),
    "hommes_costumes_fou_rire_riches": os.path.join(working_dir, "img_templates", "hommes_costumes_fou_rire_riches.jpg"),
    "honest_work_paysan_fermier_agriculteur_travail": os.path.join(working_dir, "img_templates", "honest_work_paysan_fermier_agriculteur_travail.jpg"),
    "joint_bdo_weed_splif": os.path.join(working_dir, "img_templates", "joint_bdo_weed_splif.jpg"),
    "joker_you_wouldnt_get_it": os.path.join(working_dir, "img_templates", "Joker_you_wouldnt_get_it.jpg"),
    "juan": os.path.join(working_dir, "img_templates", "juan.png"),
    "just_light_it_linda_depressed_cat_in_pot_on_stove_empty_template": os.path.join(working_dir, "img_templates", "Just_Light_It_Linda_Depressed_Cat_In_Pot_On_Stove_Empty_Template.png"),
    "khaby_lame_v": os.path.join(working_dir, "img_templates", "khaby_lame_v.jpg"),
    "kid_stairs_enfant_marches_escalier_bateau": os.path.join(working_dir, "img_templates", "Kid_stairs_enfant_marches_escalier_bateau.jpg"),
    "kirby_sign": os.path.join(working_dir, "img_templates", "Kirby_sign.jpg"),
    "man_smacking_cards_down_on_table_cartes": os.path.join(working_dir, "img_templates", "Man_smacking_cards_down_on_table_cartes.jpg"),
    "math_calcul": os.path.join(working_dir, "img_templates", "Math_calcul.png"),
    "modern_problems_require_modern_solutions_chappelles_show": os.path.join(working_dir, "img_templates", "Modern_Problems_Require_Modern_Solutions_Chappelles_show.png"),
    "narcos_boring_sad_pablo_denoisedenoise": os.path.join(working_dir, "img_templates", "Narcos_boring_sad_pablo_denoisedenoise.png"),
    "parkour_michael_gary_scott_the_office": os.path.join(working_dir, "img_templates", "Parkour_Michael_Gary_Scott_The_Office.jpg"),
    "pathetic_cat_full_image": os.path.join(working_dir, "img_templates", "Pathetic_Cat_Full_Image.png"),
    "peter_parkers_glasses_spiderman": os.path.join(working_dir, "img_templates", "Peter_Parkers_Glasses_SpiderMan.jpg"),
    "piper_perri_surrounded_black_men_white_woman": os.path.join(working_dir, "img_templates", "Piper_Perri_Surrounded_Black_Men_White_Woman.png"),
    "polite_cat_he_looks_very_polite_template_chat_troll": os.path.join(working_dir, "img_templates", "Polite_Cat_He_Looks_Very_Polite_Template_Chat_Troll.png"),
    "rat_mouse_happy_hands": os.path.join(working_dir, "img_templates", "rat_mouse_happy_hands.png"),
    "return_to_monkey_v": os.path.join(working_dir, "img_templates", "return_to_monkey_v.jpg"),
    "sad_birthday_cat_hat_candle_cake_chat_cat_triste_anniversaire_bougie_pat": os.path.join(working_dir, "img_templates", "Sad_Birthday_Cat_Hat_Candle_Cake_Chat_Cat_Triste_Anniversaire_Bougie_Pat.jpg"),
    "salt_bae_original": os.path.join(working_dir, "img_templates", "Salt_Bae_Original.png"),
    "shrugging_tom_hd_redraw_tom_and_jerry_u_gibus_squidward_on_reddit": os.path.join(working_dir, "img_templates", "Shrugging_Tom_HD_Redraw_Tom_and_Jerry_u_Gibus_Squidward_on_Reddit.jpg"),
    "spiderman_pointing_at_spiderman_pointing_at_spiderman_template": os.path.join(working_dir, "img_templates", "SpiderMan_Pointing_At_SpiderMan_Pointing_At_SpiderMan_Template.png"),
    "spooky_hat_cat_halloween_chat_cat": os.path.join(working_dir, "img_templates", "Spooky_Hat_Cat_Halloween_Chat_Cat.jpg"),
    "squid_game_soleil": os.path.join(working_dir, "img_templates", "squid_game_soleil.png"),
    "stadium_angry_pakistani_fan_stade_homme_debout_nerv_tribunes_gradins": os.path.join(working_dir, "img_templates", "Stadium_Angry_Pakistani_Fan_Stade_homme_debout_nerv_tribunes_gradins.jpg"),
    "stonks_hd_meme_man_stocks": os.path.join(working_dir, "img_templates", "Stonks_HD_Meme_Man_Stocks.png"),
    "surprised_cat_surprised_math_lady_calculating_chat": os.path.join(working_dir, "img_templates", "Surprised_Cat_Surprised_Math_Lady_Calculating_chat.jpg"),
    "surprised_pikachu_shocked_pikachu_pikachu_surpris_pikachu_choqu": os.path.join(working_dir, "img_templates", "Surprised_Pikachu_Shocked_Pikachu_Pikachu_surpris_Pikachu_choqu.png"),
    "sweating_jordan_peele_black_man_profusely_sweating_wet_sueur_mouill_transpiration": os.path.join(working_dir, "img_templates", "Sweating_Jordan_Peele_Black_Man_Profusely_Sweating_wet_sueur_mouill_transpiration.jpg"),
    "tell_me_the_truth_im_ready_to_hear_it_tell_me_the_truthimim_ready_to_hear_it_spiderman_empty_template_no_text": os.path.join(working_dir, "img_templates", "Tell_Me_The_Truth_Im_Ready_To_Hear_It_Tell_Me_The_TruthImIm_Ready_To_Hear_It_SpiderMan_Empty_Template_No_Text.jpg"),
    "thanos_avengers_i_am_inevitable": os.path.join(working_dir, "img_templates", "thanos_avengers_i_am_inevitable.jpg"),
    "the_office_enqute": os.path.join(working_dir, "img_templates", "the_office_enqute.jpg"),
    "the_office_young_michael_scott_shaking_ed_trucks_hand": os.path.join(working_dir, "img_templates", "The_office_Young_Michael_Scott_shaking_Ed_Trucks_hand.png"),
    "trump_correcting_kim_jongun": os.path.join(working_dir, "img_templates", "Trump_correcting_Kim_JongUn.jpg"),
    "undertaker_standing_behind_catch_wwe": os.path.join(working_dir, "img_templates", "undertaker_standing_behind_catch_wwe.jpg"),
    "uno_enfant_kid_child": os.path.join(working_dir, "img_templates", "uno_enfant_kid_child.jpg"),
    "wife_vs_wave_femme_vague": os.path.join(working_dir, "img_templates", "wife_vs_wave_femme_vague.jpg"),
    "will_smith_slap_v": os.path.join(working_dir, "img_templates", "Will_smith_slap_v.JPG"),
    "windows_xp_task_successful": os.path.join(working_dir, "img_templates", "Windows_xp_task_successful.jpg"),
    "woman_yelling_at_a_cat_empty_template": os.path.join(working_dir, "img_templates", "Woman_Yelling_At_A_Cat_Empty_Template.jpg"),
    "woman_yelling_at_a_cat_empty_template_smile_smiling_femme_chat": os.path.join(working_dir, "img_templates", "Woman_Yelling_At_A_Cat_Empty_Template_Smile_Smiling_femme_chat.jpg"),
    "wooo_dexter_reed_good_burger_glowing_red_eyes_lens_flare": os.path.join(working_dir, "img_templates", "Wooo_Dexter_Reed_Good_Burger_Glowing_Red_Eyes_Lens_Flare.jpg"),
}




# Template paths dictionary with dynamic paths based on the working directory
template_video_paths = {
    "modi_saying_kya_re_bete_tujhe_thakan_nhi_lag_rahi_kya": os.path.join(working_dir, "video_templates/m2.mp4"),
    "two_kids_are_running_after_seeing_something": os.path.join(working_dir, "video_templates/m3.mp4"),
    "man_shocked_after_seeing_something": os.path.join(working_dir, "video_templates/m4.mp4"),
    "man_reaction_after_seeing_something_amazing_good": os.path.join(working_dir, "video_templates/m5.mp4"),
    "laughing_mischievously_devilish_laugh": os.path.join(working_dir, "video_templates/m6.mp4"),
    "guy_lauging_and_saying_maja_aa_raha_hai": os.path.join(working_dir, "video_templates/m7.mp4"),
    "after_achieving_something_without_doing_noting": os.path.join(working_dir, "video_templates/m8.mp4"),
    "guy_loosing_his_mental_stability": os.path.join(working_dir, "video_templates/m9.mp4"),
    "aaj_mood_nhi_hai_insta_srcoll_kar_leta_hu": os.path.join(working_dir, "video_templates/m10.mp4"),
    "guys_telling_stop_it_band_karo_i_request": os.path.join(working_dir, "video_templates/m11.mp4"),
    "guy_is_telling_tumse_nhi_ho_payega": os.path.join(working_dir, "video_templates/m12.mp4"),
    "cat_dancing_on_chipi_chipi_chappa_song": os.path.join(working_dir, "video_templates/m13.mp4"),
    "dedh_sau_rupyee_dega": os.path.join(working_dir, "video_templates/m14.mp4"),
    "guy_is_dancing_on_beelarina_dress_three_person_are_lauging": os.path.join(working_dir, "video_templates/m1.mp4"),
    "guy_telling_bhai_mere_saath_kya_horaha_hai_he_is_confused_what_is_happing_with_him": os.path.join(working_dir, "video_templates/m15.mp4"),
    "two_guys_are_shouthing_bhaut_jaga_hai_nhi_jaga_hai": os.path.join(working_dir, "video_templates/m16.mp4"),
    "harsh_beniwal_saying_samjh_rahe_ho_na_aap_meme": os.path.join(working_dir, "video_templates/m17.mp4"),
    "guy_is_telling_abba_nhi_manege": os.path.join(working_dir, "video_templates/m18.mp4"),
    "woman_haha": os.path.join(working_dir, "video_templates/m19.mp4"),
    "traumtized_cat_keep_her_hands_on_head": os.path.join(working_dir, "video_templates/m20.mp4"),
    "modi_dancing": os.path.join(working_dir, "video_templates/m21.mp4"),
    "guys_walking_in_attitude_hero_entry_in_south_moive": os.path.join(working_dir, "video_templates/m22.mp4"),
    "guys_is_saying_mujhe_chakka_ane_lage_hai": os.path.join(working_dir, "video_templates/m23.mp4"),
    "kitne_tejashvi_log_hai_modi_speaking": os.path.join(working_dir, "video_templates/m24.mp4"),
    "father_when_i_do_something_wrong": os.path.join(working_dir, "video_templates/m25.mp4"),
    "modi_with_meloni_guy_with_its_fav_women_meme": os.path.join(working_dir, "video_templates/m26.mp4"),
    "me_after_implementing_personilzed_meme_very_happy": os.path.join(working_dir, "video_templates/m5.mp4"),
    "me_after_seeing_crypto_portfolio_loss_ye_kya_horaha_sad": os.path.join(working_dir, "video_templates/m15.mp4"),
    "my_mind_after_24_hrs_hackathon": os.path.join(working_dir, "video_templates/m20.mp4"),
    "after_seeing_coffee_machine_in_hackathon_happy"  : os.path.join(working_dir, "video_templates/m13.mp4"),
    "inviligilator_after_evey_10_min_insta_scroll_kar_leta_hu": os.path.join(working_dir, "video_templates/m10.mp4"),
    "my_mind_before_every_exam_insta_scroll": os.path.join(working_dir, "video_templates/m10.mp4"),
}



def resize_image():
    # Read the image from the file
    input_image_path = INPUT
    output_image_path = INPUT
    scale_factor = 0.7
    img = cv2.imread(input_image_path)
    
    # Get original dimensions
    height, width = img.shape[:2]
    print(f"Original size: {width}x{height}")
    
    # Calculate new dimensions
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    print(f"Resized to: {new_width}x{new_height}")
    
    # Resize the image
    resized_img = cv2.resize(img, (new_width, new_height), interpolation = cv2.INTER_AREA)
    
    # Save the resized image
    cv2.imwrite(output_image_path, resized_img)
    
    return "Resized image saved successfully!"

