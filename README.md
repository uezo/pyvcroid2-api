# pyvcroid2-api

A RESTful API layer to use VOICEROID2 as a service.

# Features💫

- VOICEROID RESTful APIs: Provides RESTful APIs for VOICEROID2. Uses [pyvcroid2](https://github.com/Nkyoku/pyvcroid2) internally; the Python wrapper for VOICEROID DLL.
- Compressed Audio: Provides the encoding to the format that is supported by ffmpeg and pydub.
- Cache: Returns cache if the requested params are completely same to enhance the perfomance.

# Setup🛠

NOTE: __This library supports Windows OS only.__ Tested on Python 3.8.

1. Install the dependencies:
    - VOICEROID2 (x64 version is required) 👉 https://www.ah-soft.com/history/2020.html
    - ffmpeg: Audio converter 👉 https://ffmpeg.org
    - pydub: Python interface for ffmpeg (... and more features!) 👉 `pip install pydub`
    - FastAPI: API framework 👉 `pip install fastapi`
    - Uvicorn: ASGI server 👉 `pip install uvicorn`

1. Clone this repository.
1. Clone and put [pyvcroid2](https://github.com/Nkyoku/pyvcroid2) into the directory of pyvcroid2-api.

```
pyvcroid2-api-master
├── pyvcroid2 👈 Here!
│   ├── __init__.py
│   ├── aitalk.py
│   └── pyvcroid2.py
├── pyvcroid2api
│   ├── __init__.py
│   ├── controllers.py
:   :
```

# Try🚀

Start server.

```
$ uvicorn run:app
```

Install the HTTP client library.

```bash
$ pip install requests
```

Call API.

```bash
$ python client.py
```

Make sure that `hello.mp3` is created and that sounds "こんにちは" in Japanese.

# Custom encoder

You can customize `pyvcroid2api.encoder.DefaultEncoder` directly or implement `Encoder` and set it in `run.py` instead.

```python
class MyEncoder(Encoder):
    :

VoiceroidEngine.setup(encoder=MyEncoder)
```

# Thanks❤️

[pyvcroid2](https://github.com/Nkyoku/pyvcroid2) by [@NkyokuP](https://twitter.com/NkyokuP), is an awesome library that enables us using VOICEROID2 without GUI. pyvcroid2-api is just a wrapper of this library. Thank you!
