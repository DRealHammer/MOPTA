# MOPTA 2025 Transavia Retraining Scheduling Problem

This is my solution for the [MOPTA Competition 2025](https://coral.ise.lehigh.edu/mopta2025/competition/). The problem is about retraining Boeing crews to new Airbus planes. As there are a lot of specifications and restrictions, this requires a modeling approach of some sort.
With this submission, there is not only an optimal result via [SCIP](https://www.scipopt.org) in terms of minimizing the cost, but also an interactive Dashboard for live editing and exporting data from the optimization suite via [Streamlit](https://streamlit.io/). For further interpretation, there are also some graphs, that display the core information of the solution found. Solutions are stored in the live session until reload.


## Installation on x86 Architecture

### Setup

```bash
# create a virtual environment
python -m venv .venv

# activate the env
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

### Run Application

```
# run on port 80 in the background
streamlit run main.py --server.port 80 &
```

If you want to stop the server

```bash
fg
```

and press CTRL + C

### Running in Docker

If you want to create a container for this application, you can roughly follow the steps outlined for ARM.
You can also remove the forced amd architecture in the Dockerfile in the FROM statement.

Advice: The optimization algorithm benefits a lot from running on multicore machines. Consider specifying a --cpus 4 statement, to give your container more CPU acces at runtime.


## 🛠  Build & Run on ARM Architecture

### Install Dependencies
```bash
# Install Docker
sudo apt install docker
```

### Install QEMU for multi-architecture support
```bash
sudo apt install -y qemu-user-static
```

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

Disclaimer: I do not guarantee that the solutions created by the software are always accurate and should in every case be double checked for plausibilty before any decision is made.
