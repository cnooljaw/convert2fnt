# -*- coding: utf-8 -*-

from PIL import Image

def joint_image(out_image_name,image_dict):
	outW=0
	outH=0
	for config in image_dict:
		size=image_size_at_path(config["image"])
		outW+=size[0]
		outH=max(size[1],outH)

	print "out image size %dx%d" %(outW,outH)

	toImage = Image.new('RGBA', (outW, outH))

	x=0
	for config in image_dict:
		fromImage=Image.open(config["image"])
		toImage.paste(fromImage,( x, 0))
		print "\t %s offset %d" %(config["image"],x)
		x+=fromImage.size[0]

	toImage.save(out_image_name)

def generate(path,name,image_dict):
	print path,name,image_dict

	fnt_name        = path+"/"+name+".fnt"
	image_name      = name+".png"
	fnt_define      = dict()
	index           = 0
	xOffset         = 0
	max_height      = 0
	max_width       = 0
	fnt_define_item = list()

	for config in image_dict:
		image_size                       = image_size_at_path(config["image"])
		fnt_define_item_data             = dict()
		fnt_define_item_data["id"]       = ord(config["character"])
		fnt_define_item_data["x"]        = str(xOffset)
		fnt_define_item_data["y"]        = str(0)
		fnt_define_item_data["width"]    = str(image_size[0])
		fnt_define_item_data["height"]   = str(image_size[1])
		fnt_define_item_data["xoffset"]  = str(0)
		fnt_define_item_data["yoffset"]  = str(0)
		fnt_define_item_data["xadvance"] = str(image_size[0])
		fnt_define_item_data["page"]     = str(0)
		fnt_define_item_data["chnl"]     = str(0)
		fnt_define_item_data["letter"]   = config["character"]

		fnt_define_item.append(fnt_define_item_data)

		index+=1
		xOffset+=image_size[0]
		max_width=max(max_width,image_size[0])
		max_height=max(max_height,image_size[1])

	fnt_define["data"]=fnt_define_item
	fnt_define["size"]=str(max_width)
	fnt_define["lineHeight"]=str(max_height)
	fnt_define["base"]=str(max_width)
	fnt_define["scaleW"]=str(xOffset)
	fnt_define["scaleH"]=str(max_height)
	fnt_define["file"]=image_name
	fnt_define["count"]=len(image_dict)

	image_name=path+"/"+image_name

	create_fnt_file(fnt_name, fnt_define)
	print "make:",fnt_name,"done!"
	joint_image(image_name,image_dict)
	print "make:",image_name,"done!"
	print"*************************************************************"

"""
-define
----size		#face size
----lineHeight	#line height
----base		#???
----scaleW		#scale width
----scaleH		#scale height
----file 		#texture file name
----count 		#char count
----data 		#item data
--------data[0]
------------id
------------x
------------y
------------width
------------height
------------xoffset
------------yoffset
------------xadvance
------------page
------------chnl
------------letter
------------id
"""

def create_fnt_file(fnt_name,fnt_define):
	write_file=open(fnt_name,"w")

	head_msg="""info face="Arial-Black" size=%s bold=0 italic=0 charset="" unicode=0 stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing=2,2
common lineHeight=%s base=%s scaleW=%s scaleH=%s pages=1 packed=0
page id=0 file="%s"
chars count=%s
""" % (fnt_define["size"],fnt_define["lineHeight"],fnt_define["base"],fnt_define["scaleW"],fnt_define["scaleH"],fnt_define["file"],fnt_define["count"])

	write_file.write(head_msg.encode("UTF-8"))

	for i in range(0,int(fnt_define["count"])):
		data=fnt_define["data"][i]
		line="char id=%s x=%s y=%s width=%s height=%s xoffset=%s yoffset=%s xadvance=%s page=%s chnl=%s letter=\"%s\"\n" %(data["id"],data["x"],data["y"],data["width"],data["height"],data["xoffset"],data["yoffset"],data["xadvance"],data["page"],data["chnl"],data["letter"])
		write_file.write(line.encode("UTF-8"))

	write_file.close()


def image_size_at_path(path):
	im=Image.open(path)
	# print "\tImage ",path,"size is:",im.size
	return im.size