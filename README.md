## 🛠 Build & Run on ARM Architecture

### Install Dependencies
```bash
# Install Docker
sudo apt install docker
```

# Install QEMU for multi-architecture support
sudo apt install -y qemu-user-static

### Set Up Buildx
```bash
# Create and use multi-architecture builder
docker buildx create --name multiarch --use
```

### Build Docker Image
```bash
# Build for AMD64 architecture (from ARM host)
docker buildx build --platform linux/amd64 -t mopta --load --no-cache .
```

### Run Container
```bash
# Start container with AMD64 emulation
docker run --platform=linux/amd64 -p 80:8501 -d mopta
```
