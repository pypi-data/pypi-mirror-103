
import hashlib
from xdg import BaseDirectory
from pathlib import PosixPath

from . import Media

cachePath = BaseDirectory.xdg_cache_home

class Thumb(Media):

	PATH = PosixPath(cachePath) / 'thumbnails'
	EXT = '.png'

	@classmethod
	def get_hash(cls, path: PosixPath):
		return hashlib.md5(
			cls._get_uri(path).encode()
		)\
			.hexdigest()

	@property
	def stem(self):
		if (not hasattr(self, '_stem')):
			self._stem = self.get_hash(self.target) + self.EXT

		return self._stem

	@property
	def paths_potential(self):
		if (not hasattr(self, '_paths_potential')):
			self._paths_potential = {
				size: self.PATH / flavor / self.stem
				for size, flavor in self.get_flavors().items()
			}

		return self._paths_potential

	@property
	def _paths(self):
		return {
			size: path
			for size, path in self.paths_potential.items()
			if path.exists()
		}

