# Media Tools

Toolbox for helping creating and managing playlists, and managing the filenames and directory
structure for large numbers of music files. 

This is mostly tailored to my own usage patterns, although it may be useful to others. 

Home page: https://gitlab.com/lilacashes/music-library-tools

PyPI page: https://pypi.org/project/media-tools

## Installation

```bash
$ pip install media-tools
```

## Usage

In general: run a script with the `-v` option first to see what it would change. If 
satisfied, then re-run it with the `-f` option to effect those changes.

### clean_filenames

Removing useless duplicate strings from filenames:
```bash
$ clean_filenames.py -v clean-filenames --recurse .
$ clean_filenames.py -f clean-filenames --recurse .
```
Changing filenames from different numbering schemes to the scheme `01 - filename.ext`:
```bash
$ clean_filenames -v clean-numbering .
$ clean_filenames -f clean-numbering .
``` 
Removing stray junk, such as underscores, stray dashes, and stray `[]` and `()` from
filenames:
```bash
$ clean_filenames -v clean-junk .
$ clean_filenames -f clean-junk .
```
Undoing renamings done with this script, limited to a specified directory and its subfolders,
or a single file name:
```bash
$ clean_filenames -v undo .
$ clean_filenames -f undo .
# OR
$ clean_filenames -f undo ./subdir/file_name.mp3
```
Fixing symlinks to files which have been renamed by any of the previous commands:
```bash
$ clean_filenames -v fix-symlinks .
$ clean_filenames -f fix-symlinks .
```

#### Checking results

Finding mp3 files which do not conform to the numbering scheme in general:
```bash
$ find . -name \*.mp3 | grep -vE '[[:digit:]]+ - .+\.mp3'
```
Finding mp3 files which have a number in their filename but do not conform to the numbering scheme,
excluding some more common use cases:
```bash
$ find . -name \*.mp3 | \
    grep -E '[[:digit:]]+[^/]+\.mp3' | \
    grep -vE '[[:digit:]]+ - .+\.mp3' | \
    grep -vE '[[:digit:]]{2}\.mp3'
```

## Audacious playlist tools

Tools for making and repairing playlists containing physical music files from audacious playlists
and the latest music files. The argument to `--playlist` defaults to the playlist currently playing 
in audacious.

### copy_from_playlist
Copying files from the current or specified playlist (as its name in the `playlists` subdir in the 
audacious configuration folder) to a specified target folder, optionally limiting the number of 
files to copy to the first NUM, and optionally renaming the files to reflect the position of the
song in the playlist:
```bash
$ copy_from_playlist [-v] copy \
    [--playlist PLAYLIST_ID] \
    [--number NUM] \
    [--renumber] \
    TARGET_DIR
```
Try to find files in the current playlist which are unavailable because they have been moved, and
move them back to the place in the filesystem which is noted on the playlist (does not appear to 
work currently):
```bash
$ copy_from_playlist [-v] restore \
    [--playlist PLAYLIST_ID]
```
Copy the newest files to a specified target:
```bash
$ copy_from_playlist [-v] copy-newest \
    --max-age NUM_DAYS \
    --source SOURCE_DIR \
    --target TARGET_DIR
```

### mixcloud_upload

Generate a mix on [mixcloud.com] from the contents of a local directory.

...

### buy_most_played

...

### backup_lastfm_data

...

### print_length

...

# Development

After cloning, it is recommended to set up the git hook that runs the test suite before every 
`git push`:
```bash
$ cd .git/hooks
$ ln -s ../../.git_hooks/pre-push .
```

## Test suite

```bash
$ .git_hooks/pre-push
```

# TO DO

* fix broken symlinks
  * finding broken symlinks: `$ find DIR -type l -follow -exec readlink -f "{}" \;`
* fix audacious playlists which contain moved songs
* fix filenames with common encoder suffixes
* make extensions all lowercase
* migrate undo database to JSON (backup old db first :-/)
