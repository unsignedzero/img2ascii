## img2ascii

This python script converts a given image into ascii. The intended target
is a shell, as oppose to a browse like other targets for color output.

## Dependencies

* Requires PIL and its dependencies on the local system.
  1. Have libjpeg-dev library installed already.
  2. Install pip
  3. Install Pillow and Pillow-PIL.

## General References

* Color [gist](https://gist.github.com/MicahElliott/719710) to map 24bit RGB to 8bit.
* [Setup](https://stackoverflow.com/questions/10453858/) on Cygwin
  * No compilation was needed on my tests.

## Version/Changelog

* Cleaned up README documentation.
* Added more comments and s/shell/xterm/.
* Tested and working.
* Added main library using PIL.
* Cleaned up colortrans.
* Loaded reference gist before editing.
* README and license created.

