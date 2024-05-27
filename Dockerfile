FROM python:alpine

COPY requirements.txt ./

#install packages
RUN pip install -r requirements.txt

COPY api.py .

EXPOSE 5134
ENTRYPOINT ["python","api.py"] 