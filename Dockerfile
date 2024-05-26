FROM python:alpine

COPY requirements.txt ./

#install packages
RUN pip install -r requirements.txt

#copy files in src
COPY src/ ./

CMD ["python api.py"]