import os,sys
from setuptools import setup,find_packages
sys.path.insert(0, os.path.abspath('lib'))
#from library import __version__, __author__
#print (__version__)
with open("README.md", "r") as file:
  long_description = file.read()

# with open("CHANGES.md", "r") as file:
#   changes = file.read()

setup(
	name='netkiller-kindle',
	version='0.0.3',
	author='Neo Chen',
	author_email='netkiller@msn.com',
	description="Send ebook to kindle device",
	long_description=long_description,
	long_description_content_type="text/markdown",
	keywords='kindle',
	url='http://netkiller.github.io',
	download_url='https://github.com/netkiller/kindle',
	license='MIT',
	classifiers=[
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
	],

	packages=find_packages(),
	scripts=[
		'bin/kindle'
	],

	data_files = [
		('etc', ['etc/kindle.ini'])
		# ('~/.kindle', ['db/kindle/netkiller@kindle.cn.db'])
		#('log', ['log/kindle.log']),
		# ('share', ['share/kindle.md']),
	]
)
