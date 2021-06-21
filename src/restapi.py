import requests
import json
def get_prediction(data):
  url = 'https://u57feuo6j3.execute-api.us-east-1.amazonaws.com/my-deploy-stage/churn-resource'
  r = requests.post(url, data=json.dumps(payload))
  response = getattr(r,'_content').decode("utf-8")
  print(response)
  return response

payload = {"data": "23.000,15699309.000,510.000,38.000,4.000,0.000,1.000,1.000,0.000,118913.530,0.000,0.000,1.000,1.000,0.000"}
get_prediction(data=payload)
