# booking_scraper
This is a program in python for web scraping http://www.booking.com for gathering touristic data. The program is used to extract the following information:

1. Hotel name
2. Hotel rating
3. Hotel address
4. Hotel coordinates (long/lat)
5. Hotel Popular Facilities
6. Hotel pictures (links of images)
7. Reviews from residents.

All data are saved in a json format file for further processing.

## Parameters
num_of_hotels: the total number of hotels to scrap data from
max_num_of_reviews: the maximum number of review comments to be saved (for some well-known hotels, there are over 5K reviews)
