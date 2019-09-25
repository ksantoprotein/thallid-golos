# -*- coding: utf-8 -*-

import codecs
import setuptools

try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == 'mbcs'))

with open('README.md', 'r', encoding = 'utf8') as fh:
	long_description = fh.read()
VERSION = '0.0.1'

setuptools.setup(
	name = 'tgolosbase',
	version = VERSION,
	author = 'ksantoprotein',
	author_email = 'ksantoprotein@rambler.ru',
	description = 'Python library for GOLOS',
#	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/ksantoprotein/thallid-golos',
	#packages = setuptools.find_packages()
	packages = ['tgolosbase'],
	
	#download_url='https://github.com/bitfag/golos-piston/tarball/' + VERSION,
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
	],
	install_requires=[
		"websocket-client",
		"urllib3",
		"ecdsa>=0.13",
		"graphenelib>=0.5.3",
	],
	#setup_requires=['pytest-runner'],
	#tests_require=['pytest'],
	#include_package_data=True,
)
