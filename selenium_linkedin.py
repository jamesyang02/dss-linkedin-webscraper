from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions() # opens browser
# options.add_argument("--headless=new") # makes it faster, but you won't see what's happening
options.add_argument("--ignore-certificate-errors")
options.add_experimental_option("detach", True) 
service = Service(ChromeDriverManager().install()) # installs the chrome that this webdriver will use
driver = webdriver.Chrome(options=options, service=service)
wait = WebDriverWait(driver, 10)

driver.get("https://www.linkedin.com/uas/login")
# create a expectation condition for waiting
wait.until(EC.title_contains("Sign"))


# login sequence
if (driver.title.__contains__("Sign")):
    print("Please login to LinkedIn to use the webscraper:")
    while(driver.title.__contains__("Sign")):
        # ask for credentials
        session_username = input("Email: ")
        session_password = input("Password: ")
        # find the username and password bars from the linkedin login page
        login_username = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[1]/input")
        login_password = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[2]/input")
        # input credentials
        login_username.clear()
        login_password.clear()
        login_username.send_keys(session_username)
        login_password.send_keys(session_password, Keys.ENTER)

    # wait after inputting
    time.sleep(2.5)

# get the company name as input
company = input("Please input a company name: ")
search_bar = driver.find_element(By.XPATH, "/html/body/div[5]/header/div/div/div/div[1]/input")
# get the occupation as input
occupation = input("Please input a job type: ")
# search!
search_bar.send_keys(company + " " + occupation, Keys.ENTER)
time.sleep(2.5)

# navigate to the list of all people
driver.find_element(By.XPATH, "//a[contains(text(), 'See all people results')]").click()

# collect all the links to profiles in an array
all_people_links = []

"""
Plan of action once we are on the list of all profiles:
1. Grab all profile links and store in array for later use
2. Visit profile links one by one
3. Run Apollo on each page to get emails

4. Package names, profiles, and emails nicely and export
"""