import argparse
import sys
import csv
import os
import time
import random
from linkedin_api import Linkedin
from post import Post
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="LinkedIn Download")
    parser.add_argument("-u", "--username", help="LinkedIn username/email", action='store', dest='username')
    parser.add_argument("-p", "--password", help="LinkedIn password", action='store', dest='password')
    parser.add_argument("-c", "--company", help="company name on LinkedIn", action='store', dest='company')
    parser.add_argument("-m", "--month", help="month of posts to download", action='store', dest='month')
    parser.add_argument("-y", "--year", help="year of posts to download", action='store', dest='year')

    options = parser.parse_args(args)
    return options

def get_posts(username, password, company):
    api = Linkedin(username, password)
    updates = api.get_company_updates(company)
    posts = []

    for update in updates:
        posts.append(Post(update))

    return posts

def filter_posts_by_month_year(posts, month, year):
    dated_posts = []
    for post in posts:
        date = post.get_date()
        if (date.month == month and date.year == year):
            dated_posts.append(post)

    return dated_posts

def write_csv(posts, path):
    with open(path, 'w', encoding="utf-8-sig", newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Date', 'Text', '# Like', '# Empathy', '# Appreciation', '# Praise', '# Interest', '# Shares', 'Link']
        writer.writerow(header)
        
        for post in posts:
            row = [post.get_date().strftime('%Y/%m/%d'), post.get_text(), post.get_num_likes(), post.get_num_empathy(), post.get_num_appreciation(), post.get_num_praise(), post.get_num_interest(), post.get_num_shares(), post.get_link()]
            writer.writerow(row)

def write_to_file(posts, company):
    os.makedirs(company, exist_ok = True)
    file_name = f'{company}.csv'
    file_path = os.path.join(company, file_name)
    write_csv(posts, file_path)

def login_linkedin(username, password):
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 10)

    url = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin/"
    browser.get(url)

    wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-litms-control-urn='login-submit']"))).click()

    return browser

def create_screenshots(posts, company, browser):
    os.makedirs(company, exist_ok = True)

    count = 2
    for post in posts:
        browser.get(post.get_link())
        file_name = f'{count}.png'
        file_path = os.path.join(company, file_name)
        browser.save_screenshot(file_path)
        count = count + 1
        sleep_duration = random.uniform(2, 10)
        time.sleep(sleep_duration)

def logout_linkedin(browser):
    wait = WebDriverWait(browser, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'global-nav__primary-link')][contains(.,'Me')]"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='logout']"))).click()


if __name__ == "__main__":
    userArguments = get_options()

    username = userArguments.username
    password = userArguments.password
    company = userArguments.company

    month = int(userArguments.month)
    year = int(userArguments.year)

    all_posts = get_posts(username, password, company)
    dated_posts = filter_posts_by_month_year(all_posts, month, year)
    write_to_file(dated_posts, company)

    browser = login_linkedin(username, password)
    create_screenshots(dated_posts, company, browser)
    time.sleep(5)
    logout_linkedin(browser)