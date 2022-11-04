# Base image
FROM python:3.10
EXPOSE 5001

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


RUN mkdir /app
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
#ENTRYPOINT ["gunicorn", "-b", "http://127.0.0.1:8000", "--access-logfile", "-", "--error-logfile", "-", "--timeout", "120"]
CMD ["python", "app/app.py"]