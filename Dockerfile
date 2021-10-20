
##python base image
FROM python:3.7.8-slim

#defining present work directory
WORKDIR /google-landmark
# Copy contents into the working directory
ADD . /google-landmark
##install dependencies
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]