
from pathlib import PosixPath

from folderpreview import thumbnailer

class Media():

	FLAVOR_LARGE = 'large'
	FLAVOR_NORMAL = 'normal'

	SIZES = {
		FLAVOR_LARGE: 256,
		FLAVOR_NORMAL: 128,
	}

	_cache = {}

	@classmethod
	def get(cls, path: PosixPath):
		return cls._cache\
			.setdefault(
				cls.__name__,
				{}
			)\
			.setdefault(
				cls._get_uri(path),
				cls(path)
			)

	@classmethod
	def get_flavors(cls):
		if (not hasattr(cls, '_flavors')):
			cls._flavors = dict(map(
				lambda flavor: (cls.SIZES[flavor], flavor),
				thumbnailer.sync_get_flavors()
			))

		return cls._flavors

	@classmethod
	def _get_uri(cls, path: PosixPath):
		return path.resolve().as_uri()

	def __init__(self, target: PosixPath):
		self.target = target

	def get_path(self, size = None):
		return size\
			and self._paths.get(size, None)\
			or next(iter(self._paths.values()), None)

	@property
	def _paths(self):
		raise NotImplementedError

	def __repr__(self):
		return '<' + self.__class__.__name__ + '>'\
			+ ': ' + self.target.resolve().as_posix()
