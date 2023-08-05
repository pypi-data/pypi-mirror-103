Toilmore Python SDK release notes
============================


v0.0.1
-----
* First version to optimize and process images.

v0.0.2
-----
* Improvements to the README, and setup.py.

v0.0.3
-----
* The version of the SDK is printed on command call.
* The optimized image size is returned when it is stored on disk.

v0.0.4
-----
* Improvements to the entry point, and example scripts.

v0.0.5
-----
* Added the validation for the input image.
* Improvements to the doc.

v0.0.6
-----
* Fixed an ssl issue on MacOS.

v0.0.7
-----
* Re-uploading the file in any case we get the "expecting-file" response.
* Retrying when downloading the optimized image from the bucket.

v0.0.8
-----
* Human readable rejection notices.
* Validation of the precursor name input.

v0.0.9
-----
* Fixed an issue when the force_reprocessing parameter is True, in which case an expecting-file status was always returned.

v0.1.0
-----
* Accepting JPEG-XL as precursor name.
* Added more quality metrics to the encoder.

v0.1.1
-----
* Added edsr-x4 as super-resolution algorithm for master.