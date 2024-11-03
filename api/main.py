from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import qrcode
import boto3
import os
from io import BytesIO
from azure.storage.blob import BlobServiceClient, ContentSettings

# Loading Environment variable (AWS Access Key and Secret Key)
from dotenv import load_dotenv
load_dotenv()

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

# Supported Options - AWS/AZURE (Default: AWS)
CLOUD_PROVIDER = os.getenv("CLOUD_PROVIDER")

if CLOUD_PROVIDER == "AZURE":
    # Azure Blob Storage Configuration
    """    
    Create a Storage Account and container in Azure
    Ensure anonymous access is available for blob containers (Settings > Configuration > Allow Blob anonymous access)
    Enable anonymous access (Select the blob container > Change Access Level > Blob)
    Edit the container name below and add the connection string in the .env (Found in Access Keys of the Storage Account)
    """

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = 'qrcodes'  # Add your container name here

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
else:
    # AWS S3 Configuration
    s3 = boto3.client(
        's3',
        aws_access_key_id= os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key= os.getenv("AWS_SECRET_KEY"))

    bucket_name = 'YOUR_BUCKET_NAME' # Add your bucket name here
    
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

    # Generate file name for S3
    file_name = f"qr_codes/{url.split('//')[-1]}.png"

    try:
        if CLOUD_PROVIDER == "AZURE":
           # Upload to Azure Blob Storage
            blob_client = container_client.get_blob_client(file_name)
            
            # Use ContentSettings to specify content type
            content_settings = ContentSettings(content_type="image/png")
            
            blob_client.upload_blob(img_byte_arr, blob_type="BlockBlob", content_settings=content_settings, overwrite=True)
            
            # Generate the Blob URL
            blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{file_name}"
            return {"qr_code_url": blob_url}
        else:
             # Upload to S3
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=img_byte_arr, ContentType='image/png', ACL='public-read')
            
            # Generate the S3 URL
            s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
            return {"qr_code_url": s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    