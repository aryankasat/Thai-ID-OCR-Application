from google.cloud import vision
import os,io



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"google_credentials.json"

#processing of the image which the user has uploaded
def process_ocr(filename):

    #configuring the Google Vision API
    client = vision.ImageAnnotatorClient()
    path = "static/"+filename
    with io.open(path,'rb') as image_file:
        content =image_file.read()
    image = vision.Image(content = content)

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
        ocr_result["id_number"] = texts[0].description[42:59]
        ocr_result["name"] = texts[0].description[145:159]
        ocr_result["last_name"] = texts[0].description[170:178]
        ocr_result["date_of_birth"] = texts[0].description[218:230]
        ocr_result["date_of_issue"] = texts[0].description[332:344]
        ocr_result["date_of_expiry"] = texts[0].description[428:440]
        return ocr_result
    else:
        raise Exception("OCR processing failed")
