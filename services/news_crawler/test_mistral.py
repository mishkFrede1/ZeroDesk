import requests

url = "http://localhost:5000/v1/chat/completions"

payload = {
  "model": "mistral-7b-instruct-v0.1.Q4_K_M.gguf",
  "messages": [
    {"role": "user", "content": "Write a good story."},
  ]
}

response = requests.post(url, json=payload)
print("Status code:", response.status_code)
# print("Response text:", response.text)

print(response.json()["choices"][0]["message"]["content"])