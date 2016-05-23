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
