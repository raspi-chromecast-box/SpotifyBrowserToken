# Spotify Browser Token

'''
if __name__ == '__main__':
    from spotify_browser_token import SpotifyBrowserToken
    personal_file_path = str( Path( Path.home() , ".config" , "personal" , "raspi_chromecast_box.json" ) )
    with open( personal_file_path ) as f:
        Personal = json.load( f )
    spotify_token_generator = SpotifyBrowserToken( username=Personal[ "personal" ][ "spotify" ][ "username" ] , password=Personal[ "personal" ][ "spotify" ][ "password"] )
    spotify_token_info = spotify_token_generator.refresh()
    print( spotify_token_info )
'''