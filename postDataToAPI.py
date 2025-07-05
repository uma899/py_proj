import requests
import json

# Define the URL of the API endpoint you want to send the POST request to.
# Replace 'https://api.example.com/posts' with your actual API endpoint.
url = 'http://localhost:5050/blogs'

# Define the data you want to send in the POST request body.
# This data is typically sent as JSON for most modern APIs.
# 'title', 'body', and 'userId' are common fields for a blog post or similar resource.


def upload(e):
    payload = {"title":"Blog" +str(e),"about":"fcgvhb cbhjnkm dfbk rtyuk fghk dfghjk200tdfghjk trfghjk fgvbhnjkm gfbhkm",
    "likes": i%3 + i%5,
    "extra":"",
    "image":"https://media.istockphoto.com/id/517188688/photo/mountain-landscape.jpg?s=1024x1024&w=0&k=20&c=z8_rWaI8x4zApNEEG9DnWlGXyDIXe-OmsAyQ5fGPVV8="
    }

    # Optional: Define custom headers if required by the API.
    # For JSON data, it's good practice to set 'Content-Type' to 'application/json'.
    headers = {
        'Content-type': 'application/json; charset=UTF-8',
    }

    print(f"Attempting to send POST request to: {url}")
    print(f"Payload: {payload}")
    print(f"Headers: {headers}")
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    print(f"\nPOST Request successful! Status Code: {response.status_code}")
    response_json = response.json()
    print("Response JSON:")
    print(json.dumps(response_json, indent=4))

for i in range(3, 50):
    upload(i)