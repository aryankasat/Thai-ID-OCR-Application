import google.cloud.vision 
from google.cloud.vision_v1 import types
import json,os


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'google_credentials.json'


#processing of the image which the user has uploaded
def process_ocr(image_content):

    #configuring the Google Vision API
    client = google.cloud.vision.ImageAnnotatorClient()
    image = types.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        ocr_result = {
            "id_number": None,
            "name": None,
            "last_name": None,
            "date_of_birth": None,
            "date_of_issue": None,
            "date_of_expiry": None,
        }

        # Extracting relevant information (you may need to adjust this based on the actual OCR response structure)
        for text in texts:
            if "ID" in text.description:
                ocr_result["id_number"] = text.description.split("ID")[1].strip()
            if "Name" in text.description:
                ocr_result["name"] = text.description.split("Name")[1].strip()
            if "Last_Name" in text.description:
                ocr_result["last_name"] = text.description.split("Last_Name")[1].strip()
            if "Date_of_Birth" in text.description:
                ocr_result["date_of_birth"] = text.description.split("Date_of_Birth")[1].strip()
            if "Date_of_Issue" in text.description:
                ocr_result["date_of_issue"] = text.description.split("Date_of_Issue")[1].strip()
            if "Date_of_Expiry" in text.description:
                ocr_result["date_of_expiry"] = text.description.split("Date_of_Expiry")[1].strip()

        return ocr_result
    else:
        raise Exception("OCR processing failed")
