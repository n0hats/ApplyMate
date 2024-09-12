import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def setup():
    driver = webdriver.Chrome()
    vars = {}
    return driver, vars

def teardown(driver):
    driver.quit()

def wait_for_window(driver, vars, timeout=2):
    time.sleep(round(timeout / 1000))
    wh_now = driver.window_handles
    wh_then = vars["window_handles"]
    if len(wh_now) > len(wh_then):
        return set(wh_now).difference(set(wh_then)).pop()

def test_untitled(driver, vars):
    driver.get("https://www.linkedin.com/company/linkedin/life/2d812633-5835-4a2b-9c32-cae8bbe4ec28/")
    driver.set_window_size(2576, 1408)
    driver.find_element(By.ID, "ember289").click()
    driver.find_element(By.CSS_SELECTOR, ".org-jobs-job-search-form-module__typeahead-input").click()
    driver.find_element(By.CSS_SELECTOR, ".org-jobs-job-search-form-module__typeahead-input").send_keys("detection engineer")
    driver.execute_script("window.scrollTo(0,0)")
    driver.execute_script("window.scrollTo(0,0)")
    driver.find_element(By.CSS_SELECTOR, "#ember39 use").click()
    driver.find_element(By.CSS_SELECTOR, "#basic-result-tbi4rq .jobs-search-box__search-starter-text").click()
    driver.execute_script("window.scrollTo(0,0)")
    driver.execute_script("window.scrollTo(0,0)")
    driver.find_element(By.ID, "ember51").click()
    driver.execute_script("window.scrollTo(0,0)")
    driver.find_element(By.ID, "searchFilter_company").click()
    driver.find_element(By.CSS_SELECTOR, ".list-style-none:nth-child(2) > .search-reusables__collection-values-item:nth-child(1) > .search-reusables__value-label").click()
    driver.find_element(By.CSS_SELECTOR, ".list-style-none:nth-child(2) > .search-reusables__collection-values-item:nth-child(2) > .search-reusables__value-label").click()
    driver.find_element(By.CSS_SELECTOR, ".list-style-none:nth-child(2) > .search-reusables__collection-values-item:nth-child(4)").click()
    driver.find_element(By.CSS_SELECTOR, ".list-style-none:nth-child(2) > .search-reusables__collection-values-item:nth-child(4) > .search-reusables__value-label").click()
    driver.find_element(By.CSS_SELECTOR, ".list-style-none:nth-child(2) > .search-reusables__collection-values-item:nth-child(3) > .search-reusables__value-label").click()
    driver.find_element(By.CSS_SELECTOR, "#ember565 > .artdeco-button__text").click()
    driver.execute_script("window.scrollTo(0,0)")
    driver.execute_script("window.scrollTo(0,0)")
    driver.execute_script("window.scrollTo(0,0)")
    driver.execute_script("window.scrollTo(0,0)")
    driver.execute_script("window.scrollTo(0,0)")
    driver.execute_script("window.scrollTo(0,0)")
    driver.find_element(By.CSS_SELECTOR, "#ember737 > button").click()
    driver.execute_script("window.scrollTo(0,0)")
    driver.execute_script("window.scrollTo(0,0)")
    driver.find_element(By.CSS_SELECTOR, "#ember1093 > button").click()
    driver.execute_script("window.scrollTo(0,0)")
    vars["window_handles"] = driver.window_handles
    driver.find_element(By.CSS_SELECTOR, ".org-jobs-job-search-form-module__typeahead-input").send_keys(Keys.ENTER)
    vars["win2303"] = wait_for_window(driver, vars, 2000)
    driver.switch_to.window(vars["win2303"])

def main():
    driver, vars = setup()
    try:
        test_untitled(driver, vars)
        print("Test completed successfully!")
    finally:
        teardown(driver)

if __name__ == "__main__":
    main()
