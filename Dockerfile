FROM python:alpine

COPY requirements.txt ./

#install packages
RUN pip install -r requirements.txt

COPY api.py .

EXPOSE 9000
ENTRYPOINT ["python","api.py"] 