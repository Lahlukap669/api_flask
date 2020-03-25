# api_flask_music2go
This is aplication programming interface for music2go application in Java. It enables you to save playlists from youtube, and see songs for them... and of course download them. So you insert a name for playlist and its url and you get all the songs from playlist downloaded onto your computer.

## Database
API is actively deployed on HEROKU (https://music2go.herokuapp.com/) and connects to postgres (plpgsql) database which is deployed on ElephantSQL (free up to 25MB). Database also has written functions. That way we don't need to pass SQL Query to DB every single time but we just call a function passing a given parameters.

## !Disclaimer
In some countries act of downloading music from youtube can be illigal or even cause fines. However it is definitely prohibited by youtubes licence and agreements.

<img src="api_fotos/Screenshot_1.png" width="900" height="550"/>
<img src="api_fotos/Screenshot_2.png" width="500" height="250"/>


## Getting started
1. Download the project
2. ```pip install -r /path/to/requirements.txt``` (all needed libraries)
3. position yourself into master directory
3. Run: ```python app.py``` (from terminal)

## Prerequisites
* Python 3.8

## Built with
* Flask
* SQLAlchemy
* youtube_dl
* ffmpeg

## License
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/License_icon-gpl-2.svg/1200px-License_icon-gpl-2.svg.png" width="80" height="80"/>

## Authors
```Python
AUTHOR = "Luka Lah"; ##https://github.com/Lahlukap669
```
