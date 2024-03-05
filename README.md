# Parallel-Web-Scraper
## Compile and run Instructions
Install beautifulsoup by entering in the command line 'pip install requests beautifulsoup4'   
Then run the scraper with 'python3 scraper.py'
## Problem Statement:
Web scraping is a process of writing scripts to parse and collect specific data from a website. These scripts will go through the given HTML code of a site to collect data the user wants and store it however told. When running this process for many pages, this can get to be a slow process. We are looking to increase the efficiency of web scraping tools by adding multi threading functionality, whether that is to scrape multiple sites or pages at once or look for separate data on one page concurrently.
## Technique: 
We currently plan to use python to implement our multi threading, as there is a good web scraping library, beautiful soup, that is usable in python. This will allow us to focus on how to make the multi threading process optimal without having to work through the exact details of scraping HTML data. We think a good site to test our methods on would be Wikipedia, where we can select a certain category of pages and scrape through a subset of them, knowing they will follow some kind of organizational pattern.

## Working Rough Draft of paper
https://docs.google.com/document/d/1b7JOQNewGdG5Lt22GBq4MwKcuJuCmivSBnVPjZQsDX0/edit?usp=sharing

## Challenges, tasks, and goals
- Parallelize web scraping functionality:
  - Create threads and give subset of input list
  - Add performance data collecting to compare
- Web scraper:
  - Collecting structured data
    - info boxes, data tables, etc.
  - Provide context to references
  - Create user input for list of links
  - Finalize testingdataset to scrape
- Stretch goal:
  - include NLP to gather relevant data for user
