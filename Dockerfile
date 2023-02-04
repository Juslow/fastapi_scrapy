# Use a lightweight Python image as the base image
FROM python:3.10-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt /app

# Install the necessary libraries for building and linking
RUN apk add --no-cache mariadb-dev gcc musl-dev python3-dev

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app

# Specify the command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
