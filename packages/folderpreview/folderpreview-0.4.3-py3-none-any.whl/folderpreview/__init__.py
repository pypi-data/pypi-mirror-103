
class LogicException(Exception):
	pass

from .logger import logger
from .installer import Installer

from .dbus import Thumbnailer
thumbnailer = Thumbnailer()

from .folder_preview import FolderPreview

def main():
	import argparse

	class HelpFormatter(argparse.HelpFormatter):
		def __init__(self, prog, **kwargs):
			super().__init__(prog, **kwargs, max_help_position = 26)

	parser = argparse.ArgumentParser(
		prog = 'folderpreview',
		formatter_class = HelpFormatter,
		description = 'Generate folder preview thumb '
			+ 'and save into '
			+ 'thumbnails directory or OUTPUT',
	)
	parser.add_argument(
		'folder',
		type = str,
		help = 'the target folder path',
	)
	parser.add_argument(
		'-o',
		type = str,
		dest = 'output',
		help = 'result thumbnail path',
	)
	parser.add_argument(
		'-s',
		type = str,
		dest = 'size',
		default = None,
		required = False,
		help = 'size of thumbnail, px',
	)
	parser.add_argument(
		'-c',
		type = str,
		dest = 'config',
		default = None,
		required = False,
		help = 'config path',
	)
	parser.add_argument(
		'-t', '--test',
		dest = 'test',
		action = 'store_true',
		default = False,
		required = False,
		help = 'check if folder supported and request child thumbs',
	)
	parser.add_argument(
		'--install-thumbnailer',
		dest = 'install',
		action = Installer,
		nargs = 0,
		default = False,
		required = False,
		help = 'install .thumbnailer and exit',
	)

	args = parser.parse_args()

	preview = FolderPreview(args.folder, args.config)
	args.size and preview.set_size(args.size)
	args.output and preview.set_thumb_path(args.output)

	args.test and logger.debug('test')

	args.test\
		and preview.init_renderer()\
		or preview.generate()

	return 0
