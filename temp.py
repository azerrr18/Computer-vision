import requests

api_key = "rDnxbpHdHIfPXGxEsbEKZbvd8ic18vBtroBKAEVu"

r = requests.get( "https://api.nal.usda.gov/fdc/v1/foods/search",
params={"api_key":api_key,"query":"banana","pageSize":1})

print(r.status_code)
print(r.text[:500])