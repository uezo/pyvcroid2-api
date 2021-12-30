import requests

params = {"params": {"pitch": 1.3, "speed": 0.5}}

resp = requests.post(
    "http://localhost:8000/api/speech",
    json={
        "text": "こんにちは",
        "format": "mp3",
        "params": {"speed": 0.9, "pitch": 1.05}
    },
    headers={"Content-Type": "application/json"}
)

with open("hello.mp3", "wb") as f:
    f.write(resp.content)
