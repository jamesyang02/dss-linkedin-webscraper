from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# webdriver and wait imports
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# UI and logging imports
import tkinter # Python 3.x
from tkinter import ttk
from threading import Thread

# output imports
from datetime import datetime
import pandas as pd

# fun imports
import random

"""
LinkedIn Webscraper Developed by James Yang & Preetha Kumar
DSS Tech Committee Spring 2023
========================================
This webscraper will take in a company name and job title and 
output a csv file with the names, job titles, and LinkedIn URLs 
of the employees that match the search criteria.
"""
# GLOBAL VARIABLES - May change in the future
# LinkedIn login information is not used for now, waiting for LinkedIn to accept identity verification for the burner account
global APOLLO_EMAIL
APOLLO_EMAIL = "dssberkeley.tech@gmail.com"
global APOLLO_PASSWORD
APOLLO_PASSWORD = "TechWithZek420"
global LINKEDIN_EMAIL
LINKEDIN_EMAIL = "dssberkeley.tech@gmail.com"
global LINKEDIN_PASSWORD
LINKEDIN_PASSWORD = "TechWithZek420"

# SESSION VARIABLE NAMES for reference, defined globally in enter_data (I <3 spaghetti code)
"""
SESSION_EMAIL
SESSION_PASSWORD
SESSION_COMPANY
SESSION_JOB
"""
# Another check for the logger to see if the webscraper is done
global SCRAPER_SUCCESS
SCRAPER_SUCCESS = False

# The single worst variable I have ever declared
global CURRENT_LOG_MESSAGE
CURRENT_LOG_MESSAGE = "" # keeps track of the current tkinter logger message

# opens browser
# display opening splash text
splash_texts = ["Starting up...", 
    "Firing up the webscraper...",
    "Initializing systems...",
    "Connecting to smart fridge...",
    "Charging flux capacitors...",
    "Prepare for world destruction!...",
    "Beam me up, Scotty!...",
    "Engaging hyperdrive...",
    "Elevator music...",
    "Loading...",
    "Not again...",
    "Are you sure this version was cleared for production?...",
    "This is not the webscraper you're looking for...",
    "I'm not paid enough for this...",
    "DSS Tech Committee is the best!...",
    "Get down Mrs. Obama!!...",
    "All hail Zack!...",
    "I really hope this works...",
    "Secret message..."
]
print(splash_texts[random.randrange(0, len(splash_texts) - 1)])
options = webdriver.ChromeOptions()

# options to add apollo as an extension
options = webdriver.ChromeOptions()
options.add_extension('./Apollo-io.crx')

# get rid of the ugly warnings from Selenium
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("ignore-certificate-errors")

# SO NO HEAD???? (gets rid of visible chrome window)
options.add_argument("--headless=new") # makes it faster, but you won't see what's happening
options.add_argument('--window-size=1920,1080')

options.add_experimental_option("detach", True) 
service = Service(ChromeDriverManager().install()) # installs the chrome that this webdriver will use
driver = webdriver.Chrome(options=options, service=service)

# defines a default polling time while waiting for elements to load
wait = WebDriverWait(driver, timeout=10, poll_frequency=1)


# load LinkedIn login page
driver.get("https://www.linkedin.com/uas/login")
# Apollo auto opens a second tab, close it first
wait.until(lambda x: len(driver.window_handles) == 2)
driver.switch_to.window(driver.window_handles[1])
driver.close()
# wait until LinkedIn login page is loaded
driver.switch_to.window(driver.window_handles[0])
wait.until(EC.title_contains("Sign"))

# Create tkinter window for inputs
def run_tkinter():

    app_window = tkinter.Tk()
    app_window.title("LinkedIn Contact Webscraper")

    app_frame = tkinter.Frame(app_window)
    app_frame.pack()

    # submit inputs if SUBMIT button pressed
    def enter_data():
        # INPUT DATA FOR WEBSCRAPER SESSION, USE THESE VARIABLES WHERE LOGINS ARE NEEDED
        global SESSION_EMAIL
        global SESSION_PASSWORD
        global SESSION_COMPANY
        global SESSION_JOB
        SESSION_EMAIL = linkedin_email_input.get()
        SESSION_PASSWORD = linkedin_password_input.get()
        SESSION_COMPANY = company_name_input.get()
        SESSION_JOB = job_title_input.get()

        input_error_list = []
        # check if all inputs are filled
        if(SESSION_EMAIL == ""):
            input_error_list.append("LinkedIn Email")
        if(SESSION_PASSWORD == ""):
            input_error_list.append("LinkedIn Password")
        if(SESSION_COMPANY == "" and SESSION_JOB == ""):
            input_error_list.append("Company Name or Job Title")
        if(input_error_list != []):
            # open tkinter window for input error
            input_error_window = tkinter.Tk()
            input_error_window.title("Input Error!")
            input_error_frame = tkinter.Frame(input_error_window, padx=10, pady=10)
            input_error_frame.pack()
            input_error_label = tkinter.Label(input_error_frame,
                                              text="Input Error! Please fill in the following fields:\n" \
                                                + ', '.join(input_error_list))
            input_error_label.pack()
            input_error_button = tkinter.Button(input_error_frame,
                                                text="OK",
                                                command=input_error_window.destroy,
                                                width=15)
            input_error_button.pack()
            input_error_window.mainloop()
        else:
            # close tkinter window
            app_window.destroy()

    # close tkinter window if EXIT button pressed
    def exit_tkinter():
        app_window.destroy()
        driver.quit()
        quit()

    # User login information
    login_frame = tkinter.LabelFrame(app_frame, text="LinkedIn Login")
    login_frame.grid(row=0, column=0)
    linkedin_email = tkinter.Label(login_frame, text="LinkedIn Email: ")
    linkedin_email.grid(row=0, column=0)
    linkedin_password = tkinter.Label(login_frame, text="LinkedIn Password: ")
    linkedin_password.grid(row=0, column=1)
    # User login input
    linkedin_email_input = tkinter.Entry(login_frame, width=30)
    linkedin_email_input.grid(row=1, column=0)
    linkedin_password_input = tkinter.Entry(login_frame, show="*", width=30)
    linkedin_password_input.grid(row=1, column=1)

    # LinkedIn search information
    search_frame = tkinter.LabelFrame(app_frame, text="LinkedIn Search")
    search_frame.grid(row=1, column=0)
    company_name = tkinter.Label(search_frame, text="Company Name: ")
    company_name.grid(row=0, column=0)
    job_title = tkinter.Label(search_frame, text="Job Title: ")
    job_title.grid(row=0, column=1)
    # LinkedIn search input
    company_name_input = tkinter.Entry(search_frame, width=30)
    company_name_input.grid(row=1, column=0)
    job_title_input = tkinter.Entry(search_frame, width=30)
    job_title_input.grid(row=1, column=1)

    # make padding for input frames
    for widget in login_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)
    for widget in search_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    # buttons to submit inputs or quit the app
    submit_frame = tkinter.Frame(app_frame)
    submit_frame.grid(row=2, column=0)
    button = tkinter.Button(submit_frame, text="Exit", command=exit_tkinter, width=15)
    button.grid(row=2, column=0, padx=10, pady=10)
    button = tkinter.Button(submit_frame, text="Scrape!", command=enter_data, width=35)
    button.grid(row=2, column=1, padx=10, pady=10)

    # focus on the email form (place the cursor there)
    linkedin_email_input.focus()

    # mainloop window
    app_window.mainloop()

# Sign in failed window for tkinter sign in (invalid credentials)
def signin_error_window():
    error_window = tkinter.Tk()
    error_window.title("Error!")
    error_frame = tkinter.Frame(error_window)
    error_frame.pack()
    error_label = tkinter.Label(error_frame, text="Invalid credentials!")
    error_label.grid(row=0, column=0, padx=30, pady=10)
    error_button = tkinter.Button(error_frame, text="Try Again", command=error_window.destroy)
    error_button.grid(row=1, column=0, padx=10, pady=10)
    error_window.mainloop()
    return

# LOGGING WINDOW FUNCTION
def run_tkinter_logging():
    # helper function for updating logging window text
    def update_logging_window_text():
        logging_label.configure(text=CURRENT_LOG_MESSAGE)
        logging_window.update_idletasks()
        if SCRAPER_SUCCESS == True:
            progress_bar.stop()
        logging_window.after(200, update_logging_window_text)

    # create new tkinter window
    logging_window = tkinter.Tk()
    logging_window.geometry("700x170")
    logging_window.title("Scraping...")
    logging_frame = tkinter.Frame(logging_window)
    logging_frame.pack()

    # logging window text and progress bar
    logging_label = tkinter.Label(logging_frame, text=CURRENT_LOG_MESSAGE, padx=10, pady=10)
    progress_bar = ttk.Progressbar(logging_frame, orient="horizontal", length=400, mode="indeterminate")

    logging_label.grid(row=0, column=0, padx=30, pady=10)
    progress_bar.grid(row=1, column=0, padx=30, pady=10)
    progress_bar.start()

    # button to exit
    logging_button = tkinter.Button(logging_frame, text="Exit", command=logging_window.destroy, width=15)
    logging_button.grid(row=2, column=0, padx=10, pady=10)

    # mainloop window, update every second to check for new log messages
    logging_window.after(1000, update_logging_window_text)
    logging_window.mainloop()
    return

# MAIN FUNCTION
# run tkinter window
run_tkinter()

# need this outer loop in case some day the webscraper magically autosigns in with stored credentials or whatever
if (driver.title.__contains__("Sign")):
    # 
    while(driver.title.__contains__("Sign")):
        # find the username and password bars from the linkedin login page
        login_username = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[1]/input")
        login_password = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[2]/input")
        # input credentials
        login_username.clear()
        login_password.clear()
        # quit if no credentials entered
        try:
            SESSION_EMAIL
        except NameError:
            driver.quit()
            quit()
        # if credentials entered, check that they are valid
        if (SESSION_EMAIL == "" or SESSION_PASSWORD == ""):
            signin_error_window()
            run_tkinter()
        # login
        login_username.send_keys(SESSION_EMAIL)
        login_password.send_keys(SESSION_PASSWORD, Keys.ENTER)
        # if login fails (misspelled credentials), restart login sequence
        time.sleep(0.3)
        if (driver.title.__contains__("Sign")):
            signin_error_window()
            run_tkinter()

# After tkinter window is closed and login completes, start new thread for logging
tkinter_logging = Thread(target=run_tkinter_logging)
print("\nLogged in as " + SESSION_EMAIL + "...")
print()
# Update the logger message
CURRENT_LOG_MESSAGE = "Logged in as " + SESSION_EMAIL + "..."
tkinter_logging.start()

# bypass any account security popups
# "Add phone number for security"
try:
    driver.find_element(By.XPATH, "//a[contains(text(), 'Add a phone number for security')]")
except:
    pass
else:
    driver.find_element(By.CLASS_NAME, "secondary-action").click()

# TODO: There may be more... implement catches or fails as you discover new ones

# THIS IS THE LOOP FOR COMPANY AND JOB SEARCH
search_successful = 0
while search_successful == 0:
    # find the search bar
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "search-global-typeahead__typeahead")))
    #time.sleep(7)
    #driver.find_element(By.CLASS_NAME, "search-global-typeahead__input")
    search_link = driver.current_url
    print("Searching for \"" + SESSION_COMPANY + " " + SESSION_JOB + "\"...")
    CURRENT_LOG_MESSAGE = "Searching for \"" + SESSION_COMPANY + " " + SESSION_JOB + "\"..."
    # clicking shenanigans, sometimes the search bar is collapsed
    try:
        driver.find_element(By.CLASS_NAME, "search-global-typeahead__collapsed-search-button-icon").click()
    except:
        pass
    else:
        # stupidest fucking code I have ever written
        time.sleep(0.2)
        pass
    search_bar = driver.find_element(By.CLASS_NAME, "search-global-typeahead__input")
    # get the company name as input
    company = SESSION_COMPANY
    # get the occupation as input
    occupation = SESSION_JOB
    # clear search bar and search! We assume inputs are valid from cleaning earlier
    search_bar.clear()
    search_bar.send_keys(company + " " + occupation, Keys.ENTER)
    
    # wait until button to see people results shows up
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'See all people results')]")))
    except TimeoutError:
        print("Timed out while looking for results page! Have you spelled everything correctly?")
        CURRENT_LOG_MESSAGE = "Searching for " + SESSION_COMPANY + " " + SESSION_JOB + \
            "... \n Timed out while looking for results page! Have you spelled everything correctly?"
        driver.get(search_link)
    # after searching, make sure that results are actually shown eg. you're not on the "no results found" page
    try:
        driver.find_element(By.XPATH, "//a[contains(text(), 'See all people results')]")
    except:
        print("Improper results returned! Have you spelled everything correctly? \n")
        CURRENT_LOG_MESSAGE = "Searching for " + SESSION_COMPANY + " " + SESSION_JOB + \
            "... \n Improper results returned! Have you spelled everything correctly?"
        driver.get(search_link)
        # run_tkinter_stripped() TODO: implement this, only include company and occupation
    else:
        search_successful = 1

# navigate to the list of all people ("See all people results")
driver.find_element(By.XPATH, "//a[contains(text(), 'See all people results')]").click()
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "entity-result__title-text")))

# collect all the links to profiles in an array
all_link_blocks = driver.find_elements(By.CLASS_NAME, "entity-result")
all_profile_links = [block.find_element(By.CLASS_NAME, "app-aware-link").get_attribute("href") for block in all_link_blocks]

# remove links that do not lead directly to profiles
cleaned_profiles = []
for link in all_profile_links:
    if "/in" in link:
        cleaned_profiles.append(link)

# display number of links after cleaning
print("Found " + str(len(cleaned_profiles)) + " valid links!")
CURRENT_LOG_MESSAGE = "Found " + str(len(cleaned_profiles)) + " valid links! Signing into Apollo..."

# this doesn't work yet, idk why it's so hard to press the next button
# next_button = driver.find_element(By.ID, "ember443")

# login to Apollo
# store the linkedin tab
original_window = driver.current_window_handle
# open a new tab
driver.switch_to.new_window('tab')
# go to apollo
driver.get("https://app.apollo.io/#/login")
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "zp_kxUTD")))
try:
    driver.find_element(By.CLASS_NAME, "zp_kxUTD").click()
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "whsOnd")))
    driver.find_element(By.CLASS_NAME, "whsOnd").send_keys(APOLLO_EMAIL, Keys.ENTER)
    time.sleep(1.5)
    driver.find_element(By.CLASS_NAME, "whsOnd").send_keys(APOLLO_PASSWORD, Keys.ENTER)
    # short wait to make sure Apollo registers the sign in submission
    time.sleep(1)
    # return to linkedin tab
    driver.switch_to.window(original_window)
except:
    print("Apollo login failed! Exiting the webscraper...")
    print("Please tell James if this happens often, ty <3")
    CURRENT_LOG_MESSAGE = "Apollo login failed! Exiting the webscraper..." + \
                            "\n Please tell James if this happens often, ty <3"
    driver.quit()
    quit()
else:
    pass

# create name and email columns / arrays
names = []
emails = []

# one big try catch to make sure Apollo works before telling the user they can sit back
print("Running one last check to make sure everything is working...")
CURRENT_LOG_MESSAGE = "Running one last check to make sure everything is working..."
try:
    driver.get(cleaned_profiles[0])
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "x_kxUTD")))
    driver.find_element(By.CLASS_NAME, "x_SULq8").text
except:
    print("Couldn't find information with Apollo! A page may have loaded too slowly or Apollo sign-in failed.")
    print("Please tell James if this happens often, ty <3")
    print("Exiting the webscraper...")
    CURRENT_LOG_MESSAGE = "Couldn't find information with Apollo! A page may have loaded too slowly or Apollo sign-in failed." + \
                            "\n Please tell James if this happens often, ty <3" + \
                            "\n Exiting the webscraper..."
    driver.quit()
    quit()
else:
    print("Everything looks good! Beginning the scraping process! Sit back and relax...\n")
    CURRENT_LOG_MESSAGE = "Everything looks good! Beginning the scraping process! Sit back and relax..."
    this_name = driver.find_element(By.CLASS_NAME, "x_SULq8").text
    names.append(this_name)
    print(this_name)
    # click the div that reveals the email (if it exists)
    try:
        driver.find_element(By.CLASS_NAME, "x_LQDkG").click()
    except:
        pass
    else:
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

# visit each page individually and run Apollo on every link
for i in range(1, len(cleaned_profiles)):
    driver.get(cleaned_profiles[i])
    # wait for the Apollo tab to open automatically
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "x_kxUTD")))

    # grab the name! Adding a try and FAIL if Apollo was overridden and not signed in
    try:
        driver.find_element(By.CLASS_NAME, "x_SULq8").text
    except:
        print("Couldn't find information with Apollo! A page may have loaded too slowly.")
        print("Please tell James if this happens often, ty <3")
        print("Exiting the webscraper...")
        CURRENT_LOG_MESSAGE = "Couldn't find information with Apollo! A page may have loaded too slowly." + \
                            "\n Please tell James if this happens often, ty <3" + \
                            "\n Exiting the webscraper..."
        driver.quit()
        quit()
    else:
        this_name = driver.find_element(By.CLASS_NAME, "x_SULq8").text
        names.append(this_name)
        print(this_name)
    # click the div that reveals the email (if it exists)
    try:
        driver.find_element(By.CLASS_NAME, "x_LQDkG").click()
    except:
        pass
    else:
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

# Store results in a dataframe and export to csv
# Converts the given information (sames, email, occupation, company, profile links)
data = {'Name': names, 'Email': emails, 'Company' : [company]*len(names), 'Occupation': [occupation]*len(names), 
        'Profile': cleaned_profiles}
df = pd.DataFrame(data)

# Make a filename based on the company + date and time
# Get the current date and time
current_datetime = datetime.now()

file_datetime = current_datetime.strftime("%Y-%m-%d_%H%M%S")
# Outputs datetime as a string like YYYY-MM-DD_THHMMSS
output_filepath = SESSION_COMPANY + "_" + file_datetime

# export
df.to_csv("output/" + output_filepath + ".csv")
compression_opts = dict(method='zip',
                        archive_name=output_filepath + ".csv")  
df.to_csv("output/" + output_filepath + ".zip", index=False,
          compression=compression_opts)

print("Scraping complete! Outputs stored in", output_filepath, "in both csv and zip formats.")
CURRENT_LOG_MESSAGE = "Scraping complete! Outputs stored in " + output_filepath
SCRAPER_SUCCESS = True
driver.quit()
