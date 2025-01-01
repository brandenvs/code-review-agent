from selenium import webdriver

from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

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

        # Ensure there are enough cells in the row (at least 9 for course_lvl, task_name, student_id, review_link)
        if len(cells) >= 9:
            course_lvl = cells[2].text.strip()
            task_name = cells[3].text.strip()
            student_id = cells[4].text.strip() 
            review_link = cells[9].find_element(By.TAG_NAME, "a").get_attribute('href')

            match (task_name):
                case 'Task 1 - Pre-Assessment MCQ':
                    task_name = 'T01 – Pre-Assessment MCQ'
                
                case 'Task 2 - Getting Started with Your Bootcamp':
                    task_name = 'T02 – Getting Started with Your Bootcamp'
                
                case 'Task 3 - Data Types and Conditional Statements':
                    task_name = 'T03 – Data Types and Conditional Statements'
                
                case 'Task 4 - Iteration':
                    task_name = 'T04 – Iteration'
                
                case 'Task 5 - Build Your Brand – Technical Portfolio':
                    task_name = 'T05 – Build Your Brand – Technical Portfolio'
                
                case 'Task 6 - Programming with User-defined Functions':
                    task_name = 'T06 – Programming with User-defined Functions'
                
                case 'Task 7 - Handling Strings, Lists and Dictionaries':
                    task_name = 'T07 – Handling Strings, Lists and Dictionaries'
                
                case 'Task 8 - IO Operations':
                    task_name = 'T08 – IO Operations'
                
                case 'Task 9 - OOP – Classes':
                    task_name = 'T09 – OOP – Classes'
                
                case 'Task 10 - Build Your Brand – Preparing to Enter the Job Market':
                    task_name = 'T10 – Build Your Brand – Preparing to Enter the Job Market'
                
                case 'Task 11 - Datasets and DataFrames':
                    task_name = 'T11 – Datasets and DataFrames'
                
                case 'Task 12 - Data Visualisation - Simple':
                    task_name = 'T12 – Data Visualisation - Simple'
                
                case 'Task 13 - Data Analysis - Data Cleaning':
                    task_name = 'T13 – Data Analysis - Data Cleaning'
                
                case 'Task 14 - Data Analysis - Preprocessing':
                    task_name = 'T14 – Data Analysis - Preprocessing'
                
                case _:
                    print(f'[WARN] {task_name} is not yet automated! (course: {course_lvl})')
                    continue

            data_result = {
                'course_lvl': course_lvl,
                'student_id': student_id,
                'task_name': task_name,
                'review_link': review_link
            }

            # Optionally, print the result for debugging purposes
            print(data_result)

            review_data_list.append(data_result)

    driver.quit()
    return review_data_list


def get_review(url: str, driver: webdriver.Edge):
    # Open the URL
    driver.get(url)
    
    # Enter username
    input_username = driver.find_element(By.NAME, 'username')
    input_username.send_keys("brandenvs@hyperiondev.com")
    time.sleep(2)  # Optional: Use only if absolutely necessary

    # Enter password
    input_password = driver.find_element(By.NAME, 'password')
    input_password.send_keys("fTpX5U&Y7l&0%*3c")
    input_password.send_keys(Keys.RETURN)  # Press Enter to log in
    time.sleep(3)  # Optional: Use only if absolutely necessary

    # Wait for the quotes to be loaded and click the link
    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="format"]'))
    )
    review_text_link = link.get_attribute('href')  # Perform the click action

    driver.get(review_text_link)

    time.sleep(3)

    review = driver.find_element(By.CSS_SELECTOR, "pre[style='word-wrap: break-word; white-space: pre-wrap;']")

    review_text = review.text

    driver.quit()
    return review_text
