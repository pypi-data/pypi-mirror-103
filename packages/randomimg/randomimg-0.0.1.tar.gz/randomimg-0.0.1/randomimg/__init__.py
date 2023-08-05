import random
from PIL import Image
def create(w,h,fname):
    img=Image.new('RGB',(w,h),0)
    pixels = img.load() # create the pixel map

    for i in range(img.size[0]): # for every pixel:
        for j in range(img.size[1]):
            pixels[i,j]=(random.randrange(255),random.randrange(255),random.randrange(255)),


    img.save(fname)
def _create(w,h):
    img=Image.new('RGB',(w,h),0)
    pixels = img.load() # create the pixel map

    for i in range(img.size[0]): # for every pixel:
        for j in range(img.size[1]):
            pixels[i,j]=(random.randrange(255),random.randrange(255),random.randrange(255)),
    return img

