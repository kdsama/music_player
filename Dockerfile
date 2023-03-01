FROM alpine:3.16
ENV DISPLAY=:0

# Install Python3 and PyQt5
RUN apk add --no-cache python3 py3-qt5 py3-pip
# Install xorg-server and xauth for interface display
RUN apk add --no-cache xorg-server xauth

COPY src /src
WORKDIR /src

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]