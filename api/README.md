# API Explanation:

## Dockerisation:

This command keeps things simple for building and running containers locally:

` docker build -t devops-qr-code-api . ; cd ../front-end-nextjs/; docker build -t devops-qr-code-frontend .; cd ../api/ ;docker run -d --name devops-qr-api -p 8000:80 devops-qr-code-api; cd ../front-end-nextjs/ ; docker run -d --name devops-qr-frontend -p 3000:3000 devops-qr-code-frontend`

This command tags the images and pushes them to the repo:

`
docker tag devops-qr-code-frontend:lastest vikramnayyar/devops-qr-code-frontend:latest

docker push vikramnayyar/devops-capstone-challenge:tagname
`

Build the images and then use those images to run the containers.

## Migration to GCP:

This project has been migrated from AWS to GCP.

The bucket and service account were <b>manually</b> created.

### GCP Service Account:

Provide the Storage Admin role.

Store Keys.json next to this file.

### Handling the Image Upload:

This article really simplified the process.
https://medium.com/@castanheira.it/gcp-how-to-upload-file-to-storage-simplest-as-possible-with-python-7534741d309
