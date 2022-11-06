# Base image
FROM python:3.10

RUN mkdir docker_dir
WORKDIR /docker_dir
COPY /requirements.txt .
COPY /app.py .
COPY /model.pkl .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the application
# CMD ["python", "app/app.py"]
ENTRYPOINT python app.py