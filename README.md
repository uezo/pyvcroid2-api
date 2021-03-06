# pyvcroid2-api

A RESTful API layer to use VOICEROID2 as a service.

# Featuresπ«

- VOICEROID RESTful APIs: Provides RESTful APIs for VOICEROID2. Uses [pyvcroid2](https://github.com/Nkyoku/pyvcroid2) internally; the Python wrapper for VOICEROID DLL.
- Compressed Audio: Provides the encoding to the format that is supported by ffmpeg and pydub.
- Cache: Returns cache if the requested params are completely same to enhance the perfomance.

# Setupπ 

NOTE: __This library supports Windows OS only.__ Tested on Python 3.8.

1. Install the dependencies:
    - VOICEROID2 (x64 version is required) π https://www.ah-soft.com/history/2020.html
    - ffmpeg: Audio converter π https://ffmpeg.org
    - pydub: Python interface for ffmpeg (... and more features!) π `pip install pydub`
    - FastAPI: API framework π `pip install fastapi`
    - Uvicorn: ASGI server π `pip install uvicorn`

1. Clone this repository.
1. Clone and put [pyvcroid2](https://github.com/Nkyoku/pyvcroid2) into the directory of pyvcroid2-api.

```
pyvcroid2-api-master
βββ pyvcroid2 π Here!
β   βββ __init__.py
β   βββ aitalk.py
β   βββ pyvcroid2.py
βββ pyvcroid2api
β   βββ __init__.py
β   βββ controllers.py
:   :
```

# Tryπ

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

Make sure that `hello.mp3` is created and that sounds "γγγ«γ‘γ―" in Japanese.

# Custom encoder

You can customize `pyvcroid2api.encoder.DefaultEncoder` directly or implement `Encoder` and set it in `run.py` instead.

```python
class MyEncoder(Encoder):
    :

VoiceroidEngine.setup(encoder=MyEncoder)
```

# Thanksβ€οΈ

[pyvcroid2](https://github.com/Nkyoku/pyvcroid2) by [@NkyokuP](https://twitter.com/NkyokuP), is an awesome library that enables us using VOICEROID2 without GUI. pyvcroid2-api is just a wrapper of this library. Thank you!
