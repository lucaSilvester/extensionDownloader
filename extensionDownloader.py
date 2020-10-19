from selenium import webdriver
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-l", "--link", help="link of extension to download")
parser.add_argument("-wd", "--webdriver", help="webdriver location")

args = parser.parse_args()

print("link {} webdriver {}".format(
        args.link,
        args.webdriver
        ))

def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)

driver = webdriver.Chrome(args.webdriver)

driver.get(args.link)

element_present = EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Download Extension']"))

WebDriverWait(driver, 5).until(element_present)

donwloadButton = driver.find_element_by_xpath("//button[@aria-label='Download Extension']")
donwloadButton.click()

paths = WebDriverWait(driver, 120, 1).until(every_downloads_chrome)
# print(paths)
driver.close()