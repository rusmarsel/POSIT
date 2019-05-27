from PIL import Image

basewidth = 1000
filename = '.JPG'
filename_new = '.jpg'

for i in range(11):
    img = Image.open(str(i)+filename)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save('kocka_rescale'+str(i)+filename_new) 