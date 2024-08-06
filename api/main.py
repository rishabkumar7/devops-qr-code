from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import qrcode
import os
from io import BytesIO
from google.cloud import storage

# Loading Environment variable (AWS Access Key and Secret Key)
from dotenv import load_dotenv
load_dotenv()

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the KEYS.json file
credential_path = os.path.join(current_directory, 'KEYS.json') #Service Account in GitIgnore.
# Set the environment variable for Google Cloud authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

app = FastAPI()

# Allowing CORS for local testing
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GCP Configuration Todo
storage_client = storage.Client()
bucket_name = 'devops-capstone-challenge-bucket' # Add your bucket name here

@app.post("/generate-qr/")
async def generate_qr(url: str):
    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR Code to BytesIO object
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Generate file name for GCP
    file_name = f"qr_codes/{url.split('//')[-1]}.png"

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_file(img_byte_arr, content_type='image/png')

        # Generate the GCP URL
        gcp_url = f"https://storage.googleapis.com/devops-capstone-challenge-bucket/{file_name}"
        return {"qr_code_url": gcp_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    