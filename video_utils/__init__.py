import os
import re
import sys

# Videos are organized into directories named based on the range of video file
# name numbers they contain. For example, "FILE1250.MOV" would be placed in a
# subdirectory named "1200-1299".
dirname_regex = '^[0-9]{4}-[0-9]{4}$'

# The ContourROAM splits videos at about the 44-minute mark. This is indicated
# in how the ContourROAM names its video files. The first video in any set is
# called FILEXXXX.MOV, where "XXXX" is the recording count. If the first video
# is longer than 44 minutes, second and further videos are named FIYYXXXX.MOV,
# where YY starts at "01" with the first continuation file, "02" for the second,
# and so on. The organization below renames these continuation files from
# FIYYXXXX.MOV to FILEXXXX-Y.MOV. For example, "FI011250.MOV" would be renamed
# to "FILE1250-1.MOV".
video_fn_regex = r'^FI(LE|[0-9]{2})([0-9]{4})(-[0-9]{1})?.(THM|MOV|MOV\.times)$'

videos_each_dir = 100

def list_videos(path):
    for dirpath, dirnames, filenames in sorted(os.walk(path)):
        if dirpath.startswith(path):
            dirpath = dirpath.replace(path, '', 1)
        if dirpath.startswith(os.sep):
            dirpath = dirpath[1:]
        if dirpath and not re.match(dirname_regex, dirpath):
            continue
        for fn in sorted(filenames):
            m = re.match(video_fn_regex, fn)
            if not m:
                continue
            yield os.path.join(dirpath, fn)

def organized_path(fn):
    """Calculate organized destination filename for input filename"""
    m = re.match(video_fn_regex, fn)
    if not m:
        return None
    fn_num = int(m.group(2))
    range_start = fn_num - fn_num % videos_each_dir
    range_end = range_start + videos_each_dir - 1
    new_fn_dir = '{:04d}-{:04d}'.format(range_start, range_end)
    if m.group(1).isdigit():
        prefix, suffix = fn.split('.', 1)
        new_fn = '{}-{:d}.{}'.format(prefix, int(m.group(1)), suffix)
        new_fn = re.sub('^FI[0-9]{2}', 'FILE', new_fn)
    else:
        new_fn = fn
    new_fn = os.path.join(new_fn_dir, new_fn)
    return new_fn
