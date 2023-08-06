
import os
from xdg import BaseDirectory
from pathlib import PosixPath

from .resource import Resource

class Config(Resource):

	def __init__(self, path = None):
		if (path):
			self._set_path(path)

		super().__init__()

	@property
	def defaults(self):
		return {
			'size': 256,
			'use_hidden': False,
			'request_child_thumbs': True,
			'request_timeout': 30,
			'priority': [
				'media',
				'thumbs',
				'icons',
				'subdirs',
			],
			'locations': [
				'/',
			],
			'renderer': 'folderpreview.renderer.TileThumbRenderer',
		}

	@property
	def path(self):
		if (not hasattr(self, '_path')):
			config_home = BaseDirectory.xdg_config_home
			dir_name = 'folderpreview'

			if (os.environ['HOME'] == config_home):
				dir_name = '.' + dir_name

			self._path = PosixPath(
				config_home + '/' + dir_name + '/config.yaml'
			)

		return self._path

	def _set_path(self, path):
		self._path = PosixPath(path).resolve()
