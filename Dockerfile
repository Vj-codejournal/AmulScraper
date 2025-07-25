FROM python:3.9-slim

# Install Chrome, ChromeDriver, and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    libgl1 \
    chromium-driver \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 scraper && chown -R scraper:scraper /app
USER scraper

# Copy requirements and install Python dependencies
COPY --chown=scraper:scraper requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Add user's pip bin to PATH
ENV PATH="/home/scraper/.local/bin:${PATH}"

# Copy application files
COPY --chown=scraper:scraper . .

# Set environment variables for headless Chrome
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome
ENV WEBDRIVER_CHROME_DRIVER=/usr/bin/chromedriver

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:10000/health', timeout=5)" || exit 1


# Expose health check port (default 10000, can be overridden)
ARG PORT=10000
ENV PORT=${PORT}
EXPOSE ${PORT}

# Run the service
CMD ["gunicorn", "amulscraper:app", "--bind", "0.0.0.0:${PORT}", "--timeout", "120"]
