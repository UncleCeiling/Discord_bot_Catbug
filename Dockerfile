ARG PYTHON_VER=3.13.5
FROM python:${PYTHON_VER}-slim

# Prevent `pyc` files.
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent lost logs.
ENV PYTHONUNBUFFERED=1

# Sets the working directory for the rest of the Dockerfile
WORKDIR /catbug_bot

# apt req
RUN apt update -y
RUN apt upgrade -y
RUN apt install libffi-dev -y
RUN apt install libnacl-dev -y
RUN apt install python3-dev -y
RUN apt install ffmpeg -y

# pip req
RUN python3 -m pip install --upgrade pip
COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt

# copy files
COPY .env.sample .env
COPY . .

# run the bot
CMD ["python3","catbug_v2.py"]