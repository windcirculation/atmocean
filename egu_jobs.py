import pytz
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urljoin
from job_bot import postbot
from api_token import api_key

# Function to get the bot token from api_token
bot_token = api_key()

def egujobs(post_jobs=True, jobbot_status=False, current_date=None, verbose=False):
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

        if verbose:
            print(f"Bot token: {bot_token}")
            print(f"Current date in Hawaii timezone: {current_date}")

        base_url = 'https://www.egu.eu/jobs/?limit=10&sortby=-created_at&page=1&keywords=&sector=10&sector=20&sector=30&employment_level=30'
        if verbose:
            print(f"Base URL: {base_url}")

        # Send an HTTP GET request to the URL
        response = requests.get(base_url)
        if verbose:
            print(f"HTTP response status code: {response.status_code}")

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')
            if verbose:
                print(f"Page title: {soup.title.string if soup.title else 'No title'}")

            # Find the elements you want to scrape
            job_list = soup.find_all('div', class_='media-body')
            if verbose:
                print(f"Number of job listings found: {len(job_list)}")

            for job in job_list:
                job_title = job.find('h2').text.strip()
                job_link = urljoin(base_url, job.find('h2').find('a')['href'])
                if verbose:
                    print(f"Job title: {job_title}")
                    print(f"Job link: {job_link}")

                # Send a request to the job page
                job_response = requests.get(job_link)
                if verbose:
                    print(f"Job page response status code: {job_response.status_code}")

                if job_response.status_code == 200:
                    job_soup = BeautifulSoup(job_response.text, 'html.parser')

                    # Find the "Posted" line
                    posted_line = job_soup.find("div", class_="col-md-3 mb-2 mb-md-0 strong text-md-right", string='Posted')

                    # Find the date that follows the "Posted" line
                    if posted_line:
                        posted_date = posted_line.find_next_sibling('div').text.strip()
                        if verbose:
                            print(f"Posted date: {posted_date}")
                        input_format = "%d %B %Y"  # day month year (e.g., "29 September 2023")
                        # Parse the posted_date into a datetime object
                        posted_datetime = datetime.strptime(posted_date, input_format).strftime('%Y-%m-%d')
                        posted_datetime = datetime.strptime(posted_datetime, "%Y-%m-%d")
                        converted_date = datetime.strptime(current_date, "%Y-%m-%d")
                        if verbose:
                            print(f"Posted date (formatted): {posted_datetime}")
                            print(f"Converted date: {converted_date}")
                        
                        # Revert back to exact date matching if desired
                        # if posted_datetime == converted_date:

                        # Adjust date comparison logic for broader range (past week)
                        date_range_start = converted_date - timedelta(days=7)
                        date_range_end = converted_date
                        if date_range_start <= posted_datetime <= date_range_end:
                            # Location
                            location = job_soup.find("div", class_="col-md-3 mb-2 mb-md-0 strong text-md-right", string="Location")
                            location_content = location.find_next_sibling("div").text.strip() if location else "Not specified"
                            if verbose:
                                print(f"Location: {location_content}")

                            # Application deadline
                            application_deadline = job_soup.find("div", class_="col-md-3 mb-2 mb-md-0 strong text-md-right", string="Application deadline")
                            application_deadline_content = application_deadline.find_next_sibling("div").text.strip() if application_deadline else "Not specified"
                            if verbose:
                                print(f"Application deadline: {application_deadline_content}")

                            # Job description
                            job_description = job_soup.find("div", class_="col-md-3 mb-2 mb-md-0 strong text-md-right", string="Job description")
                            job_description_content = job_description.find_next_sibling("div").text.strip() if job_description else "Not specified"
                            if verbose:
                                print(f"Job description: {job_description_content}")

                            # How to apply
                            how_to_apply = job_soup.find("div", class_="col-md-3 mb-2 mb-md-0 strong text-md-right", string="How to apply")
                            how_to_apply_content = how_to_apply.find_next_sibling("div").text.strip() if how_to_apply else "Not specified"
                            if verbose:
                                print(f"How to apply: {how_to_apply_content}")

                            # Format the job post
                            job_heading = f"*{job_title}*\n\nLocation: {location_content}\nDate Posted: {posted_date}\nDeadline: {application_deadline_content}"
                            job_desc = f"\n\nDescription:\n{job_description_content}\n\nHow to Apply:\n{how_to_apply_content}\n--------"

                            full_post = job_heading + job_desc + "---------"
                            # Uncomment the line below to post to Telegram
                            postbot(bot_token, full_post)
                            # print(full_post)
        else:
            print(f"Failed to retrieve jobs. HTTP Status code: {response.status_code}")

# Run the function
# egujobs(post_jobs=True, verbose=True)