scrapeVeilingSylvies.be
====
Scrape auction results from www.veilingsylvies.be

This script will get all auction results from www.veilingsylvies.be. Sylvie's Wine Auctions is an auction house in the Benelux for the sale and purchase of wines.

Results will be stored as a csv file.
Contents of the dataset:
- auction_nr
- year of auction
- month of auction
- lot_nr
- lot_name
- lot_description
- lot_bottle
- lot_bottle_type
- lot_estimate
- lot_my_bid
- result (euro)

Requirements: BeautifulSoup, requests, os & unicodecsv
