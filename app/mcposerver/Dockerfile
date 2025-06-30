FROM ghcr.io/open-webui/mcpo:latest

# Copy the requirements file and install Python dependencies
COPY ./app/mcposerver/requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt

# Install Playwright in Node.js environment
RUN npx playwright install chrome

# Install Playwright in Python environment
RUN pip install playwright
RUN playwright install --with-deps