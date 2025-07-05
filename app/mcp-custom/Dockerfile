FROM python:3.12-bullseye

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get -y clean;
# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Copy the requirements file and install Python dependencies
COPY ./app/mcp-custom/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright in Python environment
RUN pip install playwright
RUN playwright install --with-deps
# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"
CMD ["uvx", "mcp-proxy", "--host", "0.0.0.0", "--port", "8000",  "--named-server-config", "/app/conf/config.json"]
EXPOSE 8000
