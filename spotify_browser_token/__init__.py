import JSONFileOBJDB
from pathlib import Path
import time
import asyncio
from pyppeteer import launch

class SpotifyBrowserToken:

	def __init__( self , options={} ):

		self.options = options

		if "save_path" in self.options:
			self.options[ "save_path_posix" ] = Path( self.options[ "save_path" ] )
		else:
			self.init_fresh_db()
		if self.options[ "save_path_posix" ].is_file():
			self.db = JSONFileOBJDB.create({
					"posix_obj": self.options[ "save_path_posix" ]
				})
		else:
			self.init_fresh_db()

		if "username" in self.options and "password" in self.options:
			self.db.self[ "username" ] = self.options[ "username" ]
			self.db.self[ "password" ] = self.options[ "password" ]
			self.db.save()

		if "regeneration_time_minimum" not in self.options:
			self.options[ "regeneration_time_minimum" ] = 300

		self.db.self[ "regeneration_time_minimum" ] = self.options[ "regeneration_time_minimum" ]
		self.db.save()


	def init_fresh_db( self ):
		self.options[ "save_path_posix" ] = Path( Path.home() , ".config" , "personal" , "spotify_browser_token.json" )
		self.options[ "save_path" ] = str( self.options[ "save_path_posix" ] )
		self.db = JSONFileOBJDB.create({
				"posix_obj": self.options[ "save_path_posix" ]
			})
		self.db.save()

	async def fresh_login_and_get_token_info( self ):
		#browser = await launch( args=['--headless', '--single-process'] )
		browser = await launch( {'headless': True} )
		page = await browser.newPage()
		await page.goto( "https://google.com/" )
		await page.waitForNavigation()
		print( "we at least went somwhere" )
		await page.goto( "https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2F" )
		await page.waitForNavigation()
		print( "we made it to the login page" )
		await page.type( "#login-username" , self.db.self[ "username" ] )
		await page.type( "#login-password" , self.db.self[ "password" ] )
		await page.click( "#login-button" )
		await page.waitForNavigation()
		print( "we logged in" )
		cookies = await page.cookies()
		token_info = await page.evaluate('''() => {
			const token_script = document.getElementById( "config" );
			const token_json = token_script.text.trim();
			const token_info = JSON.parse( token_json );
			return token_info;
		}''')
		await browser.close()
		result = {
			"cookies": cookies ,
			"token_info": token_info ,
		}
		return token_info

	async def cookie_login_and_get_token_info( self ):
		browser = await launch()
		page = await browser.newPage()
		for cookie in self.db.self[ "cookies" ]:
			await page.setCookie( cookie )
		await page.goto( "https://open.spotify.com" )
		await page.waitForNavigation()
		cookies = await page.cookies()
		token_info = await page.evaluate('''() => {
			const token_script = document.getElementById( "config" );
			const token_json = token_script.text.trim();
			const token_info = JSON.parse( token_json );
			return token_info;
		}''')
		await browser.close()
		result = {
			"cookies": cookies ,
			"token_info": token_info ,
		}
		return result

	def are_cookies_still_valid( self ):
		if "cookies" in self.db.self:
			for cookie in self.db.self[ "cookies" ]:
				if "expires" in cookie:
					if cookie[ "expires" ] - int( time.time() ) < 3:
						return False
		return True

	def generate( self ):
		if self.are_cookies_still_valid() == True:
			print( "cookies still valid , re-using" )
			result = asyncio.get_event_loop().run_until_complete( self.cookie_login_and_get_token_info() )
		else:
			print( "some cookie is expired , re-logging in" )
			result = asyncio.get_event_loop().run_until_complete( self.fresh_login_and_get_token_info() )
		print( result )
		self.db.self[ "cookies" ] = result[ "cookies" ]
		seconds_left = ( ( int( result[ "token_info" ][ "accessTokenExpirationTimestampMs" ] ) // 1000 ) - int( time.time() ) )
		self.db.self[ "token_info" ] = {
			"access_token": result[ "token_info" ][ "accessToken" ] ,
			"expire_time": result[ "token_info" ][ "accessTokenExpirationTimestampMs" ] ,
			"seconds_left": seconds_left
		}
		self.db.save()

	def refresh( self ):
		try:

			if "token_info" not in self.db.self:
				print( "Token Info Empty, Refreshing" )
				self.generate()
				return self.db.self[ "token_info" ]

			if "seconds_left" not in self.db.self[ "token_info" ]:
				print( "Token Info Empty, Refreshing" )
				self.generate()
				return self.db.self[ "token_info" ]

			self.db.self[ "token_info" ][ "seconds_left" ] = ( ( int( self.db.self[ "token_info" ][ "expire_time" ] ) // 1000 ) - int( time.time() ) )

			if self.db.self[ "token_info" ][ "seconds_left" ] < self.db.self[ "regeneration_time_minimum" ]:
				print( "Spotify Token is About to Expire in " + str( self.db.self[ "token_info" ][ "seconds_left" ] ) + " Seconds" )
				self.generate()
				return self.db.self[ "token_info" ]
			else:
				print( "Spotify Token is Still Valid for " + str( self.db.self[ "token_info" ][ "seconds_left" ] ) + " Seconds" )
				return self.db.self[ "token_info" ]

		except Exception as e:
			print( "Couldn't Regenerate Spotify Token" )
			print( e )
			return False


if __name__ == '__main__':
	import json
	personal_file_path = str( Path( Path.home() , ".config" , "personal" , "raspi_chromecast_box.json" ) )
	with open( personal_file_path ) as f:
		Personal = json.load( f )
	spotify_token_generator = SpotifyBrowserToken({
			"username": Personal[ "personal" ][ "spotify" ][ "username" ] ,
			"password": Personal[ "personal" ][ "spotify" ][ "password"] ,
			"regeneration_time_minimum" : 300
		})
	spotify_token_info = spotify_token_generator.refresh()
	print( spotify_token_info )