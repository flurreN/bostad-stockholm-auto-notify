FROM selenium/standalone-chrome:108.0

RUN sudo apt-get update && sudo apt-get install -y \
  python3-pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY src/main.py main.py

CMD [ "python3", "./main.py" ]
