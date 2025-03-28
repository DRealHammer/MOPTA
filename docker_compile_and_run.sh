#/bin/sh

# build the docker image and load it into the local images
docker buildx build --platform linux/amd64 -t mopta --load --no-cache .

# run the created container
docker run --platform=linux/amd64 -p 80:8501 -d --name mopta_service mopta



