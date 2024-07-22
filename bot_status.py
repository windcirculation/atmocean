from es_jobs_net import esjobs
from met_jobs import metjobs
from egu_jobs import egujobs
from api_token import api_key
import random

def mask_random_positions(token, num_positions):
    token_list = list(token)
    token_length = len(token_list)
    positions = random.sample(range(token_length), num_positions)
    for pos in positions:
        token_list[pos] = 'X'
    return ''.join(token_list)

# Retrieve the bot token
bot_token = api_key()

# Define the number of positions to mask
num_positions_to_mask = 15  # Adjust this number as needed

# Mask the token at random positions
masked_bot_token = mask_random_positions(bot_token, num_positions_to_mask)

print(masked_bot_token)

esjobs(post_jobs=False, jobbot_status=True)
print("Posted E_JOBS")

metjobs(post_jobs=False, jobbot_status=True)
print("Posted Met-Jobs")

egujobs(post_jobs=False, jobbot_status=True)
print("Posted EGU-Jobs")