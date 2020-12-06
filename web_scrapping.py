import selenium
import json
import time
import re
import string
import requests
import bs4
import math
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


#This is the English version of the booking domain
domain =  'https://www.booking.com/index.html?lang=en-us'


def prepare_driver(url):
    '''Returns a Firefox Webdriver.'''
    options = Options()
    #options.add_argument('-headless')
    driver = Firefox(executable_path='geckodriver', options=options)
    driver.get(url)
    wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ss')))
    return driver


def fill_form(driver, search_argument):
    '''Finds all the input tags in form and makes a POST requests.'''
    search_field = driver.find_element_by_id('ss')
    search_field.send_keys(search_argument)
    # We look for the search button and click it
    driver.find_element_by_class_name('sb-searchbox__button').click()
    wait = WebDriverWait(driver, timeout=10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sr-hotel__title')))


def scrape_results(driver, n_results, n_reviews):
    '''Returns the data from n_results amount of results.'''

    accommodations_urls = list()
    accommodations_data = list()

    for accomodation_title in driver.find_elements_by_class_name('sr-hotel__title'):
        accommodations_urls.append(accomodation_title.find_element_by_class_name('hotel_name_link').get_attribute('href'))

    for url in range(0, n_results):
        if url == n_results:
            break
        url_data = scrape_accommodation_data(driver, accommodations_urls[url], n_reviews)
        accommodations_data.append(url_data)

    return accommodations_data


def scrape_accommodation_data(driver, accommodation_url, n_reviews):
    '''Visits an accommodation page and extracts the data.'''

    if driver == None:
        driver = prepare_driver(accommodation_url)

    driver.get(accommodation_url)
    time.sleep(5)

    accommodation_fields = dict()

    # Get the Hotel name to print
    hotel_name = driver.find_element_by_id('hp_hotel_name').text
    print(hotel_name + "\n")

    # Get the accommodation name
    accommodation_fields['name'] = driver.find_element_by_id('hp_hotel_name').text.strip('Hotel')

    # Get the accommodation score
    accommodation_fields['score'] = driver.find_element_by_class_name(
        'bui-review-score--end').find_element_by_class_name('bui-review-score__badge').text

    # Get the accommodation location
    accommodation_fields['location'] = driver.find_element_by_id('showMap2').find_element_by_class_name(
        'hp_address_subtitle').text

    # Get the accommodation coordinates
    accommodation_fields['latlng'] = driver.find_element_by_id('hotel_address').get_attribute("data-atlas-latlng")

    # Get the most popular facilities
    accommodation_fields['popular_facilities'] = list()
    facilities = driver.find_element_by_class_name('hp_desc_important_facilities')


    # click on the first image to open the image carousel
    driver.find_element_by_class_name('bh-photo-grid-item').click()

    # find the number of images for every hotel
    tmp1 = driver.find_element_by_class_name('bh-photo-modal-caption-left').text
    tmp = tmp1.split()
    img_number = int(tmp[2])
    print(img_number)

    accommodation_fields['images'] = list()
    # loop through every image to save the link
    for image in range(img_number-1):
        img_href = driver.find_element_by_class_name('bh-photo-modal-image-element').find_element_by_tag_name('img').get_attribute('src')
        #print(img_href)
        accommodation_fields['images'].append(img_href)
        driver.find_element_by_class_name('bh-photo-modal-image-element').click()
    print("Total images are: " + str(img_number-1))

    # end of loop - return to the previous hotel page
    # will do this by sending the Escape click
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()


    for facility in facilities.find_elements_by_class_name('important_facility'):
        accommodation_fields['popular_facilities'].append(facility.text)

    #Show the reviews of the hotel
    driver.find_element_by_id('show_reviews_tab').click()
    time.sleep(5)

    # find the number of pages with the reviews results
    rev_pages = driver.find_element_by_class_name("bui-review-score__text").text
    tmp = rev_pages.split()
    rev_numbers = int(tmp[0].replace(",",""))
    rev_pages =math.ceil( rev_numbers /10)
    print ("The total number of reviews is: " + str(rev_numbers)  + "\n")
    print ("The total number of pages with reviews is: " + str(rev_pages) + "\n\n")

    accommodation_fields['reviews'] = list()
    #Loop through all pages

    if (rev_pages>n_reviews):  #this is the maximum number of pages to get data
        rev_pages=n_reviews

    for page in range(rev_pages):
        #print("PAGE " + str(page+1) + " from " + str(rev_pages) + "\n")

        if page != 0 :
            rev_link = driver.find_element_by_class_name('pagenext').get_attribute('href')
            driver.get(rev_link)
            time.sleep(5)
        reviews = driver.find_elements_by_class_name('c-review__body')  # this is the first page
        ii = 0
        for rev in reviews:
            #print(str(ii + 1) + ". " + rev.text)
            accommodation_fields['reviews'].append(rev.text)
            ii = ii + 1
       
    return accommodation_fields


if __name__ == '__main__':

    num_of_hotels = 1
    max_num_of_reviews = 13

    try:
        driver = prepare_driver(domain)
        fill_form(driver, 'Athens')
        accommodations_data = scrape_results(driver, num_of_hotels, max_num_of_reviews)
        with open('booking_data.json', 'w', encoding='utf8') as f:
            json.dump(accommodations_data, f, ensure_ascii=False, indent=4)
    finally:
        driver.quit()
