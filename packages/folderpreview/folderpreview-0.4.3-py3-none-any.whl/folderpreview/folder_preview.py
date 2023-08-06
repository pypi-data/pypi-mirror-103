
import os
import mimetypes
from pathlib import PosixPath

from . import LogicException
from . import logger
from . import thumbnailer

from .config import Config

from .media import (
	MediaDecorator,
	Thumb
)

from .renderer import ThumbRenderer

class FolderPreview():

	META_URI = 'Thumb::URI'
	META_MTIME = 'Thumb::MTime'

	def __init__(self, folder_path, config_path = None):
		self.config = Config(config_path)

		self.folder = PosixPath(folder_path).resolve()
		self.log()

		if (
			not self.folder.is_dir()
			or not self._validate_hidden(self.folder)
			or not self._is_valid_folder(self.folder)
		):
			raise LogicException('Invalid folder path')

		self.size = self.config.size

		self.files = {}
		self.dirs = {}

	@property
	def config(self):
		if (not hasattr(self, '_config')):
			self.config = Config()

		return self._config

	@config.setter
	def config(self, config: Config):
		self._config = config

		confgi_dir = self\
			.config\
			.path\
			.resolve()\
			.parent\
			.as_posix()

		import sys
		sys.path.append(confgi_dir)

	@property
	def locations(self):
		if (not hasattr(self, '_locations')):
			def is_dir(path: PosixPath):
				if (not path.is_dir()):
					logger.warning(
						'Invalid location: '
						+ path.resolve().as_posix()
					)

				return path.is_dir()

			expanded = map(
				os.path.expandvars,
				self.config.locations
			)
			posix = map(PosixPath, expanded)
			filtered = filter(is_dir, posix)

			self._locations = set(filtered)

		return self._locations

	@property
	def use_hidden(self):
		return self.config.use_hidden

	@property
	def flavor(self):
		return MediaDecorator.get_flavors()\
			.get(
				self.size,
				MediaDecorator.FLAVOR_LARGE
			)

	@property
	def size(self):
		return self.__size

	@size.setter
	def size(self, size: int):
		self.__size = int(size)

	def set_size(self, size: int):
		self.size = size

		return self

	@property
	def thumb_path(self):
		if (not hasattr(self, '_thumb_path')):
			thumb = self._get_thumb(self.folder)
			self._thumb_path = thumb.paths_potential.get(self.size)

		return self._thumb_path

	@property
	def renderer(self) -> ThumbRenderer:
		return _import(
			self.config.renderer
		)

	def set_thumb_path(self, thumb_path):
		self._thumb_path = PosixPath(thumb_path)

	def generate(self):
		renderer = self.init_renderer()
		renderer.render()
		self.set_meta(renderer)
		renderer.save()

	def set_meta(self, renderer: ThumbRenderer):
		renderer.meta[self.META_URI] = self.folder.as_uri()
		renderer.meta[self.META_MTIME] = int(
			self.folder.stat().st_mtime
		)

	def init_renderer(self):
		renderer = self.renderer(
			self.config,
			self._get_icon(self.folder),
			map(
				self._get_media,
				self._iter_folder_album(self.folder)
			),
			self.thumb_path,
			self.size
		)
		self.require_thumbs(renderer)

		return renderer

	def require_thumbs(self, renderer: ThumbRenderer):
		if (self.config.request_child_thumbs):
			to_thumb = set(filter(
				lambda path: (
					not self._has_thumb(path)
					and self._has_thumbler(path)
				),
				map(
					lambda media: media.target,
					renderer.content
				)
			))

			if (to_thumb):
				thumbnailer.sync_queue_wait(
					map(
						lambda path: path.resolve().as_uri(),
						to_thumb
					),
					map(self._get_mime, to_thumb),
					self.flavor,
					self.config.request_timeout
				)

	def log(self):
		logger.debug(
			'folder: '
			+ self.folder.as_posix()
			+ '\n[' + Thumb.get_hash(self.folder) + ']'
		)

	def _iter_folder_album(self, path: PosixPath = None):
		for iterator in self.queue:
			for file in getattr(self, iterator)(path):
				yield file

	@property
	def queue(self, path: PosixPath = None):
		queue_map = {
			'media': '_iter_files_media',
			'thumbs': '_iter_files_has_thumb',
			'icons': '_iter_files_other',
			'subdirs': '_iter_childs_album',
			'files': '_get_files',
		}

		for iter_name in self.config.priority:
			yield queue_map[iter_name]

	def _iter_childs_album(self, path: PosixPath):
		childs = self._get_dirs(path)
		child_albums = {}

		while len(childs):
			for child in list(childs):
				album = child_albums.setdefault(
					child.resolve().as_posix(),
					self._iter_folder_album(child)
				)

				new = next(album, None)
				if (new):
					yield new
				else:
					childs.remove(child)

	def _iter_files_media(self, path: PosixPath = None):
		return filter(
			lambda file: (
				self._is_visual(file)
				and self._can_thumb(file)
			),
			self._get_files(path)
		)

	def _iter_files_has_thumb(self, path: PosixPath = None):
		return filter(
			lambda file: (
				not self._is_visual(file)
				and self._can_thumb(file)
			),
			self._get_files(path)
		)

	def _iter_files_other(self, path: PosixPath = None):
		return filter(
			lambda file: not self._can_thumb(file),
			self._get_files(path)
		)

	def _get_files(self, path: PosixPath = None):
		path_str = path.resolve().as_posix()

		if (not path_str in self.files):
			self.files[path_str] = sorted(
				filter(
					lambda child: (
						child.is_file()
						and self._validate_hidden(child)
					),
					path.iterdir()
				)
			)

		return self.files[path_str]

	def _get_dirs(self, path: PosixPath = None):
		path = path or self.folder
		path_str = path.resolve().as_posix()

		if (not path_str in self.dirs):
			self.dirs[path_str] = sorted(
				filter(
					lambda child: (
						child.is_dir()
						and self._validate_hidden(child)
					),
					path.iterdir()
				)
			)

		return self.dirs[path_str]

	def _get_icon(self, path: PosixPath):
		return self._get_media(path).icon

	def _get_thumb(self, path: PosixPath):
		return self._get_media(path).thumb

	def _get_media(self, path: PosixPath):
		return MediaDecorator.get(path)

	def _get_mime(self, path: PosixPath):
		return mimetypes.guess_type(
			path.resolve().as_posix()
		)[0]

	def _validate_hidden(self, path: PosixPath):
		return self.use_hidden\
			or not self._is_hidden(path)

	def _is_valid_folder(self, folder: PosixPath):
		parents = set([folder] + list(folder.parents))

		return bool(parents & self.locations)\
			and Thumb.PATH not in parents

	def _is_hidden(self, path: PosixPath):
		return path.stem.startswith('.')

	def _can_thumb(self, path: PosixPath):
		return (
			self._has_thumb(path)
			or self._has_thumbler(path)
		)

	def _is_visual(self, path: PosixPath):
		mime = self._get_mime(path)

		return mime and mime\
			.startswith(('video/', 'image/'))

	def _has_thumb(self, path: PosixPath):
		return bool(self._get_thumb(path).get_path(self.size))

	def _has_thumbler(self, path: PosixPath):
		mime = self._get_mime(path)

		return mime in thumbnailer.sync_get_supported()

def _import(name):
	components = name.split('.')
	mod = __import__(components[0])
	for comp in components[1:]:
		mod = getattr(mod, comp)

	return mod
