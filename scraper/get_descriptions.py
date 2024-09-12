from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from __init__ import uname, passwd
import time
from bs4 import BeautifulSoup

# Set up the WebDriver
driver = webdriver.Chrome()

try:
    # Open LinkedIn login page
    driver.get("https://www.linkedin.com/login")

    # Enter your LinkedIn credentials
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password = driver.find_element(By.ID, "password")
    username.send_keys(uname)
    password.send_keys(passwd)

    # Click the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    # Wait for the login process to complete
    WebDriverWait(driver, 10).until(
        EC.url_contains("feed")
    )

    # Navigate to the LinkedIn job search page
    driver.get("https://www.linkedin.com/jobs/")

    # Wait for the job search input to be present
    job_search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "id=jobs-search-box-keyword-id-ember29"))
    )
    job_search_input.send_keys("Software Engineer")
    job_search_input.send_keys(Keys.RETURN)

    # Wait for the search results to load
    time.sleep(5)

    # Scroll to the bottom of the page to load more jobs
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Adjust time as needed

    # Get the page source and parse it with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find job descriptions
    job_cards = soup.find_all('div', class_='job-card-container__link')

    for job_card in job_cards:
        job_title = job_card.find('h3', class_='job-card-list__title').text.strip()
        company_name = job_card.find('h4', class_='job-card-container__company-name').text.strip()
        job_location = job_card.find('span', class_='job-card-container__metadata-item').text.strip()

        # To get the job description, LinkedIn typically loads it on a separate page
        # You can try opening the job link for more details
        job_link = job_card['href']
        print(f"Job Title: {job_title}")
        print(f"Company: {company_name}")
        print(f"Location: {job_location}")
        print(f"Job Link: https://www.linkedin.com{job_link}")
        print("-" * 40)

finally:
    # Close the WebDriver
    driver.quit()
