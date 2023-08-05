FROM python:3.8-slim

# Update and install common
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install web (server & framework)
RUN pip install --upgrade --no-cache-dir \
    gunicorn \
    flask

# Copy start executable (chmod +x)
COPY ./scripts/start.sh /start.sh

# Copy gunicorn_conf.py
COPY ./scripts/gunicorn_conf.py /gunicorn_conf.py

# Set working directory
WORKDIR /app/

# Copy main.py
COPY ./scripts/main.py main.py

# Run the start script
CMD ["/start.sh"]
