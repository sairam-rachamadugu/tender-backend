FROM python:3.12-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl unzip gnupg ca-certificates fonts-liberation libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Set display port for Selenium
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy your code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the app (replace main.py if different)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
