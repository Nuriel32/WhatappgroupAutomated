from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import logging

# Enable debug logging
logging.basicConfig(level=logging.INFO)


def load_contacts(file_path):
    """
    Load contacts from a CSV file and return a list of phone numbers as strings.
    """
    try:
        logging.info(f"Loading contacts from file: {file_path}")
        # Load the CSV file, ensuring phone numbers are treated as strings
        data = pd.read_csv(file_path, dtype={'Phone 1 - Value': str})
        logging.info("CSV Content:\n" + str(data.head()))  # Show first few rows

        # Check if the 'Phone 1 - Value' column exists
        if 'Phone 1 - Value' not in data.columns:
            raise ValueError("The file must have a column named 'Phone 1 - Value'.")

        # Extract phone numbers, clean them, and ensure they are strings
        contacts = [
            contact.strip() for contact in data['Phone 1 - Value'].dropna()
        ]
        logging.info(f"Loaded {len(contacts)} contacts:")
        for contact in contacts:
            logging.info(contact)
        return contacts
    except Exception as e:
        logging.error(f"Error loading contacts: {e}")
        return []


def open_whatsapp(driver):
    """
    Open WhatsApp Web and wait for the user to scan the QR code.
    """
    logging.info("Opening WhatsApp Web...")
    driver.get("https://web.whatsapp.com/")
    logging.info("Please scan the QR code to log in.")
    time.sleep(30)  # Wait for QR code scan
    logging.info("WhatsApp Web login completed.")


def create_group(driver, contacts, group_name):
    """
    Create a WhatsApp group with the given contacts and group name.
    """
    try:
        logging.info(f"Creating a new group named '{group_name}'...")

        # Click on the "Menu" (three dots) using aria-label
        menu_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="תפריט"]'))
        )
        menu_button.click()
        logging.info("Menu button clicked.")

        # Select "New Group" (labeled as "קבוצה חדשה" in Hebrew)
        new_group_option = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[text()="קבוצה חדשה"]'))
        )
        new_group_option.click()
        logging.info("New group option (קבוצה חדשה) selected.")

        # Add contacts
        for contact in contacts:
            logging.info(f"Adding contact: {contact}")
            search_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="אפשר לחפש שם או מספר"]'))
            )
            search_box.send_keys(contact)
            time.sleep(2)

            # Grab the first user from the search results
            try:
                first_result = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span[title]'))
                )
                first_result.click()
                logging.info(f"First user in search results added for contact: {contact}")
            except Exception:
                logging.warning(f"Could not find or add the first user for contact: {contact}. Skipping.")
            search_box.clear()

        # Click the forward arrow button to proceed to group naming
        forward_arrow = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-icon="arrow-forward"]'))
        )
        forward_arrow.click()
        logging.info("Forward arrow clicked. Proceeding to group naming.")

        # Enter the group name
        group_name_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-lexical-editor="true"]'))
        )
        group_name_box.send_keys(group_name)
        logging.info(f"Group name entered: {group_name}")

        # Press the checkmark button to complete group creation
        checkmark_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-icon="checkmark-medium"]'))
        )
        checkmark_button.click()
        logging.info(f"Group '{group_name}' created successfully.")
    except Exception as e:
        logging.error(f"Error creating group: {e}")
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise
    """
    Create a WhatsApp group with the given contacts and group name.
    """
    try:
        logging.info(f"Creating a new group named '{group_name}'...")

        # Click on the "Menu" (three dots) using aria-label
        menu_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="תפריט"]'))
        )
        menu_button.click()
        logging.info("Menu button clicked.")

        # Select "New Group" (labeled as "קבוצה חדשה" in Hebrew)
        new_group_option = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[text()="קבוצה חדשה"]'))
        )
        new_group_option.click()
        logging.info("New group option (קבוצה חדשה) selected.")

        # Add contacts
        for contact in contacts:
            logging.info(f"Adding contact: {contact}")
            search_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="אפשר לחפש שם או מספר"]'))
            )
            search_box.send_keys(contact)
            time.sleep(2)

            # Grab the first user from the search results
            try:
                first_result = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span[title]'))
                )
                first_result.click()
                logging.info(f"First user in search results added for contact: {contact}")
            except Exception:
                logging.warning(f"Could not find or add the first user for contact: {contact}. Skipping.")
            search_box.clear()

        # Proceed to group naming
        next_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="next"]'))
        )
        next_button.click()
        logging.info("Proceeded to group naming.")

        # Enter group name
        group_name_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
        )
        group_name_box.send_keys(group_name)
        logging.info(f"Group name entered: {group_name}")

        # Create the group
        create_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="checkmark-medium"]'))
        )
        create_button.click()
        logging.info(f"Group '{group_name}' created successfully.")
    except Exception as e:
        logging.error(f"Error creating group: {e}")
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise


def main():
    """
    Main function to execute the script.
    """
    # File paths and group name
    csv_path = r"E:\Downloads\‏‏Converted_Group_1 .csv"
    group_name = "A"

    # Load contacts
    contacts = load_contacts(csv_path)
    if not contacts:
        logging.error("No valid contacts loaded. Exiting.")
        return

    logging.info("Setting up WebDriver...")
    try:
        # Set up Selenium WebDriver with Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Automatically manage ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)
        logging.info("WebDriver setup complete.")

        # Open WhatsApp Web and create the group
        open_whatsapp(driver)
        create_group(driver, contacts, group_name)

        logging.info("Script execution completed.")
    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
        logging.info("WebDriver closed.")


if __name__ == "__main__":
    main()
