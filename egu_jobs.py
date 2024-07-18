import pytz
import requests
import warnings
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
from job_bot import postbot
from api_token import api_key

# def init_bot():
bot_token = api_key()

def egujobs(post_jobs=True, jobbot_status=False, current_date=None):
    if jobbot_status:
        sign1 = f"\n----- ** {datetime.now().strftime('%Y-%b-%d')} ** -----"
        sign2 = f"\nEGU Jobs"
        message_text = f" *{'Job_Bot Status: Active'}* {sign1}{sign2}"
        postbot(bot_token, message_text)

    if post_jobs:        
        if current_date is None:
            # Get the current time in the Hawaii timezone
            hawaii_timezone = pytz.timezone('Pacific/Honolulu')
            current_date_hawaii = datetime.now(hawaii_timezone)    
            current_date = current_date_hawaii.strftime("%Y-%m-%d")

        base_url0 = 'https://www.egu.eu/jobs/?'
        base_url1 = 'limit=10&sortby=-created_at&sortby=-created_at&'
        base_url2 = 'page=&keywords=&sector=10&employment_level=30'
        base_url = f'{base_url0}{base_url1}{base_url2}'

        # Send an HTTP GET request to the URL
        response = requests.get(base_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the elements you want to scrape
            job_list = soup.find_all('div', class_='media-body')

            for job in job_list:
                job_title = job.find('h2').text.strip()
                job_link = urljoin(base_url, job.find('h2').find('a')['href'])

                # Send a request to the job page
                job_response = requests.get(job_link)
                if job_response.status_code == 200:
                    job_soup = BeautifulSoup(job_response.text, 'html.parser')
                    # Location

                    # Find the "Posted" line
                    posted_line = job_soup.find("div",
                                                class_="col-md-3 mb-2 mb-md-0 strong text-md-right",
                                                string='Posted')

                    # Find the date that follows the "Posted" line
                    if posted_line:
                        posted_date = posted_line.find_next_sibling('div').text.strip()
                        input_format = "%d %B %Y"  # day month year (e.g., "29 September 2023")
                        # Parse the posted_date into a datetime object
                        posted_datetime = datetime.strptime(posted_date,
                                                            input_format).strftime('%Y-%m-%d')
                        posted_datetime =  datetime.strptime(posted_datetime, "%Y-%m-%d")
                        converted_date = datetime.strptime(current_date, "%Y-%m-%d")
                        if posted_datetime == converted_date:
                            # print(posted_datetime)
                            location = job_soup.find("div",
                                class_="col-md-3 mb-2 mb-md-0 strong text-md-right",
                                string="Location"
                                )

                            location_content = location.find_next_sibling(
                                "div").text.strip() if location else "Not specified"

                            # Application deadline
                            application_deadline = job_soup.find(
                                "div",
                                class_="col-md-3 mb-2 mb-md-0 strong text-md-right",
                                string="Application deadline")

                            application_deadline_content = application_deadline.find_next_sibling(
                                "div").text.strip() if application_deadline else "Not specified"

                            # Job description
                            job_description = job_soup.find(
                                "div",
                                class_="col-md-3 mb-2 mb-md-0 strong text-md-right",
                                string="Job description")

                            job_description_content = job_description.find_next_sibling(
                                "div").text.strip() if job_description else "Not specified"

                            # How to apply
                            how_to_apply = job_soup.find(
                                "div",
                                class_="col-md-3 mb-2 mb-md-0 strong text-md-right",
                                string="How to apply"
                            )

                            how_to_apply_content = how_to_apply.find_next_sibling(
                                "div").text.strip() if how_to_apply else "Not specified"

                            # # Print the extracted information
                            # print(f"Title: {job_title}")
                            # print(f"Date Posted: {posted_date}")
                            # print(f"Location: {location_content}")
                            # print(f"Deadline: {application_deadline_content}")
                            # print(f"Job Description:\n{job_description_content}")
                            # print(f"How to Apply:\n{how_to_apply_content}")

                            job_heading = f"*{job_title}* \n\nLocation:\
                            {location_content} \nDate Posted: {posted_date} \
                            \nDeadline: {application_deadline_content}"
                            job_desc = f"\n\nDescription:\n{job_description_content} \
                            \n\nHow to Apply:\n{how_to_apply_content}\n--------"

                            full_post = job_heading+job_desc+"---------"

                            postbot(bot_token, full_post)
                            # print(full_post)