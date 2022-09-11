FROM python:3.10
WORKDIR /zmall_rest

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
