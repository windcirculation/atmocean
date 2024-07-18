from datetime import datetime
from bs4 import BeautifulSoup
import requests
import os
import re
from job_bot import postbot
from api_token import api_key
import feedparser
import pytz


bot_token = api_key()

def metjobs(post_jobs=True, jobbot_status=False, current_date=None):
    if jobbot_status:
        sign1 = f"\n----- ** {datetime.now().strftime('%Y-%b-%d')} ** -----"
        sign2 = f"\nMet-Jobs"
        message_text = f" *{'Job_Bot Status: Active'}* {sign1}{sign2}"
        postbot(bot_token, message_text)
    
    if post_jobs:
        if current_date is None:
            # Set the time zone to Hawaii Standard Time (HST)
            hawaii_timezone = pytz.timezone('Pacific/Honolulu')
            current_date = datetime.now(hawaii_timezone).strftime("%Y-%m-%d")
        else:
            current_date = datetime.strptime(current_date, "%Y-%m-%d")
        # Replace this URL with the URL of the RSS feed you want to scrape
        rss_url = "https://maillists.reading.ac.uk/scripts/wa-READING.exe?RSS&L=MET-JOBS&v=2.0&LIMIT=50"

        # Define headers for your requests to mimic a web browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
            'Cache-Control': 'max-age=0',
            'Referer': 'http://localhost:8888/',
            'Sec-Ch-Ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'authority': 'maillists.reading.ac.uk',
            'method': 'GET',
            'path': '/scripts/wa-READING.exe?A2=MET-JOBS;45592065.2310D',
            'scheme': 'https',
            'Cookie': 'WALOGIN=RESET; WALOGIN=RESET',
        }

        # Parse the RSS feed
        feed = feedparser.parse(rss_url)

        # Extract and print the information for each item
        for item in feed.entries:
            pub_date = item.published
            author = item.author
            title = item.title
            guid = item.id
            description = item.description
            # print(pub_date)
            # print(pub_date[:24])
            # Convert the pub_date string to a datetime object
            # pub_date_datetime = datetime.strptime(pub_date[:24], "%a, %d %b %Y %H:%M:%S")
            date_format = "%a, %d %b %Y %H:%M:%S %z"
            pub_date_datetime = datetime.strptime(pub_date, date_format)
            # print(pub_date_datetime)

            # Format the datetime object to get the desired date string
            formatted_date_str = pub_date_datetime.strftime('%Y-%m-%d')
            formatted_date_str = datetime.strptime(formatted_date_str, "%Y-%m-%d")
            if formatted_date_str == current_date:
                # print("--------------------")
                # print(formatted_date_str, current_date)
                # Define keywords to search for
                keywords = ["phd", "ph.d.", " doctoral", "ms ", "m.s.", "master", "assistantship", "fellowship"]

                # Initialize a list to store the links containing the keywords
                filtered_links = []

                for keyword in keywords:
                    if re.search(keyword, title, re.I):
                        filtered_links.append(guid)

        #         print(len(filtered_links))
                # Print the filtered links
                # ...
                for link in filtered_links:
    #                 print(link)
    #                 print(current_date)
    #                 print(title)
    #                 print("----------------------")
                    
                    sign1 = f"\n----- ** {current_date.strftime('%Y-%b-%d')} ** -----"
                    sign2 = f"\n--------------------"
                    link1 = f"\n{link}"
                    message_text = f" *{title}* \n\n{link1}{sign1}{sign2}"
                    postbot(bot_token, message_text)
                    # print(message_text)

# if __name__ == "__main__":
    # metjobs()