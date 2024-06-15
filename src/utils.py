import requests
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


publitio_api = PublitioAPI(key=api_key , secret=api_secret)

def savenft(path):
    data = publitio_api.create_file(file=open(path, 'rb'),
                         title='My title',
                         description='My description')
        
    return data['url_preview'], data['url_download']

template_paths = {
    "aerial_view_of_a_car_driving_down_a_road_in_the_middle_of_a_forest_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/aerial_view_of_a_car_driving_down_a_road_in_the_middle_of_a_forest_1.jpg",
}

# Template paths dictionary with dynamic paths based on the working directory
template_video_paths = {
    "guy_is_dancing_three_person_are_laughing": os.path.join(working_dir, "video_templates/m1.mp4"),
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
    "guy_is_teling_tumse_nhi_ho_payega": os.path.join(working_dir, "video_templates/m12.mp4"),
    "cat_dancing_on_chipi_chipi_chappa_song": os.path.join(working_dir, "video_templates/m13.mp4"),
    "dedh_sau_rupyee_dega": os.path.join(working_dir, "video_templates/m14.mp4"),
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
    "guy_getting_slaaped_in_differnt_time_lapps": os.path.join(working_dir, "video_templates/m25.mp4"),
    "guys_with_his_fav_girl": os.path.join(working_dir, "video_templates/m26.mp4")
}
