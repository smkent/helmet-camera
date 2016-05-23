# Helmet camera video importer

I use this to manage the videos from my bicycle helmet camera.

## import-videos

`import-videos` is meant to run automatically via udev. It mounts the camera
device, copies video files to a directory specified by the user, and unmounts
the camera.

I wrote this script to handle my specific camera (an original ContourROAM), but
it may be useful for video import from any camera that presents videos to the
host via USB mass storage.

### udev rule example

To configure `import-videos` to run automatically, create a udev rule such as
the following (the entire rule must be placed on a single line):

``` KERNEL=="sd?1", ATTRS{idVendor}=="0d64", ATTRS{idProduct}=="5566", ACTION=="add", MODE="664", RUN+="/path/to/helmet-camera/import-videos -e 'email@example.com' -d '/path/to/videos/directory'" ```

Note that the `import-videos` executable name and the target videos directory
argument must be absolute paths.

The email argument is optional, but recommended. If specified, a summary is
emailed from and to the specified address when video import is complete. This
feature requires sendmail.

If you have a camera other than the original ContourROAM, you will likely want
to change the `idVendor` and `idProduct` values in the above example rule. You
can determine the correct values for your hardware by examining the output of
`lsusb`.

Place your udev rule in `/etc/udev/rules.d`, for example in a file named
`/etc/udev/rules.d/81-helmet-camera.rules`.

After creating your udev rule, you may need to reload your udev configuration
by running:

```shell
$ sudo udevadm control --reload
```

Please note this udev rule has been tested on Gentoo Linux. I am not sure if
these instructions are portable to other Linux distributions.

## organize-videos

This is a utility meant to be run manually for organizing already-imported
video files. `import-videos` places all video files directly into the
specified destination directory. `organize-videos` can be used to organize
video files into subdirectories based on the recording count.

`organize-videos` uses a hardcoded organization method based on how the
ContourROAM names its video files. Please see the top of
[video\_utils/\_\_init\_\_.py](/video_utils/__init__.py) for an explanation.

Video file  organization can also happen automatically in `import-videos` with
the `-o`/`--organize` option.

## cleanup-videos

This utility removes video files to free disk space, in order by video number
from lowest to highest. `cleanup-videos` removes videos until the amount of
disk space specified by `-f`/`--free-space` (in GiB) is available.

Video file  organization can also happen automatically in `import-videos` by
specifying the desired amount of free disk space (in GiB) with the
`-c`/`--clean-up-free-space` option.
