from pathlib import Path
import time
import json
import asyncio
from pyppeteer import launch

class SpotifyBrowserToken:

	def __init__( self , username=None , password=None , save_path=None , regeneration_time_minimum=300 ):
		self.username = username
		self.password = password
		self.save_path = save_path
		self.regeneration_time_minimum = regeneration_time_minimum
		if self.save_path is None:
			self.save_path_posix = Path( Path.home() , ".config" , "personal" , "spotify_browser_token.json" )
			self.save_path = str( self.save_path_posix )
			Path( Path.home() , ".config" , "personal" ).mkdir( parents=True , exist_ok=True )
		else:
			self.save_path_posix = Path( self.save_path )
		if self.save_path_posix.is_file():
			self.token_info = self.read_json( self.save_path )
		else:
			self.token_info = {}

	def read_json( self , file_path ):
		with open( file_path ) as f:
			return json.load( f )

	def write_json( self , file_path , python_object ):
		with open( file_path , 'w', encoding='utf-8' ) as f:
			json.dump( python_object , f , ensure_ascii=False , indent=4 )

	async def login_and_get_token_info( self ):
		browser = await launch()
		page = await browser.newPage()
		await page.goto( "https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2F" )
		await page.type( "#login-username" , self.username )
		await page.type( "#login-password" , self.password )
		await page.click( "#login-button" )
		await page.waitForNavigation()
		token_info = await page.evaluate('''() => {
			const token_script = document.getElementById( "config" );
			const token_json = token_script.text.trim();
			const token_info = JSON.parse( token_json );
			return token_info;
		}''')
		await browser.close()
		return token_info

	def generate( self ):
		token_info = asyncio.get_event_loop().run_until_complete( self.login_and_get_token_info() )
		seconds_left = ( ( int( token_info[ "accessTokenExpirationTimestampMs" ] ) // 1000 ) - int( time.time() ) )
		self.token_info = {
			"access_token": token_info[ "accessToken" ] ,
			"expire_time": token_info[ "accessTokenExpirationTimestampMs" ] ,
			"seconds_left": seconds_left
		}
		self.write_json( self.save_path , self.token_info )

	def refresh( self ):
		try:
			if "seconds_left" not in self.token_info:
				print("Token Info Empty, Refreshing")
				self.generate()
				return self.token_info
			self.token_info[ "seconds_left" ] = ( ( int( self.token_info[ "expire_time" ] ) // 1000 ) - int( time.time() ) )
			if self.token_info[ "seconds_left" ] < self.regeneration_time_minimum:
				print( "Spotify Token is About to Expire in " + str( self.token_info[ "seconds_left" ] ) + " Seconds" )
				self.generate()
				return self.token_info
			else:
				print( "Spotify Token is Still Valid for " + str( self.token_info[ "seconds_left" ] ) + " Seconds" )
				return self.token_info
		except Exception as e:
			print( "Couldn't Regenerate Spotify Token" )
			print( e )
			return False