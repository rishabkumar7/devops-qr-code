# devops-qr-code

This is the sample application for the DevOps Capstone Project.
It generates QR Codes for the provided URL, the front-end is in NextJS and the API is written in Python using FastAPI.

## Application

**Front-End** - A web application where users can submit URLs.

**API**: API that receives URLs and generates QR codes. The API stores the QR codes in cloud storage(AWS S3 Bucket).

## Running locally

### API

The API code exists in the `api` directory. You can run the API server locally:

- Clone this repo
- Create a AWS User with AmazonS3FullAccess 
- Create a S3 Bucket and select ACL enable for public access, Uncheck block bucket.
- Make sure you are in the `api` directory
- Create a virtualenv by typing in the following command: `python3 -m venv .venv`
- Run command `source .venv/bin`
- Run command `source .venv/bin/activate`
<<<<<<< HEAD
- Install the required packages: `pip install -r requirements.txt` 'or pip install fastapi uvicorn boto3 python-dotenv pytest qrcode' 
=======
- Install the required packages: `pip install -r requirements.txt` or `pip install fastapi uvicorn boto3 python-dotenv pytest qrcode`
>>>>>>> 9db5a81 (Moved Terraform files into the infrastructure folder)
- Create a `.env` file, and add you AWS Access and Secret key, check  `.env.example`
- and Save the Access & secret key, cat the `.env` to verify. 
- Also, change the BUCKET_NAME to your S3 bucket name in `main.py`
- Run the API server: `uvicorn main:app --reload`
- Your API Server should be running on port `http://localhost:8000`

### optional- Troubleshoting S3 bucket
### you might add Bucket policy 

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"  # Add bucket name 
        }
    ]
}


### Front-end

The front-end code exits in the `front-end-nextjs` directory. You can run the front-end server locally:

- Clone this repo
- Make sure you are in the `front-end-nextjs` directory
- Install the dependencies: `npm install`
- Run the NextJS Server: `npm run dev`
- Your Front-end Server should be running on `http://localhost:3000`


## Goal

The goal is to get hands-on with DevOps practices like Containerization, CICD and monitoring.

Look at the capstone project for more detials.

## Author

[Rishab Kumar](https://github.com/rishabkumar7)

## License

[MIT](./LICENSE)
