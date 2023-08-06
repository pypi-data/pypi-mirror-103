
from . import *

class MediaDecorator(Media):

	@property
	def thumb(self):
		return Thumb.get(self.target)

	@property
	def icon(self):
		return Icon.get(self.target)

	def get_path(self, size = None):
		path = filter(
			bool,
			map(
				lambda media: media.get_path(size),
				[self.thumb, self.icon]
			)
		)

		return next(path, None)
