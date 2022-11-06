# Base image
FROM python

RUN mkdir docker_dir
WORKDIR /docker_dir
COPY /deployment/* .

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
# CMD ["python", "app/app.py"]
ENTRYPOINT python app.py