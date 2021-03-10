from PIL import Image, ExifTags #using pillow to open in image using its url
import requests
import piexif
import os
import sys

def scrub(im):
    exif_dict = piexif.load(im.info['exif'])
    all_tags, recommended_tags = get_tags(im,exif_dict)
    clear_chosen(im,recommended_tags.keys(),exif_dict)

def get_tags(im,exif_dict):

    rec_list = ["make", "model", "gps", "maker", "note", "location", "name",
                "date", "datetime", "description", "software", "device",
                "longitude", "latitude", "altitude"]
    tags_found = {}  # dictionary of all tags found mapped to their metadata values
    recommended_found = {}  # dictionary of all tags found using the recommended keys in the list above, mapped to values
    for tag_space in ("0th", "Exif", "GPS", "1st"):
        for tag in exif_dict[tag_space]:
            name = piexif.TAGS[tag_space][tag]["name"]
            desc = exif_dict[tag_space][tag]
            tags_found[name] = desc
            if any(rec in name.lower() for rec in rec_list):
                recommended_found[name] = desc

    print("==Found recommended==", recommended_found.keys())
    return tags_found, recommended_found

def clear_chosen(im,tags_chosen,exif):
    print("===clear_chosen===")
    new_exif = adjust_exif(tags_chosen,exif)
    new_bytes = piexif.dump(new_exif) #dumps the new dictionary into bytes for inserting into an image's exif metadata

    #saves an image and gives it a unique name if it is already found in the directory/system
    suffix = 0
    while (os.path.isfile("photosensed"+str(suffix)+".jpg")):
        suffix +=1
    im.save("photosensed"+str(suffix)+".jpg", exif = new_bytes)

    print("===finish clearing chosen tags===")

def full_scrub(im):
    suffix = 0
    while (os.path.isfile("photosensed"+str(suffix)+".jpg")):
        suffix +=1
    #simply saving using the Pillow library automatically scrubs all metadata
    im.save("photosensed"+str(suffix)+".jpg")


def adjust_exif(tags_chosen,exif):
    new_exif = dict(exif)
    tag_space_list = ["0th", "Exif", "GPS", "1st"]
    i =0
    for index,tag_space in enumerate(tag_space_list):
        print("Tag Space: ",tag_space)

        for chosen in tags_chosen:
            try:
                # have to check each case because of the piexif does not have __getattribute__ for ImageIFD, ExifIFD,etc..
                if index == 0:
                    new_exif[tag_space][piexif.ImageIFD.__getattribute__(piexif.ImageIFD,chosen)] = ""
                elif index == 1:
                    new_exif[tag_space][piexif.ExifIFD.__getattribute__(piexif.ExifIFD,chosen)] = b''
                elif index == 2:
                    #have to assign the right None types for bytes, ints, and tuples
                    if type(new_exif[tag_space][piexif.GPSIFD.__getattribute__(piexif.GPSIFD,chosen)]) is bytes:
                        new_exif[tag_space][piexif.GPSIFD.__getattribute__(piexif.GPSIFD,chosen)] = b''
                    if type(new_exif[tag_space][piexif.GPSIFD.__getattribute__(piexif.GPSIFD, chosen)]) is int:
                        new_exif[tag_space][piexif.GPSIFD.__getattribute__(piexif.GPSIFD,chosen)] = 0
                    if type(new_exif[tag_space][piexif.GPSIFD.__getattribute__(piexif.GPSIFD, chosen)]) is tuple:
                        new_exif[tag_space][piexif.GPSIFD.__getattribute__(piexif.GPSIFD,chosen)] = (0,0)
                else:
                   new_exif[tag_space][piexif.InteropIFD.__getattribute__(piexif.InteropIFD, chosen)] = ""
                #count progress of tags cleared/found
                i+=1
                print("removed: ",chosen, i,"/",len(tags_chosen))

            except: continue #this accounts for the fact that each tag doesnt exist in every tag_space (would throw an exception)

    return new_exif

#for now, tries to automatically detect if it is a path or url
def get_image(path_or_url):
    try:
        im = Image.open(path_or_url)

    except:
        im = Image.open(requests.get(path_or_url, stream=True).raw)
    return im

'''
If no arguments are used when running the script, then a default image URL will be used for demonstration.
If any number of valid arguments are used, then those images will be processed.
'''
def main():
    #use a default path if none specified
    if len(sys.argv) == 1:
        # path_or_url = "./data_images/gps3.jpg" #paths work
        path_or_url = "https://github.com/ianare/exif-samples/blob/master/jpg/gps/DSCN0025.jpg?raw=true" #all urls besides those to TIFF
        im = get_image(path_or_url)
        scrub(im)
        #full_scrub(im)
        # path_or_url = "https://github.com/ianare/exif-samples/blob/master/jpg/invalid/image00971.jpg?raw=true" #TIFF formats do not work

    else: #process any working URL's and paths
        for i,arg in enumerate(sys.argv):
            print("arg:", arg)
            if i > 0:
                path_or_url = arg
                im = get_image(path_or_url)
                scrub(im)
                #full_scrub(im)


if __name__ == "__main__":
    main()