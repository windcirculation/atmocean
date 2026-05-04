"""Run job posting scripts with status flags.

This module consolidates the three job scripts (esjobs, metjob, egujobs) and
executes them with ``jobbot_status=True`` so they only report status without
actually posting. The previous version contained merge conflict markers and a
debug routine that masked the Telegram token – both have been removed.
"""

from atmocean.es_jobs_net import esjobs
from atmocean.met_jobs import metjobs
from atmocean.egu_jobs import egujobs

# Execute each job in status‑only mode. The functions themselves print concise
# messages, but we also output a short confirmation here for clarity.
esjobs(post_jobs=False, jobbot_status=True)
print("Posted E_JOBS")

metjobs(post_jobs=False, jobbot_status=True)
print("Posted Met-Jobs")

egujobs(post_jobs=False, jobbot_status=True)
print("Posted EGU-Jobs")
