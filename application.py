from flask import Flask, request
from flask_cors import CORS
from src.logger import logging
from src.pipeline import Genrate
import src.utils as utils
from src.pipeline.genrate_video import VedioGenerator

app = Flask(__name__)
CORS(app)


draw = Genrate.Gen()
meme_generator = Genrate.MemeGenerator(utils.GEN_KEY, utils.template_paths)
meme_gen1 = VedioGenerator(utils.GEN_KEY, utils.template_video_paths)


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
    link = meme_generator.create_meme(data["prompt"])
    return link


@app.route("/video", methods=["POST"])
def video():

    data = request.json

    logging.info("Genrating video meme!")

    link = meme_gen1.create_video_meme(data["prompt"], utils.OUTPUT_VEDIO)
    
    logging.info("Genrating video meme successful!")

    return link

if __name__ == "__main__":
    app.run(host="0.0.0.0")
