from datetime import datetime
from bs4 import BeautifulSoup
import requests
import os
import re
import pytz
from job_bot import postbot
from api_token import api_key

# def init_bot():
bot_token = api_key()

def esjobs(post_jobs=True, jobbot_status=False, current_date=None):
    if jobbot_status:
        sign1 = f"\n----- ** {datetime.now().strftime('%Y-%b-%d')} ** -----"
        sign2 = f"\nEarth Science Jobs"
        message_text = f" *{'Job_Bot Status: Active'}* {sign1}{sign2}"
        postbot(bot_token, message_text)
    
    if post_jobs:
        if current_date is None:
            # Get the current time in the Hawaii timezone
            hawaii_timezone = pytz.timezone('Pacific/Honolulu')
            current_date_hawaii = datetime.now(hawaii_timezone)    
            current_date = current_date_hawaii
            current_time = current_date.strftime("%B %Y")
        else:
            current_date = datetime.strptime(current_date, "%Y-%m-%d")
            current_time = current_date.strftime("%B %Y")
        # print(current_time)
        url = "https://mailman.ucar.edu/pipermail/es_jobs_net/"

        # Define user-agent and headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; \
            x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,\
            application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "mailman.ucar.edu",
            "If-Modified-Since": "Thu, 19 Oct 2023 09:12:44 GMT",
            "If-None-Match": "\"1a8c-6080e289aa9c3\"",
            "Sec-Ch-Ua": "\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"macOS\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1"
        }

        # Send a request to the URL
        response = requests.get(url, headers=headers)
        page_content = response.text

        soup = BeautifulSoup(page_content, "html.parser")

        # Find the link to the latest thread (October 2023)
        latest_thread_link = None
        for row in soup.find_all("tr"):
            cells = row.find_all("td")
            if cells and current_time in cells[0].get_text():
                latest_thread_link = row.find("a", href=True)["href"]
                break

        tempPath = latest_thread_link.split("/")[0]
        print(tempPath)

        # Construct the URL for the latest thread
        if latest_thread_link:
            latest_thread_url = f"{url.rstrip('/')}/{latest_thread_link}"


            # Send a request to the latest thread's URL and scrape its content
            response_latest_thread = requests.get(latest_thread_url, headers=headers)
            latest_thread_content = response_latest_thread.text

            # Parse and extract data from the latest thread's content using BeautifulSoup
            latest_thread_soup = BeautifulSoup(latest_thread_content, "html.parser")

            # Define keywords to search for
            keywords = ["phd", "ph.d.", "doctoral", "ms ", "m.s.", "master", "assistantship", "fellowship"]

            # Initialize a list to store the links containing the keywords
            filtered_links = []

            # Loop through the links and check if they contain any of the keywords
            for link in latest_thread_soup.find_all("a", href=True):  # Fixed this line
                for keyword in keywords:
                    if re.search(keyword, link.get_text(), re.I):
                        filtered_links.append(link['href'])

            # Print the filtered links
            for link in filtered_links:
        #             print(f"posting {link}")
                # print(os.path.join(url, tempPath, link))
                full_url = os.path.join(url, tempPath, link)
                # Send a request to the filtered link and scrape its content
                response_filtered_link = requests.get(full_url, headers=headers)
                filtered_link_content = response_filtered_link.text

                # Parse and extract data from the filtered link's content using BeautifulSoup
                filtered_link_soup = BeautifulSoup(filtered_link_content, "html.parser")
                # You can perform additional parsing or extraction here, or simply print the content
                # print("Content of filtered link:", full_url)        
        #         print(filtered_link_soup.get_text())  # Print the text content of the filtered link
    #             print("--------------------------------------\n")
                pub_date = filtered_link_soup.find("i").get_text()
                format_str = '%a %b %d %H:%M:%S %Y'
                date_time_str = pub_date[:19] + pub_date[23:]

                if len(date_time_str) == 24:
                    date_time_ = datetime.strptime(date_time_str, format_str)
                    date_time_str_formatted = date_time_.strftime("%Y-%m-%d")

                    if date_time_.date() == current_date.date():
                        print(date_time_str_formatted, current_date.strftime('%Y-%m-%d'))

                        # Extract the header
                        header = filtered_link_soup.find("h1")  # Assuming the header is within an h2 element
                        if header:
                            header_text = header.get_text().removeprefix('[ES_JOBS_NET] ')
                            # print("Header:")
                            # print(header_text)

                        # Extract the body
                        body = filtered_link_soup.find("pre")  # Adjust class as needed
                        if body:
                            body_text = body.get_text()
                            # print("\nBody:")
                            split_index = body_text.find("-------------- next part --------------")
                            if split_index != -1:
                            # Keep only the part before "-------------- next part --------------"
                                body_text = body_text[:split_index]
                            # print(body_text)
                        sign1 = f"\n----- ** {current_date} ** -----"
                        sign2 = f"\n"
                        message_text = f" *{header_text.title()}* \n\n{body_text}{sign1}{sign2}"
                        postbot(bot_token, message_text)
                        # print(message_text)

# if __name__ == "__main__":
#     esjobs(current_date=None)