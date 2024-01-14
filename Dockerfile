FROM python:3
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /
EXPOSE 8000