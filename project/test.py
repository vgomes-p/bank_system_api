import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNzYwMTExMTUzfQ.xx6EA9UYsafVCwIQbBdOq6F9Annjd4San2f20IEj3V4"
}

reques = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(reques)
print(reques.json())