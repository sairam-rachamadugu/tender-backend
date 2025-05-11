from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
def is_int(s):
    #print(s)
    try:
        float(s)
        #print(s)
        return True
    except ValueError:
        return False

def scrape_and_save():
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    
    # Set up WebDriver with auto ChromeDriver management
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Step 1: Go to the login page
    driver.get("https://tender.telangana.gov.in/login.html")
    
    # If login is required, fill in login details (adjust if needed)
    # Example: Enter username and password and submit
    # driver.find_element(By.ID, "username_field").send_keys("your_username")
    # driver.find_element(By.ID, "password_field").send_keys("your_password")
    # driver.find_element(By.ID, "login_button").click()
    
    # Wait for page to load and proceed to the live tenders page
    time.sleep(3)
    
    # Step 2: Click on "View More" under Live Tenders
    view_more_button = driver.find_element(By.XPATH, "//a[contains(text(), 'More...')]")
    view_more_button.click()
    
    # Wait for the page to load fully
    time.sleep(3)
    
    # Step 3: Apply filter for Bhupalpally district (adjust XPath or select method as needed)
    # Example: Select the district (if it's a dropdown)
    district_dropdown = driver.find_element(By.XPATH, "//select[@name='ddlDistrict']")
    district_dropdown.click()
    
    # Wait for options to appear and select Bhupalpally
    district_option = driver.find_element(By.XPATH, "//option[contains(text(), 'JAYASHANKAR BHUPALPALLY')]")
    district_option.click()
    
    
    
    district_search = driver.find_element(By.XPATH, "//input[@id='searchTender']")
    district_search.click()
    
    time.sleep(5)
    
    # Click to apply the filter (if needed)
    # driver.find_element(By.XPATH, "//button[text()='Apply']").click()
    district_dropdown_t = driver.find_element(By.XPATH, "//select[@name='pagetable13_length']")
    district_dropdown_t.click()
    
    # Wait for options to appear and select Bhupalpally
    district_option_t = driver.find_element(By.XPATH, "//option[contains(text(), '100')]")
    district_option_t.click()
    # Wait for filtered results to load
    time.sleep(5)
    
    # Step 4: Scrape the tender details
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    # Example: Extract tender data from the table
    tenders = []
    for row in soup.select("table tr")[1:]:  # Skip header row
        cols = row.find_all("td")
        #print(len(cols))
        if len(cols) >= 8 and is_int(cols[5].text.strip()):  # Ensure it has enough columns
            tender = {
                #"department": cols[0].text.strip(),
                "tender_id": cols[1].text.strip(),
                "tender_dep": cols[2].text.strip(),
                "title": cols[4].text.strip(),
                "estimated_value": cols[5].text.strip(),
                "published_date": cols[6].text.strip(),
                "start_date": cols[7].text.strip(),
                "closing_date": cols[8].text.strip(),
            }
            tenders.append(tender)
            #print("inside")
    from functools import cmp_to_key
    
    def compare(t1, t2):
        return float(t2["estimated_value"]) - float(t1["estimated_value"]) 
    
    tenders.sort(key=cmp_to_key(compare))
    
    # Output the tenders data
    # tenders.sort(key=lambda tender1,tender2 : 1 if int(tender1["estimated_value"]) > int(tender2["estimated_value"]) else -1)
    # for tender in tenders:
    #print(tenders)
    #print(len(tenders))
    # Step 5: Close the browser session
    driver.quit()
    with  open("data.json","w") as f:
        json.dump(tenders,f)

scrape_and_save()
    