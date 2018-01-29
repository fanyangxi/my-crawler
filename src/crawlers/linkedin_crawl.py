import argparse
import os
import random
import time
import urlparse2

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LinkedInCrawl:
    def __init__(self):
        pass

    def do_some_thing(self):
        print ("The name is: {0} {1}".format("Yangxi", "FAN"))


def start_crawling(linkedin_email, linkedin_password):
    # parser = argparse.ArgumentParser()
    # parser.add_argument("email", help="linkedin email")
    # parser.add_argument("password", help="linkedin password")
    # args = parser.parse_args()

    browser = webdriver.Chrome()
    browser.get("https://linkedin.com/uas/login")

    email_element = browser.find_element_by_id("session_key-login")
    email_element.send_keys(linkedin_email)

    pass_element = browser.find_element_by_id("session_password-login")
    pass_element.send_keys(linkedin_password)
    pass_element.submit()

    os.system("clear")

    print ("[+] Success! Logged in, bot starting.")
    __view_bot(browser)
    browser.close()


def __view_bot(browser):
    visited = {}
    p_list = []
    count = 0

    while True:
        # Sleep to make sure everything loads.
        # Add random to make us look human.
        time.sleep(random.uniform(6.5, 6.9))
        page = BeautifulSoup(browser.page_source, "html.parser")
        people = __get_people_links(page)
        if people:
            for person in people:
                Id = __get_id(person)
                if Id not in visited:
                    p_list.append(person)
                    visited[Id] = 1
        if p_list:  # If there is people to look at, then look at them
            person = p_list.pop()
            browser.get(person)
            count += 1
        else:  # Otherwise find people via the job pages
            jobs = __get_job_links(page)
            if jobs:
                job = random.choice(jobs)
                root = 'http://www.linkedin.com'
                roots = 'http://www.linkedin.com'
                if root not in job or roots not in job:
                    job = 'https://www.linkedin.com' + job
                browser.get(job)
            else:
                print ("I'm lost, exiting!")
                break
        # Output, make option for this
        print ("[+] " + browser.title + "Visited! \n(" \
              + str(count) + "/" + str(len(p_list)) + ") Visited/Queue")


def __get_people_links(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('herf')
        if url:
            if 'profile/view?id=' in url:
                links.append(url)
    return links


def __get_job_links(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('herf')
        if url:
            if '/jobs' in url:
                links.append(url)
    return links


def __get_id(url):
    p_url = urlparse.urlparse(url)
    return urlparse.parse_qs(p_url.query)['id'][0]
