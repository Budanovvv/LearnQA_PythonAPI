import requests
import time


url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# Create token
response = requests.get(url)
token = None
if response.json()["token"]:
    token = response.json()["token"]
    estimate = response.json()["seconds"]
    print(response.json())
else:
    print("Token doesnt created")

# Check that status is Job is NOT ready
response = requests.get(url, params={"token": token})
if response.json()["status"] == "Job is NOT ready":
    print(response.json())
else:
    print("Job is NOT started")

# Waiting for job
print(f"Need to waite {estimate} seconds")
time.sleep(estimate)

# Check that status is Job is ready
response = requests.get(url, params={"token": token})
if response.json()["status"] == "Job is ready":
    print(response.json())
else:
    print("Some error")
