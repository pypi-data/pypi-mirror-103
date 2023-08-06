
import sys
import pkgutil

from pathlib import PosixPath
from argparse import Action

class Installer(Action):

	THUMBNAILER = '/usr/share/thumbnailers/' + __package__ + '.thumbnailer'

	def __call__(self, *args):
		executable = PosixPath(sys.argv[0]).resolve()

		data = pkgutil\
			.get_data(
				__package__,
				'resources/template.thumbnailer'
			)\
			.decode()\
			.replace('folderpreview', executable.as_posix())

		with open(self.THUMBNAILER, 'w') as f:
			f.write(data)

		sys.exit(0)

