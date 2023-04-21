from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass
import pandas as pd

options = webdriver.ChromeOptions() # opens browser

# options to add apollo as an extension
options = webdriver.ChromeOptions()
options.add_extension('./Apollo-io.crx')

# get rid of the ugly warnings from Selenium
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("ignore-certificate-errors")

# SO NO HEAD????
# options.add_argument("--headless=new") # makes it faster, but you won't see what's happening
options.add_experimental_option("detach", True) 
service = Service(ChromeDriverManager().install()) # installs the chrome that this webdriver will use
driver = webdriver.Chrome(options=options, service=service)
wait = WebDriverWait(driver, 10)

driver.get("https://www.linkedin.com/uas/login")
# create a expectation condition for waiting
wait.until(EC.title_contains("Sign"))
# switch to the linkedin tab
driver.switch_to.window(driver.window_handles[0])


# OLD MANUAL LOGIN METHOD
# login sequence
if (driver.title.__contains__("Sign")):
    print("Please login to LinkedIn to use the webscraper:")
    while(driver.title.__contains__("Sign")):
        # ask for credentials
        session_username = input("Email: ")
        session_password = getpass.getpass() # makes the password input protected (not visible)
        print()
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

"""
# NEW AUTO LOGIN METHOD unfortunately doesn't work
# login sequence
login_username = driver.find_element(By.ID, "username")
login_password = driver.find_element(By.ID, "password")
# input credentials
login_username.send_keys("dssberkeley.tech@gmail.com")
login_password.send_keys("TechWithZek420", Keys.ENTER)
time.sleep(5)
"""

# THIS IS A LOOP FOR COMPANY AND JOB SEARCH
search_successful = 0
while search_successful == 0:
    # get the company name as input
    company = input("Please input a company name: ")
    search_bar = driver.find_element(By.CLASS_NAME, "search-global-typeahead__input")
    # get the occupation as input
    occupation = input("Please input a job type: ")
    # clear search bar and search!
    search_bar.clear()
    search_bar.send_keys(company + " " + occupation, Keys.ENTER)
    time.sleep(5)
    # after searching, make sure that results are actually shown eg. you're not on the "no results found" page
    try:
        driver.find_element(By.XPATH, "//a[contains(text(), 'See all people results')]")
    except:
        print("Improper results returned! Have you spelled everything correctly? \n")
    else:
        search_successful = 1

# navigate to the list of all people ("See all people results")
driver.find_element(By.XPATH, "//a[contains(text(), 'See all people results')]").click()
time.sleep(5)

# collect all the links to profiles in an array
all_link_blocks = driver.find_elements(By.CLASS_NAME, "entity-result")
all_profile_links = [block.find_element(By.CLASS_NAME, "app-aware-link").get_attribute("href") for block in all_link_blocks]

# remove links that do not lead directly to profiles
cleaned_profiles = []
for link in all_profile_links:
    if "/in" in link:
        cleaned_profiles.append(link)

# display number of links after cleaning
print("\nFound ", len(all_profile_links), "links")
print("after James's flaming laser sword, ", len(cleaned_profiles), " links remain \n")

# this doesn't work yet, idk why it's so hard to press the next button
# next_button = driver.find_element(By.ID, "ember443")

"""
Plan of action once we are on the list of all profiles:
1. Grab all profile links and store in array for later use, DONE for first page, need way to do multiple pages of results -- James
2. Visit profile links one by one
3. Run Apollo on each page to get emails

4. Package names, profiles, and emails nicely and export -- Preetha
"""
"""
# wait for Apollo login manually lol (will fix later hopefully)
apollo_login_successful = 0
while apollo_login_successful == 0:
    apollo_wait = input("Hit Enter once signed into Apollo to continue! \n")
    # unmovable Apollo sidebar icon has classname x_bfaN0
    # movable Apollo sidebar icon has classname   x_ra5C3
    # check to see if signed into Apollo
    try:
        driver.find_element(By.CLASS_NAME, "x_ra5C3")
    except:
        apollo_override = input("Apollo login not detected! Try again (hit Enter) or override (enter 'y'): ")
        # if override, treat as if login was successful
        if apollo_override.lower() == "y":
            apollo_login_successful = 1
            print("Continuing...\n")
        else:
            continue
    else:
        apollo_login_successful = 1

"""

# login to Apollo
# store the linkedin tab
original_window = driver.current_window_handle
# open a new tab
driver.switch_to.new_window('tab')
# go to apollo
driver.get("https://app.apollo.io/#/login")
time.sleep(2)
driver.find_element(By.CLASS_NAME, "zp_kxUTD").click()
time.sleep(1)
driver.find_element(By.CLASS_NAME, "whsOnd").send_keys("dssberkeley.tech", Keys.ENTER)
time.sleep(1)
driver.find_element(By.CLASS_NAME, "whsOnd").send_keys("TechWithZek420", Keys.ENTER)
# return to linkedin tab
driver.switch_to.window(original_window)

# create name and email columns / arrays
names = []
emails = []

# one big try catch to make sure Apollo works before telling the user they can sit back
print("One last check to make sure everything is working...")
try:
    driver.get(cleaned_profiles[0])
    time.sleep(6)
    driver.find_element(By.CLASS_NAME, "x_SULq8").text
except:
    print("Couldn't find information with Apollo! Exiting the webscraper...")
    quit()
else:
    print("Everything looks good! Beginning the scraping process! Sit back and relax...\n")

# visit each page individually and run Apollo on every link
for link in cleaned_profiles:
    driver.get(link)
    # sleep to wait for the Apollo tab to open automatically
    time.sleep(6)

    # grab the name! Adding a try and FAIL if Apollo was overridden and not signed in
    try:
        driver.find_element(By.CLASS_NAME, "x_SULq8").text
    except:
        print("Couldn't find information with Apollo! Exiting the webscraper...")
        quit()
    else:
        this_name = driver.find_element(By.CLASS_NAME, "x_SULq8").text
        names.append(this_name)
        print(this_name)

    # click the div that reveals the email
    try:
        driver.find_element(By.CLASS_NAME, "x_LQDkG").click()
    except:
        pass
    time.sleep(1)

    # grab the email!
    try:
        this_email = driver.find_element(By.CLASS_NAME, "x_GxQlI").text
    # if except, appends NaN. If successful, appends email
    except:
        print("No valid email!\n")
        emails.append("NaN")
    else:
        emails.append(this_email)
        print(this_email + "\n")


# Converts the given information (sames, email, occupation, company, profile links)
data = {'Name': names, 'Email': emails, 'Company' : [company]*len(names), 'Occupation': [occupation]*len(names), 
        'Profile': cleaned_profiles}
df = pd.DataFrame(data)
df.to_csv('out.csv')
compression_opts = dict(method='zip',
                        archive_name='out.csv')  
df.to_csv('out.zip', index=False,
          compression=compression_opts) 

print("Scraping complete! Check the webscraper folder for out.csv")
