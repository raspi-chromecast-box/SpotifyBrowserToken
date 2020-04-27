# Spotify Browser Token

```
sudo apt-get update && sudo apt-get install \
libx11-xcb-dev libxcomposite1 libxcursor1 libxdamage1 \
libxi6 libxtst-dev libnss3-dev libcups2 libxrandr2 \
libasound2 libpangocairo-1.0-0 libatk-bridge2.0-dev libgtk-3-0 -y
```

```
sudo python3 -m pip install pyppeteer SpotifyBrowserToken
```

```
if __name__ == '__main__':
	from pathlib import Path
	import json
	from spotify_browser_token import SpotifyBrowserToken
	personal_file_path = str( Path( Path.home() , ".config" , "personal" , "raspi_chromecast_box.json" ) )
	with open( personal_file_path ) as f:
		Personal = json.load( f )
	spotify_token_generator = SpotifyBrowserToken( username=Personal[ "personal" ][ "spotify" ][ "username" ] , password=Personal[ "personal" ][ "spotify" ][ "password"] )
	spotify_token_info = spotify_token_generator.refresh()
	print( spotify_token_info )
```