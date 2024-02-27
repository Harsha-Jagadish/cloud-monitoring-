#Lets get the required python image from docker website
FROM python:3.9-slim-buster 

# current working directory in container
WORKDIR /app

# lets copy the requirements text file to the container
COPY requirements.txt .

# Install gcc, Python dev packages, and other dependencies Python Packages with Native Extensions: Some Python packages, like psutil, rely on native extensions written in C or C++
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    # Add any other dependencies you might need
    && rm -rf /var/lib/apt/lists/*

# Install the requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy app files to the container
COPY . . 

# Provide env variablef for flask
ENV FLASK_RUN_HOST=0.0.0.0

# Port for flask
EXPOSE 5000

# Start flask app when container is run 
CMD ["flask", "run", "--host=0.0.0.0"]

