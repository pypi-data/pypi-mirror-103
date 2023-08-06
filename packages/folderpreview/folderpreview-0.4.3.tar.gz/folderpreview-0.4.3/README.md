# FOLDERPREVIEW

Generates folder thumbs using child files thumbs

![demo](https://gitlab.com/hxss-linux/folderpreview/-/raw/master/demo.png)

## Installation

### aur: `folderpreview`

### pip:

systems requirements:

* [dbus thumbnail service](https://wiki.gnome.org/DraftSpecs/ThumbnailerSpec#Request_the_creation_of_thumbnails)
* gtk3 >= 3.24.3
* libvips >= 8.9.2

```
$ pip install folderpreview
$ sudo -E folderpreview --install-thumbnailer
```

## Usage

The thumbnailer will be automatically calling by thumnail service when file manager asks for folder thumbnail. For general usage all you need is installed thumnail service.

`folderpreview --help` for manual usage.

### Tested with:

* `tumbler`
* `thunar`
* `nemo`
* `pcmanfm` (`libfm-directory_thumbnails` required)

### Debugging:

```sh
$ journalctl -f -p debug -t folderpreview
```

## Configuration

`XDG_CONFIG_HOME/folderpreview/config.yaml:`
```yaml
size: 256                  # default thumb size, px
use_hidden: false          # generate thumbs for and use hidden files in preview
request_child_thumbs: true # request thumbs of supported child files
                           # in background scheduler and wait for their readiness
request_timeout: 5         # request timeout, s
priority:                  # priority of child's files for using on preview
- media                    # video/image files with thumbs/thumbnailer
- thumbs                   # other files with thumbs/thumbnailer
- icons                    # files without thumbs/thumbnailer
- subdirs                  # recursion in subdirs with the order
- files                    # all child files
locations:                 # enabled folders locations(including subdirs)
- /
- $HOME/videos
renderer: custom_renderer.CustomRenderer # renderer class name
```

## Customization

For better integration with icon theme renderer can be customized using `config.renderer` option. It should be instance of `folderpreview.renderer.ThumbRenderer` class. Custom renderer can be stored in config folder.

## Links

* [Thumbnail Managing Standard](https://specifications.freedesktop.org/thumbnail-spec/thumbnail-spec-latest.html#CREATION)
* [Thumbnail management DBus specification](https://wiki.gnome.org/DraftSpecs/ThumbnailerSpec#Request_the_creation_of_thumbnails)
