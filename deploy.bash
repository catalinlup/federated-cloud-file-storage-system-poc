#!/bin/bash


IMAGE_BASE_NAME=europe-west1-docker.pkg.dev/helical-bonsai-380311/federated-google-cloud
VERSION_NUMBER="v0.0.1"
ARG_LIST=$@
COMMAND="$1"
TARGET=central-service
FILEPATH=central_service



function build() {
 
    docker build --build-arg env_file=.env -t $IMAGE_BASE_NAME/$TARGET:$VERSION_NUMBER -f ./$FILEPATH/Dockerfile ./$FILEPATH
   
}

function push() {
    docker push $IMAGE_BASE_NAME/$TARGET:$VERSION_NUMBER
}

function deploy() {
    gcloud run deploy $TARGET --image $IMAGE_BASE_NAME/$TARGET:$VERSION_NUMBER --region europe-west1 --allow-unauthenticated --min-instances=0 --cpu=1 --memory=1Gi
}

build
echo "Service built"

push
echo "Service pushed"

deploy
echo "Service deployed"



