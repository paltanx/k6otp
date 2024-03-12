# Use an official Python runtime as a parent image
FROM arm64v8/python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Mangum for AWS Lambda compatibility (if you still need it for other purposes)

# Install system dependencies required for general operation
RUN apt-get update && apt-get install -y wget curl jq unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Fetch the latest k6 release for Linux x86_64 and unzip it
RUN wget "https://github.com/grafana/k6/releases/download/v0.49.0/k6-v0.49.0-linux-arm64.tar.gz" -O k6.tar.gz && \
    tar -xzf k6.tar.gz -C /usr/local/bin/ --strip-components=1 && \
    rm k6.tar.gz

# Define environment variable
ENV FASTAPI_ENV=development

# Amazon App Runner listens on port 8080
EXPOSE 8080

# Use uvicorn to serve the app on port 8080. Adapt the `main:app` to your application's entry point.
CMD ["uvicorn", "main:app","--port","8080", "--host", "0.0.0.0"]