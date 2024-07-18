import subprocess
import os

def handler(request):
    try:
        # Run the post_jobs.py script
        result = subprocess.run(['python', 'post_jobs.py'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        return {
            "statusCode": 200,
            "body": result.stdout
        }
    except subprocess.CalledProcessError as e:
        return {
            "statusCode": 500,
            "body": f"Error: {e.stderr}"
        }