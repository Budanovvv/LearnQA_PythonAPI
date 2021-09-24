import requests
import time


url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# Check that status is Job is NOT ready
token = "something"
estimate = None

response = requests.get(url, params={"token": token})
if response.json()["error"] == "No job linked to this token":
    print(response.json())
else:
    print("Some error")

# Create token
response = requests.get(url)
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
