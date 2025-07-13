FROM --platform=linux/amd64 mcr.microsoft.com/playwright:v1.50.0-noble

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y x11vnc xvfb python3-pip
RUN apt-get -y clean;
# RUN mkdir ~/.vnc
# RUN x11vnc --version

# Install Playwright in Node.js environment
RUN npx playwright install chrome

WORKDIR /app
# RUN npm i -g pnpm
# COPY package.json ./
# RUN pnpm install -P
# COPY ./app/playwright/app/config.json ./

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

CMD ["uvx", "mcp-proxy", "--pass-environment", "--host", "0.0.0.0", "--port", "8001",  "--named-server-config", "/app/conf/config.json"]
EXPOSE 8001