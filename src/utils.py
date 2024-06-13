import requests
import os

# GEN_KEY = "AIzaSyCEDJ1aaSEGimwoSgF-bSNY2PP4i-j4_Kc"
GEN_KEY = "AIzaSyBa5b8ZuK83ehPi52ua4Ly724ofJHTT5Zk"

current_directory = os.getcwd()
INPUT = os.path.join(current_directory, "artifacts", "Input.jpg")
OUTPUT = os.path.join(current_directory, "artifacts", "output.jpg")
OUTPUT_VEDIO = os.path.join(current_directory, "artifacts", "output_video.mp4")
OUTPUT_MEME = os.path.join(current_directory, "artifacts", "output_meme.jpg")

def savenft(path):

    with open(path, "rb") as f:
        image_data = f.read()

    # Create FormData-like object
    files = {"file": ("filename.jpg", image_data)}  # Adding the filename here

    # Define headers (without Content-Type)
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDRCOWM5Q0UwQmE3NENiRjA4QkJlZjIwNDMzZEUwYjczNzUxNjI4RTgiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY5ODUwNDQ1NzM3MywibmFtZSI6IkZ1bmRFVEgifQ.JxTH4iRtScscfmb9mvZqhSqF9MKs2b0JJS2yof7hzF4",
    }

    # Make the request
    response = requests.post(
        "https://api.nft.storage/upload", files=files, headers=headers
    )

    cid = response.json()["value"]["cid"]

    value = f"https://{cid}.ipfs.nftstorage.link/filename.jpg"

    return value

def savenft1(path):
    with open(path, "rb") as f:
        file_data = f.read()

    # Create FormData-like object
    files = {"file": ("filename.mp4", file_data, "video/mp4")}

    # Define headers (without Content-Type)
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDRCOWM5Q0UwQmE3NENiRjA4QkJlZjIwNDMzZEUwYjczNzUxNjI4RTgiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY5ODUwNDQ1NzM3MywibmFtZSI6IkZ1bmRFVEgifQ.JxTH4iRtScscfmb9mvZqhSqF9MKs2b0JJS2yof7hzF4",
    }

    # Make the request
    response = requests.post(
        "https://api.nft.storage/upload", files=files, headers=headers
    )

    # Check if the request was successful
    if response.status_code == 200:
        cid = response.json()["value"]["cid"]
        value = f"https://{cid}.ipfs.nftstorage.link/filename.mp4"
        return value
    else:
        response.raise_for_status()

template_paths = {
    "aerial_view_of_a_car_driving_down_a_road_in_the_middle_of_a_forest_1": "c:/Users/shrey/OneDrive/Desktop/Memish/notebooks/Templates/aerial_view_of_a_car_driving_down_a_road_in_the_middle_of_a_forest_1.jpg",
}