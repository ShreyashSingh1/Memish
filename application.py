from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from src.logger import logging
from src.pipeline import Genrate
import src.utils as utils
from pathlib import Path
from src.pipeline.genrate_video import VedioGenerator, VideoMeme
app = Flask(__name__)
CORS(app)

draw1 = Genrate.GenPhoto()
meme_generator = Genrate.MemeGenerator(utils.GEN_KEY, utils.template_paths)
meme_gen1 = VedioGenerator(utils.GEN_KEY, utils.template_video_paths, utils.FONT)
meme_gen2 = VideoMeme(utils.GEN_KEY, utils.FONT)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")
    
    
@app.route("/text-to-image-gen-meme", methods=["POST"])
def make_image():
    try:
        data = request.json
        toptext, bottomtext = draw1.genimg(data["prompt"], normal=True)
        print(toptext, bottomtext)
        logging.info("Image generated successfully!")
        link_preview, link_download = draw1.drawimage(toptext, bottomtext, normal=True)
        return jsonify({"link_preview": link_preview, "link_download": link_download})
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        return jsonify({"error": "Error generating image"}), 500


@app.route("/text-to-anime-image-gen-meme", methods=["POST"])
def generate_anime_image():
    try:
        data = request.json
        top_text, bottom_text = draw1.genimg(data["prompt"], animate=True)
        logging.info("Anime image generated successfully!")
        link_preview, link_download = draw1.drawimage(top_text, bottom_text)
        return jsonify({"link_preview": link_preview, "link_download": link_download})
    except Exception as e:
        logging.error(f"Error generating anime image: {e}")
        return jsonify({"error": "Error generating anime image"}), 500   
    
    
@app.route("/upload-photo-to-meme", methods=["POST"])
def upload_photo():
    try:
        image = request.files["image"]
        data = request.form["prompt"]
        print(data)
        image.save(utils.INPUT)
        logging.info("Generating custom image meme!")
        link_preview, link_download = draw1.drawimage(top_text=" ", bottom_text=" ", photo=True, prompt=data)
        logging.info("Custom image meme generation successful!")
        return jsonify({"link_preview": link_preview, "link_download": link_download})
    except Exception as e:
        logging.error(f"Error uploading photo: {e}")
        return jsonify({"error": "Error uploading photo"}), 500


@app.route("/upload-video-to-meme", methods=["POST"])
def upload_video():
    try:
        image = request.files["video"]
        data = request.form["prompt"]
        print(data)
        image.save(utils.VIDEOMEMEPATH)
        # utils.resize_image()
        logging.info("Generating custom image meme!")
        link_preview, link_download = meme_gen2.create_video_meme(data, utils.VIDEOMEMEPATH, utils.VIDEOMEMEPATHOUT)
        logging.info("Custom image meme generation successful!")
        return jsonify({"link_preview": link_preview, "link_download": link_download})
    except Exception as e:
        logging.error(f"Error uploading photo: {e}")
        return jsonify({"error": "Error uploading Video"}), 500
    
        
@app.route("/text-to-template-meme", methods=["POST"])
def create_template_meme():
    try:
        data = request.json
        link_preview, link_download = meme_generator.create_meme(data["prompt"], utils.FONT, 120)
        logging.info("Template meme generated successfully!")
        return jsonify({"link_preview": link_preview, "link_download": link_download})
    except Exception as e:
        logging.error(f"Error generating meme: {e}")
        return jsonify({"error": "Error generating anime image"}), 500


@app.route("/text-to-video-meme", methods=["POST"])
def create_video_meme():
    try:
        data = request.json
        logging.info("Generating video meme!")
        link_preview, link_download = meme_gen1.create_video_meme(data["prompt"], utils.OUTPUT_VEDIO)
        logging.info("Video meme generation successful!")
        return jsonify({"link_preview": link_preview, "link_download": link_download})
    except Exception as e:
        logging.error(f"Error generating video meme: {e}")
        return jsonify({"error": "Error generating video meme"}), 500
    
    
@app.route("/uploadimage", methods=["POST"])
def upload_image():
    try:
        image = request.files["image"]
        file_extension = Path(image.filename).suffix
        image.save(utils.UPLOAD + "\\" + f"upload{file_extension}")
        logging.info("Generating custom image meme!")
        link_preview, link_download = utils.savenft(utils.UPLOAD + "\\" + f"upload{file_extension}")
        return jsonify({"link_preview": link_preview, "link_download": link_download})
    except Exception as e:
        logging.error(f"Error uploading image: {e}")
        return jsonify({"error": "Error uploading image"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
