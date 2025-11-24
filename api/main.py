import logging
import os
from io import BytesIO

import boto3
import qrcode
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Wczytanie zmiennych środowiskowych z .env
load_dotenv()

# Prosta konfiguracja logowania
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# CORS – dla lokalnego frontu (React np. na porcie 3000)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- AWS S3 CONFIG ---------------------------------------------------------

# Czytamy dane z .env
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY") or os.getenv("AWS_SECRET_KEY")
aws_region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")

# Tworzymy klienta S3
# Jeśli region jest ustawiony w AWS_REGION/AWS_DEFAULT_REGION, boto3 go wykorzysta.
s3_kwargs = {}
if aws_access_key_id and aws_secret_access_key:
    s3_kwargs["aws_access_key_id"] = aws_access_key_id
    s3_kwargs["aws_secret_access_key"] = aws_secret_access_key
if aws_region:
    s3_kwargs["region_name"] = aws_region

s3 = boto3.client("s3", **s3_kwargs)

bucket_name = "leszek-bucket"  # <- tutaj Twój bucket


# Helper: bezpieczna nazwa pliku z URL-a
def sanitize_url_for_filename(url: str) -> str:
    """
    Usuwa/problemowe znaki z URL-a, tak żeby nadawał się na nazwę pliku w S3.
    """
    unsafe_chars = [":", "/", "?", "&", "=", " ", "#"]
    safe = url
    for ch in unsafe_chars:
        safe = safe.replace(ch, "_")
    return safe


# --- ENDPOINT --------------------------------------------------------------


@app.post("/generate-qr/")
async def generate_qr(url: str):
    """
    Generuje QR z podanego URL-a, wrzuca PNG do S3
    i zwraca presigned URL do pobrania obrazka.
    """
    if not url:
        raise HTTPException(status_code=400, detail="Parameter 'url' is required")

    # 1. Generowanie kodu QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # 2. Zapis do pamięci (BytesIO)
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    # 3. Nazwa pliku w S3
    safe_name = sanitize_url_for_filename(url)
    file_name = f"qr_codes/{safe_name}.png"

    try:
        # 4. Upload do S3
        # Uwaga: nie używamy ACL, bo bucket ma ACL-e wyłączone (Bucket owner enforced).
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=img_byte_arr,
            ContentType="image/png",
        )

        # 5. Generowanie presigned URL (działa nawet przy prywatnym buckecie)
        s3_url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": file_name},
            ExpiresIn=3600,  # URL ważny 1h (możesz zmienić)
        )

        # Jeśli KONIECZNIE chcesz "stały" URL, to wygląda tak:
        # static_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        # ale wtedy musisz mieć publiczny bucket lub odpowiednią bucket policy.

        return {"qr_code_url": s3_url}

    except Exception as e:
        logging.exception("Error while uploading to S3")
        raise HTTPException(status_code=500, detail=str(e))
