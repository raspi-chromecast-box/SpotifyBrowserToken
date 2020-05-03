const process = require( "process" );
const path = require( "path" );
const global_package_path = process.argv[ 0 ].split( "/bin/node" )[ 0 ] + "/lib/node_modules";
const puppeteer = require( path.join( global_package_path ,  "puppeteer" ) );
//const chrome_cookies = require( path.join( global_package_path ,  "chrome-cookies-secure" ) );
const JFODB = require( path.join( global_package_path ,  "jsonfile-obj-db" ) );

const SPOTIFY_USERNAME = false;
const SPOTIFY_PASSWORD = false;

// // First Run
// ( async ()=> {
// 	const spotify_login_save = new JFODB( "spotify_login_save" );
// 	spotify_login_save.self[ "spotify_username" ] = SPOTIFY_USERNAME;
// 	spotify_login_save.self[ "spotify_password" ] = SPOTIFY_PASSWORD;
// 	const browser = await puppeteer.launch( { headless: true } );
// 	const page = await browser.newPage();
// 	await page.setViewport( { width: 1200 , height: 720 } )
// 	await page.goto( "https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2F" , { waitUntil: "networkidle0" } );
// 	await page.type( "#login-username" , spotify_login_save.self[ "spotify_username" ] || SPOTIFY_USERNAME );
// 	await page.type( '#login-password', spotify_login_save.self[ "spotify_password" ] || SPOTIFY_PASSWORD );
// 	await page.click( "#login-button" );
// 	await page.waitForNavigation( { waitUntil: "networkidle0" } );
// 	// for ( let cookie of spotify_login_save.self[ "cookies" ] ) {
// 	// 	await page.setCookie( cookie );
// 	// }
// 	const local_storage_clone = await page.evaluate( () => {
// 		return localStorage;
// 	});
// 	// const cookies_clone = await page.evaluate( () => {
// 	// 	return document.cookie;
// 	// });
// 	const cookies_clone = await page.cookies();
// 	const token_info = await page.evaluate( () => {
// 		const token_script = document.getElementById( "config" );
// 		const token_json = token_script.text.trim();
// 		const token_info = JSON.parse( token_json );
// 		return token_info;
// 	});
// 	await browser.close();
// 	spotify_login_save.self[ "local_storage" ] = local_storage_clone;
// 	spotify_login_save.self[ "cookies" ] = cookies_clone;
// 	spotify_login_save.self[ "token_info" ] = token_info;
// 	spotify_login_save.save();
// 	console.log( spotify_login_save.self );
// })();


// Reuse Login Cookies
( async ()=> {
	const spotify_login_save = new JFODB( "spotify_login_save" );
	const browser = await puppeteer.launch( { headless: true } );
	const page = await browser.newPage();
	await page.setViewport( { width: 1200 , height: 720 } )
	for ( let cookie of spotify_login_save.self[ "cookies" ] ) {
		await page.setCookie( cookie );
	}
	await page.goto( "https://open.spotify.com" , { waitUntil: "networkidle0" } );
	const local_storage_clone = await page.evaluate( () => {
		return localStorage;
	});
	const cookies_clone = await page.cookies();
	const token_info = await page.evaluate( () => {
		const token_script = document.getElementById( "config" );
		const token_json = token_script.text.trim();
		const token_info = JSON.parse( token_json );
		return token_info;
	});
	await browser.close();
	spotify_login_save.self[ "local_storage" ] = local_storage_clone;
	spotify_login_save.self[ "cookies" ] = cookies_clone;
	spotify_login_save.self[ "token_info" ] = token_info;
	spotify_login_save.save();
	console.log( spotify_login_save.self );
})();