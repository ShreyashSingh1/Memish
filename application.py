from flask import Flask, request, jsonify
from flask_cors import CORS
from src.logger import logging
from src.pipeline import Genrate
import src.utils as utils
from src.pipeline.genrate_video import VedioGenerator

app = Flask(__name__)
CORS(app)

# Initialize the generators
draw = Genrate.Gen()
meme_generator = Genrate.MemeGenerator(utils.GEN_KEY, utils.template_paths)
meme_gen1 = VedioGenerator(utils.GEN_KEY, utils.template_video_paths)


@app.route("/imgen", methods=["POST"])
def make_image():
    try:
        data = request.json
        toptext, bottomtext = draw.genimg(data["prompt"], normal=True)
        logging.info("Image generated successfully!")
        link = draw.drawimage(toptext, bottomtext, normal=True)
        return jsonify({"link": link})
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        return jsonify({"error": "Error generating image"}), 500


@app.route("/uploadphoto", methods=["POST"])
def upload_photo():
    try:
        image = request.files["image"]
        image.save(utils.INPUT)
        logging.info("Generating custom image meme!")
        link = draw.drawimage(top_text=" ", bottom_text=" ", photo=True)
        logging.info("Custom image meme generation successful!")
        return jsonify({"link": link})
    except Exception as e:
        logging.error(f"Error uploading photo: {e}")
        return jsonify({"error": "Error uploading photo"}), 500


@app.route("/imgen1", methods=["POST"])
def generate_anime_image():
    try:
        data = request.json
        top_text, bottom_text = draw.genimg(data["prompt"], animate=True)
        logging.info("Anime image generated successfully!")
        link = draw.drawimage(top_text, bottom_text)
        return jsonify({"link": link})
    except Exception as e:
        logging.error(f"Error generating anime image: {e}")
        return jsonify({"error": "Error generating anime image"}), 500


@app.route("/template", methods=["POST"])
def create_template_meme():
    try:
        data = request.json
        link = meme_generator.create_meme(data["prompt"])
        logging.info("Template meme generated successfully!")
        return jsonify({"link": link})
    except Exception as e:
        logging.error(f"Error creating template meme: {e}")
        return jsonify({"error": "Error creating template meme"}), 500


@app.route("/video", methods=["POST"])
def create_video_meme():
    try:
        data = request.json
        logging.info("Generating video meme!")
        link = meme_gen1.create_video_meme(data["prompt"], utils.OUTPUT_VEDIO)
        logging.info("Video meme generation successful!")
        return jsonify({"link": link})
    except Exception as e:
        logging.error(f"Error generating video meme: {e}")
        return jsonify({"error": "Error generating video meme"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
