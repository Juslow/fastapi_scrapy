# Use a lightweight Python image as the base image
FROM python:3.10-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt /app

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app

ENV APPID=12ccdf79474e14750faf353df0a149dc
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=Dvw93)fw2M
ENV MYSQL_DB=test_db
ENV MYSQL_HOST=localhost

# Specify the command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
