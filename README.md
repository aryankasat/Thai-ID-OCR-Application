# Thai-ID-OCR-Application

Welcome to the Thai ID OCR System! This project is designed to provide a solution for Optical Character Recognition (OCR) of Thai ID cards. The system includes a backend implemented in Python using Flask and MySQL as database. On the frontend, a simple HTML user interface interacts with the backend to upload images, view OCR results, and manage historical records.

## Backend
I have used Flask framework to along with Google Vision API for understand the images that are being uploaded. Apart from this I have used a database.py file containing the essential keys to connect to the MySQL database wherein all the CRUD operations are taking place.

### Folder Structure

- app.py - The main entry point for backend applications
- database.py - Configuration of database with the backend application and performing CRUD operations on the database
- ocr_processor.py - Configuration of the Google Vision API and extraction of the data from the scanned identity cards

## Database
I have used the MySQL database in order to store the required data. The schema for the database contains - An individual unique ID for each new user, Timestamp of updating the card to the database, status of the whether the update is successful or failed and json datatype storing the essential information of the user.

### API Endpoints

1. *Upload Image and perform OCR*
   - Endpoint - '/upload'
   - Method - 'POST', 'GET'
   - Description - It lets the user upload the image followed by extraction of essential information from the same.
     ![image](https://github.com/aryankasat/Thai-ID-OCR-Application/assets/33005008/5c148e0e-f28a-42cb-aec5-dc0d6d025f6b)

2. *Fetches the Filtered data based on the filters applied by the user*
   - Endpoint - '/history'
   - Method - 'POST', 'GET'
   - Description - It lets users filter the data based on the selection of his/her choice.
     ![image](https://github.com/aryankasat/Thai-ID-OCR-Application/assets/33005008/1f5a0ede-ba06-4152-b097-5cd5170237fe)

  
3. *Deleting data from the database*
    - Endpoint - '/delete'
    - Method - 'DELETE', 'POST','GET'
    - Description - It allows users to delete any instance from the database
      ![image](https://github.com/aryankasat/Thai-ID-OCR-Application/assets/33005008/4aa910f6-2279-4274-ad58-d2e17f860f28)

4. *Updating data in the database*
     - Endpoint - '/update'
     - Method - 'POST', 'GET'
     - Description - It allows users to update any query in the database
       ![image](https://github.com/aryankasat/Thai-ID-OCR-Application/assets/33005008/7182b875-f7c5-4d9b-9d6b-28257cfb86d7)

## Frontend
I have used separate HTML files for each page creating an entire new feel about for the user.

## Running the frontend 
1. Run ~~~pip install -r requirements.txt to install dependencies
2. Execute python app.py to start the Flask Development Server
3. Open your browser and navigate to http://127.0.0.1:5000 to view the application

## Deployment of the OCR System to Production
1. Used the Python Anywhere application to host the application
2. Run the ~~~pip3 install -r requirements --user to download the dependencies of the code
3. Use the application seamlessly on [https://ocridscanner.pythonanywhere.com]
