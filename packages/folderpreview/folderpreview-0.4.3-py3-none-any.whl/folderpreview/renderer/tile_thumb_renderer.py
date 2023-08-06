
import pyvips
import itertools

from pathlib import PosixPath
from parse import parse

from folderpreview import LogicException
from folderpreview.media import MediaDecorator

from .thumb_renderer import ThumbRenderer

class TileThumbRenderer(ThumbRenderer):

	TILE_SIZE = 4
	META_PATTERN = 'png-comment-{id}-{name}'
	PYVIPS_ENUMS_BLEND_MODE_OVER = 'over'     # pyvips>=2.1.12

	def __init__(self, *args):
		super().__init__(*args)

		self.image = None

	def set_content(self, content: [MediaDecorator]):
		self._content = sorted(
			itertools.islice(content, self.TILE_SIZE),
			key = lambda media: media.target
		)

		if (not self._content):
			raise LogicException('Not enough files in folder')

	def render(self):
		image = self._extend(
			self._load(self.folder.get_path(self.size)),
			self.size
		)

		content_size = int(self.size / 2)

		content, mode, x, y = list(map(list, zip(*[
			(
				self._resize(
					self._load(
						media.get_path(content_size),
						content_size
					),
					content_size
				),
				self.PYVIPS_ENUMS_BLEND_MODE_OVER,
				int(content_size * (k & 1) / 2 ** 0),
				int(content_size * (k & 2) / 2 ** 1),
			) for k, media in enumerate(self.content)
		])))

		self.image = image.composite(content, mode, x = x, y = y)

	@property
	def meta(self):
		if (not hasattr(self, '_meta')):
			self._meta = {}

		if (not self._meta and self.image):
			for field in self.image.get_fields():
				matches = parse(self.META_PATTERN, field)
				if (matches):
					name = matches['name']
					self._meta[name] = self.image.get(field)
					self.image.remove(field)

		return self._meta

	def save(self):
		self._pack_meta()
		self.image.pngsave(self.path.resolve().as_posix())

	def _pack_meta(self):
		gtype = pyvips.base.type_from_name('gchararray')
		for i, (name, value) in enumerate(self.meta.items()):
			field = self.META_PATTERN.format(id = i, name = name)
			self.image.set_type(gtype, field, str(value))

	def _resize(self, image: pyvips.Image, size):
		image = self._extend(image, size)

		mask = image.extract_band(3)
		l, t, w, h = mask.find_trim(background = 0)

		if (0 in (l, t) or size in (w, h)):
			image = self._extend(image.resize(0.9), size)

		return image

	def _extend(self, image: pyvips.Image, size):
		return image.embed(
			int((size - image.width) / 2),
			int((size - image.height) / 2),
			size,
			size,
			extend = 'background',
			background = [0, 0, 0, 0]
		)

	def _load(self, path: PosixPath, base_size = None):
		base_size = base_size or self.size

		image = pyvips.Image.new_from_file(
			path.resolve().as_posix()
		)

		size = image.width > image.height\
			and image.width\
			or image.height

		scale = base_size / size

		return ('svg' in path.suffix)\
			and pyvips.Image.svgload(
				path.resolve().as_posix(),
				scale = scale
			)\
			or image.resize(scale)
