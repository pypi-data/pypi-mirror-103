from setuptools import setup

setup(
	name='term-forecast',
	version='0.1.dev2',
	author='Kevin Midboe',
	author_email='support@kevinmidboe.com',
	
	description='Terminal Forcast is a easily accessible terminal based weather forecaster',
	url='https://github.com/KevinMidboe/termWeather/',
	license='MIT',
	
	packages=['term_forecast'],
  pacakge_data={
    "": ["*.txt"]
  },

	classifiers = [
		"Environment :: Console",
        "Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",

        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],

    install_requires=[
        'fire==0.1.1',
'geoip2==2.5.0',
'fuzzywuzzy==0.15.1',
'python-Levenshtein==0.12.0'
    ],

    entry_points={
       'console_scripts': [
           'forecast = term_forecast.term_weather:main',
       ],
    }
)
