# booking_scraper
This is a program in python for web scraping http://www.booking.com for gathering touristic data. The program is used to extract the following information:

* Hotel name
* Hotel rating
* Hotel address
* Hotel coordinates (long/lat)
* Hotel Popular Facilities
* Hotel pictures (links of images)
* Reviews from residents.

All data are saved in a json format file for further processing.

## Parameters
* **`num_of_hotels`**: the total number of hotels to scrap data from
* **`max_num_of_review_pages`**: the maximum number of pages with review comments to be saved (every page stores 10 reviews)
