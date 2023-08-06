
from pathlib import PosixPath

from folderpreview.config import Config
from folderpreview.media import *

class ThumbRenderer():

	'''
	Abstract renderer class

	Args:
		config (Config): loaded configuration
		folder (Icon): the folder Icon object
		content ([MediaDecorator]): generator of the folder child files Media
		path (PosixPath): path of the resulting thumbnail
		size (int): size of thumbnail, px

	Attributes:
		see args
	'''

	def __init__(
		self,
		config: Config,
		folder: Icon,
		content: [MediaDecorator],
		path: PosixPath,
		size
	):
		self.config = config
		self.folder = folder
		self.content = content
		self.path = path
		self.size = size

	'''
	Content list
	'''
	@property
	def content(self):
		if (not hasattr(self, '_content')):
			self._content = []

		return self._content

	@content.setter
	def content(self, content: [MediaDecorator]):
		self.set_content(content)

	'''
	Loads the content list
	This list will be used to require missing thumbs
	'''
	def set_content(self, content: [MediaDecorator]):
		self._content = list(content)

	'''
	Renders thumbs
	'''
	def render(self):
		raise NotImplementedError

	'''
	Thumb metadata dictionary
	Required for rendering directly into thumbnails dirs
	'''
	@property
	def meta(self) -> dict:
		raise NotImplementedError

	'''
	Save rendered thumb and filled metadata into `self.path`
	'''
	def save(self):
		raise NotImplementedError
