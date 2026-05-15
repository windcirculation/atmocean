import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from es_jobs_net import esjobs
from met_jobs import metjobs
from egu_jobs import egujobs
from datetime import datetime

def handler(request):
    current_date = datetime.now().strftime('%Y-%m-%d')
    results = []

    for fn, name in [(esjobs, "ES_JOBS"), (metjobs, "Met-Jobs"), (egujobs, "EGU-Jobs")]:
        try:
            fn(current_date=current_date)
            results.append(f"Posted {name}")
        except Exception as e:
            results.append(f"Error posting {name}: {e}")

    return {
        "statusCode": 200,
        "body": "\n".join(results)
    }
