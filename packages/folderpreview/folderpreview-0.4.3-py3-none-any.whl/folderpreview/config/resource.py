
import yaml
from yaml import Loader

from pathlib import PosixPath

from folderpreview import logger

class Resource():

	def __init__(self):
		self.path.parent.mkdir(
			parents = True,
			exist_ok = True
		)
		self.save()
		self._load()
		self._switch_dict()

	def save(self):
		if (
			not self.path.is_file()
			or not self.path.stat().st_size
		):
			with self.path.open('w') as file:
				yaml.dump(
					self.defaults,
					file,
					indent = 4,
					sort_keys = False,
				)

	def _load(self):
		self._dict = self.defaults
		if (self.path.is_file()):
			with self.path.open('r') as file:
				try:
					self._dict = yaml.load(file, Loader = Loader)\
						or self._dict
				except Exception as e:
					logger.warning(
						'Error loading: '
						+ self.path.resolve().as_posix()
					)

	def _switch_dict(self):
		def getattr(name):
			if (name in self._dict):
				return self._dict[name]
			elif (name in self.defaults):
				return self.defaults[name]

			raise AttributeError(name)

		def setattr(name, value):
			self._dict[name] = value

		self.__getattr = getattr
		self.__setattr = setattr

	@property
	def defaults(self):
		return {}

	@property
	def path(self) -> PosixPath:
		pass

	def __getattr__(self, name):
		return self.__getattr(name)

	def __getattr(self, name):
		if (name in self.__dict__):
			return self.__dict__[name]

		raise AttributeError(name)

	def __setattr__(self, name, value):
		self.__setattr(name, value)

	def __setattr(self, name, value):
		self.__dict__[name] = value

	def __delattr__(self, name):
		if (name in self._dict):
			del self._dict[name]
		else:
			raise AttributeError(name)
