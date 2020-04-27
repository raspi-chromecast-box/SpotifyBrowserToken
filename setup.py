import setuptools

setuptools.setup(
	name="SpotifyBrowserToken",
	version="0.0.1",
	author="raspichromecastbox",
	author_email="raspiccbox03@gmail.com",
	description="Spotify Browser Token Generator",
	url="https://github.com/raspi-chromecast-box/SpotifyBrowserToken",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)

install_requires = [
	'json',
	'pathlib',
	'time',
	'asyncio',
	'pyppeteer'
]