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
RUN apt install libffi-dev libnacl-dev python3-dev ffmpeg -y

# pip req
COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

# copy files
COPY .env.sample .env
COPY . .

# run the bot
CMD ["python3","catbug_v2.py"]