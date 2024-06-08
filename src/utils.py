import requests
import os

current_directory = os.getcwd()
INPUT = os.path.join(current_directory, "artifacts", "Input.jpg")
OUTPUT = os.path.join(current_directory, "artifacts", "output.jpg")


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
