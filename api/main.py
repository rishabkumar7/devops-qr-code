from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import qrcode
from supabase import create_client, Client
import os
from io import BytesIO

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Configuration (înlocuiește AWS S3)
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
    
)

bucket_name = "qr-codes"  # numele bucket-ului creat în Supabase

@app.post("/generate-qr/")
async def generate_qr(url: str):
    # Generare QR Code (identic cu originalul)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Nume fișier în bucket
    file_name = f"{url.split('//')[-1]}.png"

    try:
        # Upload pe Supabase Storage (înlocuiește s3.put_object)
        supabase.storage.from_(bucket_name).upload(
            path=file_name,
            file=img_byte_arr.getvalue(),
            file_options={"content-type": "image/png", "upsert": "true"}
        )

        # Generare URL public
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
        return {"qr_code_url": public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))