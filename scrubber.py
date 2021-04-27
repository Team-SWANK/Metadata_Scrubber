from PIL import Image, ExifTags #using pillow to open in image using its url
import requests
import piexif
import io
import matplotlib.pyplot as plt

def url():
    #using a url
    #url = "https://preview.redd.it/tpou7vmb6wh61.jpg?width=840&format=pjpg&auto=webp&s=fce8dbfeac72e9731cdefa5eaa53d858e8dd9ff3"
    url = "https://www.gooverseas.com/sites/default/files/styles/1014x/public/images/2018-03-11/Volunteer%20with%20Sea%20Turtles%20Hero.jpg?itok=6i_geFUq"
    im = Image.open(requests.get(url, stream=True).raw)

    metadata = im._getexif()
    print("printing metadata from image link... \n")
    print("metadata: \n", metadata)
    #im.show()
    im.save("test.jpg")
    print("finished\n")

def piexample():
    im = Image.open("gps.jpg")

    exif_dict = piexif.load(im.info['exif'])

    # rec_list = ["make", "model", "gps", "maker", "note", "location", "name",
    #             "date", "datetime", "description", "software", "device",
    #             "longitude", "latitude", "altitude"]
    rec_list = ["make"]
    found_tags = []
    found_descriptions = []
    found_recommended = []
    for tag_space in ("0th", "Exif", "GPS", "1st"):
        for tag in exif_dict[tag_space]:
            name = piexif.TAGS[tag_space][tag]["name"]
            desc = exif_dict[tag_space][tag]
            found_tags.append(name)
            found_descriptions.append(desc)

            if any(rec in name.lower() for rec in rec_list):
                found_recommended.append(name)
            #print(name, desc)
    print("==Found recommended==",found_recommended)
    clear_chosen2(im,found_recommended,exif_dict)

def adjust_exif3(tags_chosen, exif):
    new_exif = dict(exif)
    #print(new_exif)
    #key = new_exif["0th"][piexif.ImageIFD.GPSTag]
    #key = new_exif["0th"][piexif.ImageIFD.DateTime]
    #new_exif[key] = ""
    #new_exif["0th"][piexif.ImageIFD.Model] = ""
    #new_exif["0th"][piexif.ImageIFD.GPSTag] = ""

    #print([a for a in dir(new_exif["0th"]) if not a.startswith('__')])
    #print(dir(new_exif["0th"].keys()))
    #keys =
    #print(dir(new_exif["0th"]))
    #print(new_exif["0th"]))
    #print(new_exif["0th"].items())


    #print(dir(piexif))
    #print(dir(piexif.ImageIFD))
    #print(dir(piexif.ExifIFD))
    #if 0th, then ImageIFD, if GPS the GPSIFD, if Exif, then ExifIFD, if 1st then InteropIFD
    ######print(piexif.ImageIFD.__getattribute__(piexif.ImageIFD,"Make"))
    ####new_exif["0th"][piexif.ImageIFD.__getattribute__("Make")] = ""

    #print( "\nDat: ",new_exif["0th"][piexif.ImageIFD.GPSTag])
    #print(new_exif["Exif"])
    return new_exif
def adjust_exif2(tags_chosen,exif):
    new_exif = dict(exif)
    tag_space_list = ["0th", "Exif", "GPS", "1st"]
    IFD_list = ["ImageIFD", "ExifIFD", "GPSIFD", "InteropIFD"]
    i =0
    for index,tag_space in enumerate(tag_space_list):
        print("Tag Space: ",tag_space)
        #ifd = IFD_list[index]

        for chosen in tags_chosen:
            try:
                if index == 0:
                    #tag_num = piexif.ImageIFD.__getattribute__(piexif.ImageIFD,chosen)
                    new_exif[tag_space][piexif.ImageIFD.__getattribute__(piexif.ImageIFD,chosen)] = ""
                elif index == 1:
                    #print(type(new_exif[tag_space][piexif.ExifIFD.__getattribute__(piexif.ExifIFD,chosen)]))
                    new_exif[tag_space][piexif.ExifIFD.__getattribute__(piexif.ExifIFD,chosen)] = b''
                elif index == 2:
                    tagType = type(new_exif[tag_space][piexif.GPSIFD.__getattribute__(piexif.GPSIFD,chosen)])
                    if tagType is bytes:
                        new_exif[tag_space][piexif.GPSIFD.__getattribute__(piexif.GPSIFD,chosen)] = b''
                    if tagType is int:
                        new_exif[tag_space][piexif.GPSIFD.__getattribute__(piexif.GPSIFD,chosen)] = 0
                    if tagType is tuple:
                        new_exif[tag_space][piexif.GPSIFD.__getattribute__(piexif.GPSIFD,chosen)] = (0,0)
                else:
                   new_exif[tag_space][piexif.InteropIFD.__getattribute__(piexif.InteropIFD, chosen)] = ""
                i+=1
                print("removed: ",chosen, i,"/",len(tags_chosen))

            except: continue #this accounts for the fact that each tag doesnt exist in every tag_space

    return new_exif

def clear_chosen2(im, tags_chosen,exif):
    print("===clear_chosen===")
    new_exif = adjust_exif2(tags_chosen,exif)
    new_bytes = piexif.dump(new_exif)

    # used to test writing to an output buffer without writing to file
    imgByteArr = io.BytesIO()
    im.save(imgByteArr, format=im.format)
    imgByteArr = imgByteArr.getvalue()
    output_image = io.BytesIO()
    piexif.insert(new_bytes, imgByteArr, output_image)
    with open("gps-exif.jpg", 'wb') as f:
        f.write( output_image.getbuffer())
    
    # piexif.insert(new_bytes, "gps.jpg")
    print("===finish clear_chosen===")
    '''
    for tag in tags_chosen:
        im.delete(tag)
    '''
    #print(get_tags(im))
    return None


def exifd(im):
    ex = piexif.load(im.info['exif'])
    return ex
def upl1():
    im = Image.open("gps.jpg")

    metadata = im.getexif()
    print("metadata: \n", metadata)
    #im.show()
    #im.save("test.jpg") #this alone can wipe all metadata, as the saved version will be clean
    print("finished\n")
    exif = get_tags(im)
    print(exif)
    recommended_found, recommended_descriptions = get_recommended(exif)
    clear_chosen(im,recommended_found,exif) #this still doesn't work because the two types of exif data are incompatible
    print(recommended_found)

def upl2():
    im = Image.open("gps.jpg")

    metadata = im.getexif()
    print("metadata: \n", metadata)
    print("finished\n")
    exif = exifd(im)
    print(exif)
    recommended_found, recommended_descriptions = get_recommended(exif)
    clear_chosen(im, recommended_found, exif)  # this still doesn't work because the two types of exif data are incompatible
    print(recommended_found)

'''
Takes an image and returns an exif dictionary of exifTag:value
'''
def get_tags(im):
    #print(dir(im))
    exif = {
        ExifTags.TAGS[k]: v
        for k, v in im._getexif().items()
        if k in ExifTags.TAGS
    }
    print(exif)
    print("====gettags====")
    for k in exif:
        print(k)
    return exif

'''
Takes an exif dictionary and pulls out any recommended tags to be scrubbed
'''
def get_recommended(exif):
    print("====get_recommended====\n")
    rec_list = ["make", "model", "gps", "maker", "note", "location", "name",
                "date", "datetime", "description", "software", "device",
                "longitude", "latitude", "altitude"]
    found_tags = []
    found_descriptions = []
    for tag in exif:
        if any(rec in tag.lower() for rec in rec_list): #use case-insensitive version
            found_tags.append(tag)
            found_descriptions.append(exif[tag])
    print("Recommended tags found: ",len(found_tags))
    return found_tags, found_descriptions

def adjust_exif(tags_chosen,exif):
    new_exif = dict(exif)
    for tag in exif:
        if tag in tags_chosen:
            new_exif[tag] = ""
        else: new_exif[tag] = exif[tag]
    return new_exif

'''
Takes an image and clears only the chosen tags 
'''
def clear_chosen(im, tags_chosen,exif):
    print("===clear_chosen===")
    new_exif = adjust_exif(tags_chosen,exif)
    new_bytes = piexif.dump(new_exif)
    print(new_exif)
    piexif.insert(new_bytes, "gps2.jpg")
    print("===finish clear_chosen===")
    '''
    for tag in tags_chosen:
        im.delete(tag)
    '''
    #print(get_tags(im))
    return None

'''
Takes an image and clears all exif metadata (used for the simple scrub method)
'''
def clear_all(im):
    return None
#url()

#upl2()
piexample()
#using a downloaded image

#maybe try giving the user advanced options to see what kind of metadata is attached to the image
#or give them a simple solution to scrub it all clean, (or give the recommended)
#focus on apple and android metadata tags only