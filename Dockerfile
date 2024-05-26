FROM python:alpine

COPY requirements.txt ./

#install packages
RUN pip install -r requirements.txt

#ENV OPENAI_API_KEY= an open ai key (should use secrets in prod")
#copy files in src
COPY src/ ./

ENTRYPOINT ["python","api.py"] 