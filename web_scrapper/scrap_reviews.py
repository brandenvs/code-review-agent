from selenium import webdriver

from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def match_task(task_name):
    match task_name:
        case 'Task 1 - Intro to Cyber Security I':
            return 'T01 – Pre-Assessment MCQ'
        case 'Task 2 - Intro to Cyber Security II':
            return 'T02 – Getting Started with Your Bootcamp'
        case 'Task 3 - Thinking Like a Programmer - Pseudo code':
            return 'T03 – Data Types and Conditional Statements'
        case 'Task 4 - Iteration':
            return 'T04 – Iteration'
        case 'Task 5 - Build Your Brand - Technical Portfolio':
            return 'T05 – Build Your Brand – Technical Portfolio'
        case 'Task 6 - Programming with User-defined Functions':
            return 'T06 – Programming with User-defined Functions'
        case 'Task 9 - OOP - Classes':
            return 'T09 – OOP – Classes'
        case 'Task 11 - Cyber Crimes':
            return 'T11 – Cyber Crimes'
        case 'Task 13 - Cyber Security Tools - Linux':
            return 'T13 – Cyber Security Tools– Linux'
        case 'Task 20 - PKI and Man-in-the-middle Attacks':
            return 'T20 – PKI and Man-in-the-Middle Attacks'
        case 'Task 21 - XSS (Cross-Site Scripting) Vulnerability':
            return 'T21 – XSS (Cross-Site Scripting) Vulnerability'
        case 'Task 23 - SQL Injection':
            return 'T23 – SQL Injection'
        case 'Task 24 - Penetration Testing':
            return 'T24 – Penetration Testing'
        case 'Task 26 - A Toolbox for Ethical Hacking':
            return 'T26 – A Toolbox for Ethical Hacking'
        case _:
            return 'Task not found'

def load_review_data(url, driver: webdriver.Edge) -> list:
    driver.get(url)
    
    # Wait for the page to load and the table rows to be available
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//tr"))
    )
    
    review_data_list = []

    rows = driver.find_elements(By.XPATH, "//tr")

    # Add a small delay to avoid overwhelming the page or server
    time.sleep(2)

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")

        if len(cells) >= 9:
            course_lvl = cells[2].text.strip()

            if course_lvl != 'DFECSL1':
                continue

            task_name = cells[3].text.strip()

            if task_name == 'Task 1 - Pre-Assessment MCQ':
                continue
            elif task_name == 'Task 27 - Post-Assessment MCQ':
                continue

            student_id = cells[4].text.strip() 
            review_link = cells[9].find_element(By.TAG_NAME, "a").get_attribute('href')

            task_name = match_task(task_name)

            data_result = {
                'course_lvl': course_lvl,
                'student_id': student_id,
                'task_name': task_name,
                'review_link': review_link
            }
            review_data_list.append(data_result)

    driver.quit()
    return review_data_list


def get_review(url: str, driver: webdriver.Edge):
    # Open the URL
    driver.get(url)
    
    # Enter username
    input_username = driver.find_element(By.NAME, 'username')
    input_username.send_keys("brandenvs@hyperiondev.com")
    time.sleep(2)

    # Enter password
    input_password = driver.find_element(By.NAME, 'password')
    input_password.send_keys("fTpX5U&Y7l&0%*3c")
    input_password.send_keys(Keys.RETURN) 
    time.sleep(3)

    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="format"]'))
    )
    review_text_link = link.get_attribute('href')  # Perform the click action

    driver.get(review_text_link)

    time.sleep(3)

    review = driver.find_element(
        By.CSS_SELECTOR, 
        "pre[style='word-wrap: break-word; white-space: pre-wrap;']"
    )

    review_text = review.text

    driver.quit()
    return review_text
