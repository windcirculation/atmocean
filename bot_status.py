from es_jobs_net import esjobs
from met_jobs import metjobs
from egu_jobs import egujobs

esjobs(post_jobs=False, jobbot_status=True)
print("Posted E_JOBS")

metjobs(post_jobs=False, jobbot_status=True)
print("Posted Met-Jobs")

egujobs(post_jobs=False, jobbot_status=True)
print("Posted EGU-Jobs")

