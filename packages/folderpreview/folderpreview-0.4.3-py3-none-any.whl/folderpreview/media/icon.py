
from pathlib import PosixPath

from . import Media

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio , Gtk

class Icon(Media):

	_theme = Gtk.IconTheme.get_default()
	_cache = {}

	@classmethod
	def _get_icon_name(cls, path: PosixPath):
		file = Gio.File.new_for_path(
			path.resolve().as_posix()
		)
		info = file.query_info(
			'standard::icon',
			0,
			Gio.Cancellable()
		)

		return info.get_icon().get_names()[0]

	@property
	def icon_name(self):
		if (not hasattr(self, '_icon_name')):
			self._icon_name = self._get_icon_name(self.target)

		return self._icon_name

	@property
	def _paths(self):
		if (not hasattr(self, '__paths')):
			self.__paths = dict(map(
				self._get_size_path,
				self.get_flavors()
			))

		return self.__paths

	def _get_size_path(self, size):
		return (
			size,
			self._get_path(size)
		)

	def _get_path(self, size):
		file = self._theme.lookup_icon(
			self.icon_name,
			size,
			0
		)

		return file\
			and PosixPath(file.get_filename())\
			or None
