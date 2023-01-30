# Use the official Python image as the base image
FROM python:3.10.0

# Set the working directory in the image
WORKDIR /app

# Copy the requirements file to the image
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code to the image
COPY . .

# Set the environment variable for the application
ENV PORT=8000

# Expose the application port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
