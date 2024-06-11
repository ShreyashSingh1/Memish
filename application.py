from flask import Flask, request
from flask_cors import CORS
from src.logger import logging
from src.pipeline import Genrate
import src.utils as utils
import cv2
from src.pipeline.genrate_video import VedioGenerator

app = Flask(__name__)
CORS(app)

draw = Genrate.Gen()
meme_generator = Genrate.MemeGenerator(utils.GEN_KEY, utils.template_paths)

@app.route("/imgen", methods=["POST"])
def makeimage():

    data = request.json

    value = draw.genimg(data["prompt"], normal=True)

    logging.info("Image generated successfully!")

    link = draw.drawimage(value, normal=True)

    return link


@app.route("/uploadphoto", methods=["POST"])
def upload():

    image = request.files["image"]
    image.save(utils.INPUT)

    logging.info("Genrating custom image meme!")

    link = draw.drawimage(text1=" ", photo=True)

    logging.info("Genrating custom image meme successful!")

    return link


@app.route("/imgen1", methods=["POST"])
def anime():

    data = request.json

    value = draw.genimg(data["prompt"], animate=True)

    logging.info("Image generated successfully!")

    link = draw.drawimage(value)

    return link

@app.route("/template", methods=["POST"])
def template():
    
    data = request.json
    data["prompt"] 
    print(data)
    meme = meme_generator.create_meme(data["prompt"])
    cv2.imwrite("C:/Users/shrey/OneDrive/Desktop/Memish/artifacts/output_meme.jpg", meme)
    link = utils.savenft("C:/Users/shrey/OneDrive/Desktop/Memish/artifacts/output_meme.jpg")

    return link


@app.route("/video", methods=["POST"])
def video():

    data = request.json

    logging.info("Genrating video meme!")

    template_paths = {
        "guy_is_dancing_three_person_are_laughing": "C:/Users/shrey/OneDrive/Desktop/Memish/Vedio_Templates/laal_kabutar_meme_cat_is_dancing_three_cockroach_are_laughing_Oggy_and_cockroach.mp4",
        "modi_saying_kya_re_bete_tujhe_thakan_nhi_lag_rahi_kya": "C:/Users/shrey/OneDrive/Desktop/Memish/Vedio_Templates/modi_saying_kya_re_bete_tujhe_thakan_nhi_lag_rahi_kya.mp4",
        "two_kids_are_running_after_seeing_something": "C:/Users/shrey/OneDrive/Desktop/Memish/Vedio_Templates/two_kids_are_running_after_seeing_something.mp4",
        "one_eternity_later":"C:/Users/shrey/OneDrive/Desktop/Memish/Vedio_Templates/one_eternity_later.mp4"
    }
    meme_gen1 = VedioGenerator("AIzaSyBa5b8ZuK83ehPi52ua4Ly724ofJHTT5Zk", template_paths)
    output_path = "output_video.mp4"
    meme_gen1.create_video_meme(data["prompt"], output_path)
    
    link = utils.savenft1("output_video.mp4")

    logging.info("Genrating video meme successful!")

    return link

if __name__ == "__main__":
    app.run(host="0.0.0.0")
