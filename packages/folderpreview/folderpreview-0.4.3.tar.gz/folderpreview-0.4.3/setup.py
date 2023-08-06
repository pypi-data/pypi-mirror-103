
import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "folderpreview",
	version = "0.4.3",
	python_requires = '>=3.6.12',
	install_requires = [
		'dbus-next>=0.1.1',
		'pyxdg>=0.26',
		'pyyaml>=5.1',
		'parse>=1.9.0',
		'pygobject>=3.30.4', # gtk3-3.24.3
		'pyvips>=2.1.5',     # libvips-8.9.2
	],
	extra_require = [
		'cysystemd>=0.16.2', # systemd
		'colorlog>=3.1.1',
	],
	entry_points = {
		'console_scripts': [
			'folderpreview = folderpreview:main',
		],
	},
	package_data={
		'': ['resources/template.thumbnailer'],
	},
	author = "hxss",
	author_email = "hxss@ya.ru",
	description = "Generates folder preview thumb",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	license = 'MIT',
	url = "https://gitlab.com/hxss-linux/folderpreview",
	packages = setuptools.find_packages(),
	keywords = ['folder', 'thumb'],
	classifiers = [
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
		"Topic :: Desktop Environment :: File Managers",
	],
)
