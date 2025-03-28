#/bin/sh

# run the created container
docker run --platform=linux/amd64 -p 80:8501 -d --name mopta_service mopta



