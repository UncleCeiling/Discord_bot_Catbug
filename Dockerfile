# Set Python version for the container
ARG PYTHON_VER=3.13.5

# Build in two stages to install deps without the project
FROM python:${PYTHON_VER}-slim-bullseye as base

# Set Python specific env-vars 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# env requirements
RUN apt update -y && apt upgrade -y
RUN apt install libffi-dev -y
RUN apt install libnacl-dev -y
RUN apt install python3-dev -y
RUN apt install ffmpeg -y 
RUN python3 -m pip install --upgrade pip

FROM base AS build

# Sets the working directory for this stage
WORKDIR /app

# copy project files and install the required modules
COPY . .
RUN python3 -m pip install -r requirements.txt

# run the bot
CMD ["python3","catbug_v2.py"]