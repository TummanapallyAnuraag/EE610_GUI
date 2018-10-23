#!/usr/bin/env python
import sys
sys.path.append("/home/anuraag/IITB/Sem3/EE610/gui/packages")
import cgi, os
import json
from skimage.io import imsave, imread

form = cgi.FieldStorage()
fileitem = form['pic']
flag = form.getvalue("flag")
message = {}
upload_path = 'images/_target'
if(flag == 'kernel'):
    upload_path = 'images/_kernel'

print ("Content-type:text/html\r\n\r\n")
if fileitem.filename:

    fn = os.path.basename(fileitem.filename)
    format = os.path.splitext(fn)[1]
    filename = upload_path + '/0' + format
    open(filename, 'wb').write(fileitem.file.read())

    message['result'] = 'The file was uploaded successfully'
    message['filename'] = filename
    message['format'] = format[1:]
    message['message'] = ''

    if ( (format == '.tif') or (format == '.tiff') ):
        I = imread(upload_path + '/0'+format)
        imsave(upload_path + '/0.png', I)
        message['result'] = 'The file was uploaded successfully'
        message['message'] = 'Browsers dont support tif images, so converted to png format..'
        message['filename'] = upload_path + '/0.png'
        message['format'] = 'png'


else:
    message['result'] = 'No file was uploaded !!'
    message['message'] = 'Some Error Occured !!'

print(json.dumps( message ))
