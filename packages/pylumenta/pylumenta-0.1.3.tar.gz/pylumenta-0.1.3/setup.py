from setuptools import setup, find_packages

setup(
	name='pylumenta',
	version='0.1.2',
	description='Polumenta generator',
	author='Vladimir Lojanica',
	author_email='vladimirlojanica@gmail.com',
	url='https://github.com/vladimirlojanica/pylumenta',
	packages=find_packages(),
	tests_require=['pytest'],
	license_files=('LICENSE',)
)