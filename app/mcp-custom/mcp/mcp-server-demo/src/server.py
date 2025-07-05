import re
import base64
import os
import json
import uuid
import asyncio

from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright
from datetime import datetime
from google.cloud import storage
from google.oauth2 import service_account
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

mcp = FastMCP("Timestamp MCP")

@mcp.tool()
async def get_timestamp():
    """Returns the current server timestamp."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"response": f"The current server time is: {now}"}

@mcp.tool()
async def get_screenshot(
    url: str = "https://www.google.com",
    format: str = "jpeg",
    width: int = 640,
    height: int = 480,
):
    """Takes a screenshot of a given URL and returns it as a base64 encoded image."""
    # Ensure the URL has a scheme
    if not re.match(r'^[a-zA-Z]+://', url):
        url = 'https://' + url

    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Apply stealth measures to help bypass bot detection
        await page.set_viewport_size({"width": width, "height": height})
        await page.goto(url, wait_until="networkidle")
        
        screenshot_bytes = await page.screenshot(type=format)
        
        await browser.close()

    gcs_credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    gcs_bucket_name = os.getenv("GCS_BUCKET_NAME")

    if gcs_credentials_json and gcs_bucket_name:
        try:
            credentials_info = json.loads(gcs_credentials_json)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_info
            )
            storage_client = storage.Client(credentials=credentials)
            bucket = storage_client.bucket(gcs_bucket_name)

            filename = f"screenshots/{uuid.uuid4()}.{format}"
            blob = bucket.blob(filename)

            blob.upload_from_string(
                screenshot_bytes, content_type=f"image/{format}"
            )

            blob.make_public()

            public_url = blob.public_url
            markdown_image = f"![Screenshot of {url}]({public_url})"
            return {"response": markdown_image}
        except Exception as e:
            return {"response": f"Error uploading screenshot to GCS: {e}"}

    # Fallback to base64 if GCS is not configured
    encoded_string = base64.b64encode(screenshot_bytes).decode("utf-8")
    mime_type = f"image/{format}"
    data_uri = f"data:{mime_type};base64,{encoded_string}"
    markdown_image = f"![Screenshot of {url}]({data_uri})"
    return {"response": markdown_image}

def main():
    """Entry point for running the server."""
    # Create and run the server directly without asyncio.run
    mcp.run(transport="stdio")