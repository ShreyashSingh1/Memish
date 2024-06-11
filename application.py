from flask import Flask, request
from flask_cors import CORS
from src.logger import logging
from src.pipeline import Genrate
import src.utils as utils
import cv2

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

if __name__ == "__main__":
    app.run(host="0.0.0.0")
