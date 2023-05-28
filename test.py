import requests
import json

api_data = json.loads(open("BdBot.json", "r").read())
api_url = "https://api.sumup.com/"

#  https://developer.sumup.com/docs/api/request-authorization-from-users/
response = requests.request("GET", api_url + "authorize",
                            headers=
                            {
                                "Accept": "application/json"
                            },
                            data=json.dumps(
                                {
                                    "response_type": "code",
                                    "client_id": api_data["client_id"],
                                })
                            )

#print(response.text)

#  https://developer.sumup.com/docs/api/generate-a-token/
response = requests.request("POST", api_url + "token",
                            headers=
                            {
                                "Content-Type": "application/json",
                                "Accept": "application/json"
                            },
                            data=json.dumps(
                                {
                                    "grant_type": "authorization_code",
                                    "client_id": api_data["client_id"],
                                    "client_secret": api_data["client_secret"],
                                    "code": ""
                                })
                            )

#print(response.text)



url = "https://api.sumup.com/v0.1/checkouts/"

payload = json.dumps({
  "payment_type": "card"
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)