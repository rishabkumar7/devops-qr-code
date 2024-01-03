from fastapi import FastAPI, HTTPException
import qrcode
import boto3
from io import BytesIO

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# AWS S3 Configuration
s3 = boto3.client('s3')
bucket_name = 'qrcode-storage-devops-capstone'

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
        # Upload to S3
        s3.upload_fileobj(img_byte_arr, bucket_name, file_name)
        
        # Generate the S3 URL
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        return {"qr_code_url": s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    