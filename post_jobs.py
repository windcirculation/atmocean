from es_jobs_net import esjobs
from met_jobs import metjobs
from egu_jobs import egujobs
from datetime import datetime

def post_jobs_and_handle_errors(job_function, job_args, job_name, current_date=None):
    try:
        job_function(*job_args, current_date=current_date)  # Pass current_date as a keyword argument
        print(f"Posted {job_name}")
    except Exception as e:
        print(f"Error posting {job_name}: {str(e)}")


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def generate_date_list(start_date, end_date=None):
    if end_date is None:
        end_date = datetime.now() - timedelta(days=1)
    start = datetime.strptime(start_date, '%Y-%m-%d')
    date_list = []

    while start <= end_date:
        date_list.append(start.strftime('%Y-%m-%d'))
        start += relativedelta(days=1)

    return date_list

# # Example usage
# from_date = '2024-05-09'
# to_date = None # datetime(2024,3,10)
# date_list = generate_date_list(from_date, to_date)

# for date in date_list:
#     print(f"Posting Jobs for day: {date}")
#     # Call your functions here for each date
#     post_jobs_and_handle_errors(esjobs, [], "ES_JOBS", current_date=date)
#     post_jobs_and_handle_errors(metjobs, [], "Met-Jobs", current_date=date)
#     post_jobs_and_handle_errors(egujobs, [], "EGU-Jobs", current_date=date)


current_date = datetime.now().strftime('%Y-%m-%d')
print(f"Posting Jobs for day: {current_date}")

# current_date = '2023-12-16'
# print(f"Posting Jobs for day: {current_date}")

## ES_JOBS
post_jobs_and_handle_errors(esjobs, [], "ES_JOBS", current_date=current_date)

## Met-Jobs
post_jobs_and_handle_errors(metjobs, [], "Met-Jobs", current_date=current_date)

## EGU-Jobs
post_jobs_and_handle_errors(egujobs, [], "EGU-Jobs", current_date=current_date)


# from es_jobs_net import esjobs
# from met_jobs import metjobs
# from egu_jobs import egujobs
# from datetime import datetime


# # from job_bot import postbot
# # from es_jobs_net import esjobs
# # from api_token import api_key
# # from met_jobs import metjobs

# ## ES_JOBS
# # bot_token = api_key()
# # message_text = esjobs()
# # postbot(bot_token, message_text)
# date = datetime.now().strftime('%Y-%m-%d')
# print("Date:", date)

# esjobs()
# print("Posted ES_JOBS")

# ## Met-Jobs
# # message_text1 = metjobs()
# # postbot(bot_token, message_text1)

# metjobs()
# print("Posted Met-Jobs")


# ## EGU-Jobs
# egujobs()
# print("Posted EGU-Jobs")

