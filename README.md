# Metadata_Scrubber
Can scrub Exif metadata from images via URL or by providing a path/upload.

Update: 3/10/2021
The metadascrubber's initial state has been set to run with a default path/url in place, and can also run a batch scrub through the command line.
It primarily functions with analyzing and scrubbing Exif metadata, which means that there are known exceptions when it comes to images with only TIF data:

Traceback (most recent call last):
  File "metadata_scrubber.py", line 117, in <module>
    main()
  File "metadata_scrubber.py", line 103, in main
    scrub(im)
  File "metadata_scrubber.py", line 8, in scrub
    exif_dict = piexif.load(im.info['exif'])
KeyError: 'exif'


Otherwise, it currently clears the "Recommended"-identified tags, since we have not implemented it with the web-app to allow for users to choose which tags for themselves.
Users should understand that not all URL's carry raw image data, or might be scrubbed by default according to the protocol of the source image. For example, I believe Reddit and Twitter both automatically scrub this data (potentially making the URL functionality useless).
There are some images provided in the directory data_images, which carry images with raw data to work with. There are also some sample URL's in the script main().
 

