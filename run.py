import os
import time
import requests

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def create_driver():
    options = Options()
    options.add_argument("--headless=new")        # run headless (Chrome 109+ prefers this)
    options.add_argument("--disable-gpu")         # helps on Windows
    options.add_argument("--no-sandbox")          # good for Linux/containers
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")         # suppress most logs (0=ALL, 3=ERROR)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # hide USB/devtools warnings

    driver = webdriver.Chrome(options=options)
    return driver

def download_image(url, filename):
    """
        Downloads an image from a URL and saves it locally.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Original image saved as {filename}")
    else:
        print(f"Failed to retrieve image from {url}")

def apply_watermark(input_image_path, output_image_path):
    """
    Applies a watermark (with transparency) to an image and saves the result.
    """
    # Open images
    base_image = Image.open(input_image_path).convert("RGBA")
    watermark = Image.open("badge.png").convert("RGBA")

    # Resize watermark relative to base image
    wm_width = base_image.width // 4
    wm_height = int(watermark.height * (wm_width / watermark.width))
    watermark = watermark.resize((wm_width, wm_height), Image.LANCZOS)

    # Apply opacity (75%)
    alpha = watermark.split()[-1]
    alpha = alpha.point(lambda i: i * 0.75)  # Adjust transparency here
    watermark.putalpha(alpha)

    # Position watermark in bottom-right corner
    pos_x = base_image.width - watermark.width - 50
    pos_y = 50 # base_image.height - watermark.height - 50 
    position = (pos_x, pos_y)

    # Create transparent layer same size as base image
    watermark_layer = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
    watermark_layer.paste(watermark, position, watermark)  # use watermark as its own mask

    # Composite
    watermarked_image = Image.alpha_composite(base_image, watermark_layer)

    # Save result (convert back to RGB if you don’t want transparency in final file)
    watermarked_image.convert("RGB").save(output_image_path, "JPEG")

    print(f"Watermarked image saved as {output_image_path}")

def update_web():
    """
    Uses Selenium to navigate a webpage, scroll to load all products,
    download product images, and apply watermarks.
    """
    driver = create_driver()
    driver.get("https://grassroots.treez.io/onlinemenu/?customerType=ADULT")

    # Wait for elements to load
    time.sleep(5) 

    # Click past age verification
    over21 = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[3]/div[2]/button")
    over21.click()
    time.sleep(3) 
    print(">>> Bypassed age verification")

    # Set cursor to product window
    product_window = driver.find_element(By.ID, "product-menu")
    print(">>> Set cursor to product window")

    # Scroll to load all products
    prev_count = 0
    print(">>> Scrolling to load all products...")
    while True:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) 

        # Count loaded products
        items = driver.find_elements(By.CLASS_NAME, "menu-item")
        new_count = len(items)
        
        # Break if no new products loaded
        if new_count == prev_count:
            break
        prev_count = new_count

    # Find all product divs
    product_divs = product_window.find_elements(By.CLASS_NAME, "menu-item")
    print(f">>> Loaded {new_count} products")

    # Iterate over products
    count = 0
    for div in product_divs:
        product_image = div.find_element(By.TAG_NAME, "img")
        img_url = product_image.get_attribute("src")
        download_image(img_url, f"unmarked-images/00{count}.jpg")
        apply_watermark(f"unmarked-images/00{count}.jpg", f"complete-images/00{count}.jpg")
        count += 1

    driver.quit()


if __name__ == "__main__":
    while True:
        answer = input(
            "Would you like to update the website's existing images or watermark a local image? (web/local): "
        ).strip().lower()

        if answer == "web":
            update_web()
            break  # exit loop once done
        elif answer == "local":
            os.system("cls")
            input(
                "********************\n*** INSTRUCTIONS ***\n********************\n\n"
                "Navigate to the folder titled \"unmarked-images\" and place your image there.\n\n"
                "Press Enter when ready."
            )
            with os.scandir("unmarked-images/") as entries:
                for entry in entries:
                    if entry.name.lower().endswith((".png", ".jpg", ".jpeg")) and entry.is_file():
                        apply_watermark(
                            f"unmarked-images/{entry.name}",
                            f"complete-images/{entry.name}",
                        )
            break  # exit loop once done
        else:
            print("Invalid input. Please enter 'web' or 'local'.")