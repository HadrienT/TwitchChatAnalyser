# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY ./requirements.txt .
COPY ./wait-for-it.sh .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x ./wait-for-it.sh

COPY . .

CMD ["./wait-for-it.sh", "postgres:5432", "--", "python", "app.py"]
