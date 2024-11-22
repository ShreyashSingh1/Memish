from publitio import PublitioAPI
import os
from imgurpython import ImgurClient


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
    client_id = 'e838953025cdaad'
    client_secret = 'afd3762b18b5a300833fb64908ccdeef13202132'
    #client = ImgurClient(client_id, client_secret)
    #response = client.upload_from_path(path, anon=True)
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



TemplateMemeDescriptions = {
    "dragon": {
        "description": """This meme template is called the Three-headed Dragon meme, featuring three dragon heads where two are menacing, and one has a goofy, silly expression.
        Text Boxes (4 required):
        The two serious dragon heads represent something competent, intimidating, or efficient.
        The third goofy dragon head contrasts the other two, representing something that is silly, incompetent, or out of place.
        
        Text Breakdown:
        
        text_1: (Optional Heading or Comparison): Can be used to label the overall situation or the group being compared.
        text_2: (First Dragon - Left): Represents a strong, capable, or serious entity or characteristic.
        text_3: (Second Dragon - Middle): Represents another strong or capable entity or characteristic, similar to the first.
        text_4: (Third Dragon - Right): Represents something that is significantly less competent, often humorous or ridiculous in contrast.
        """,
        "number_of_texts": 4
    },
    "siper-man": {
        "description": """This is the Spider-Man pointing at Spider-Man meme template. It features three Spider-Men standing in a circle, pointing at each other, representing a situation where multiple parties are blaming or accusing each other for something, often humorously highlighting confusion or hypocrisy.
        Text Boxes (3 required):
        text_1: Represents Person/Group A who is blaming or accusing the others.
        text_2: Represents Person/Group B who is also blaming or accusing the others.
        text_3: Represents Person/Group C who, again, is blaming or accusing the others.
        Each character should be labeled to reflect the parties or entities involved in a confusing or hypocritical situation where everyone is accusing one another of the same thing.
        """,
        "number_of_texts": 3
    },
    "Scooby-Doo": {
        "description": """This is the classic Scooby-Doo villain reveal meme template. It features two panels:

        Top Panel:
        On the left, there is a tied-up villain wearing a mask.
        On the right, a hero (often Fred from Scooby-Doo) is pulling off the mask, revealing the villain's hidden identity.

        Bottom Panel:
        On the left, the villain’s true face is revealed, looking angry or surprised.
        On the right, the same hero is holding the removed mask, having exposed the villain’s real identity.

        Text Boxes (4 required):

        text_1: Top Panel - Villain (Left): 
        Label this as what the villain (or situation) appears to be at first glance, representing the false identity hidden behind the mask.

        text_2: Top Panel - Hero (Right): 
        Label this as the person doing the revealing, representing the hero who is exposing the truth.

        text_3: Bottom Panel - Villain's Face (Left): 
        Label this with the true identity that is revealed once the mask is removed, showing the real culprit or cause.

        text_4: Bottom Panel - Hero (Right): 
        Label this as the same hero who revealed the villain's face, now holding the mask after exposing the truth.

        This template is often used to show how something initially deceptive or misleading is revealed to be something unexpected or ironic when exposed.""",
        "number_of_texts": 4
    },
    "Epic Handshake": {
        "description": """This is the Epic Handshake meme template. It shows two muscular arms, one on the left and one on the right, locking hands in a strong handshake, symbolizing an agreement, shared opinion, or common ground between two different entities or groups.

        Text Boxes (3 required):

        text_1: Left Arm: Represents Person/Group A or Concept A (one party that shares a commonality with the other).

        text_2: Handshake (Center): Represents the shared belief, action, or agreement between the two parties (what unites them or the point of common ground).

        text_3: Right Arm: Represents Person/Group B or Concept B (the second party sharing a similar view or goal).

        This template is often used to show two seemingly unrelated groups bonding over a shared idea or value.""",
        "number_of_texts": 3
    },
    "Office Meeting": {
        "description": """This meme template consists of four panels, showing a typical office meeting scenario with an unexpected twist. There are 4 text boxes in total:

        text_1: Panel 1 (Top panel, single text box): 
        A manager is standing at the head of a meeting table, with a serious expression, addressing three people seated. The first text box is for what the manager is saying to introduce the topic or issue in the meeting.

        text_2: Panel 2 (Middle panel, three text boxes): 
        This panel shows the three seated people responding to the manager's statement from Panel 1:
            - First text box (left): The first person seated, raising a finger confidently, making a suggestion or giving an answer.
            - Second text box (middle): The second person, who is agreeing or adding something supportive to the first person's statement.
            - Third text box (right): The third person, leaning back casually, provides a comically unhelpful or absurd suggestion.

        text_3: Panel 3 (Lower left panel, no text box): 
        The manager looks visibly angry or frustrated after hearing the third person's response from the middle panel.

        text_4: Panel 4 (Lower right panel, no text box): 
        The third person who gave the absurd response is now being thrown out of the office building window. This is the visual punchline of the meme.

        In summary, the meme typically follows the structure of a serious situation, followed by escalating responses that culminate in a ridiculous or inappropriate suggestion that leads to the person being ejected from the meeting.""",
        "number_of_texts": 4
    },
    "The Rock Driving Reaction": {
        "description": """This meme template consists of three panels featuring a conversation between two characters inside a car. It has 2 text boxes:

        text_1: Panel 1 (Top panel, first text box): 
        The driver, played by Dwayne The Rock Johnson, is driving and looking towards the passenger, appearing confused or curious. The first text box is for what the driver is asking or saying, typically a question or comment that sets up the situation.

        text_2: Panel 2 (Middle panel, second text box): 
        The passenger (a blonde girl) is responding to the driver, usually saying something unexpected or shocking. The second text box captures the response or information that causes the punchline.

        text_3: Panel 3 (Bottom panel, no text box): 
        The driver (The Rock) is seen turning his head towards the passenger, now with a shocked or alarmed expression. This panel is the reaction to the passenger's response, providing the comedic punchline.

        In summary, this meme typically follows a structure where the driver asks a question or makes a statement, and the passenger replies with something surprising, leading to the driver’s exaggerated shocked reaction.""",
        "number_of_texts": 2
    },
    "Bus Perspective": {
        "description": """This meme depicts two people sitting on opposite sides of a bus. The person on the left looks sad and is facing a rocky, dull landscape outside the bus window. The person on the right is smiling and looking out at a bright, scenic view of mountains and a sunset. The meme is commonly used to illustrate different perspectives or attitudes towards the same situation.

        Text Boxes (2 required):
        
        text_1: Text Box 1 (Left side, above the sad person): 
        This should describe a negative or pessimistic viewpoint based on the context.
        
        text_2: Text Box 2 (Right side, above the happy person): 
        This should describe a positive or optimistic viewpoint in contrast to Text Box 1, based on the same context.

        Both texts should be tailored to the user's given scenario to show the contrast between two ways of viewing a situation.""",
        "number_of_texts": 2
    },
    "Reaction Shift": {
        "description": """This is a two-panel reaction meme showing a man initially looking happy and excited in the top image, but then transitioning to a shocked and disappointed expression in the bottom image. It’s often used to represent someone’s reaction to an unexpected disappointment.

        Text Boxes (2 required):
        
        text_1: Text Box 1 (Top panel, next to the happy face): 
        This should describe something positive or exciting that initially causes joy or excitement based on the given context.
        
        text_2: Text Box 2 (Bottom panel, next to the disappointed face): 
        This should describe the twist or unexpected negative outcome that causes the disappointment, following up from Text Box 1 in the given scenario.

        The two text boxes should relate to each other to represent a shift from excitement to disappointment.""",
        "number_of_texts": 2
    },
    "Blue Button Reaction": {
        "description": """This meme template shows a hand slamming down on a large blue button with urgency. It is typically used to represent an impulsive or enthusiastic reaction to something someone strongly desires or agrees with.

        Text Boxes (2 required):
        
        text_1: Text Box 1 (Above the button): 
        This should describe the situation, action, or idea that triggers a strong, immediate reaction or impulse from the user.
        
        text_2: Text Box 2 (On or near the button): 
        This should describe the action or statement that the user is excitedly reacting to, usually in an exaggerated or humorous way.

        The text should convey the urgency and enthusiasm surrounding the situation being represented.""",
        "number_of_texts": 2
    },
    "Drake Hotline Bling": {
        "description": """This is the popular "Drake Hotline Bling" meme template, which consists of two panels featuring the rapper Drake.

        Top Panel: Drake is rejecting something with a disgusted expression and raised hand, signaling disapproval.
        Bottom Panel: Drake is smiling and pointing, showing approval or preference for something else.

        Text Boxes (2 required):
        
        text_1: Text 1 (Top Panel): The option or idea that is being rejected or disliked.
        text_2: Text 2 (Bottom Panel): The alternative option or idea that is being preferred or approved.""",
        "number_of_texts": 2
    }
}
