# MOPTA/Dockerfile

#FROM python:3.9-slim
#FROM scipoptsuite/scipoptsuite:7.0.2
FROM --platform=linux/amd64 ubuntu:latest

WORKDIR /MOPTA

RUN apt-get update && apt-get install -y \
	build-essential \
	curl \
	software-properties-common \
	git \
	gcc \
	libblas3 \
	libboost-program-options1.83.0 \
	libboost-serialization1.83.0 \
	libc6 \
	libcliquer1 \
	libgfortran5 \
	libgmp10 \
	liblapack3 \
	libmetis5 \
	libopenblas0 \
	libstdc++6 \
	libtbb12 \
	python3-venv

COPY data .
COPY moptamodel.py .
COPY test.py .
COPY requirements.txt .

ADD https://www.scipopt.org/download/release/SCIPOptSuite-9.2.1-Linux-ubuntu24.deb . 
RUN dpkg -i SCIPOptSuite-9.2.1-Linux-ubuntu24.deb

#RUN tar xvzf scipoptsuite-9.2.1.tgz
#RUN cmake -C scipoptsuite-9.2.1

#ADD https://www.scipopt.org/download/release/SCIPOptSuite-9.2.1-Linux-ubuntu24.sh .
#RUN chmod +x ./SCIPOptSuite-9.2.1-Linux-ubuntu24.sh

#CMD ["/bin/bash"]

#RUN yes 'y' | ./SCIPOptSuite-9.2.1-Linux-ubuntu24.sh

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["python", "-m", "streamlit", "run", "test.py", "--server.port=8501", "--server.address=0.0.0.0"]
