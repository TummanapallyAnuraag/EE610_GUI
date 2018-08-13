# EE610_GUI
This Repository is part of an Assignment of the course EE610 at EE Department, IIT Bombay.

The main goal of this is to make a small image editor tool.

## Requirements
* Apache, php, python 
* Python Modules: numpy, skimage

## Features
This Code can perform the following tasks:
* Upload an Image
* Do Image histogram equalisation
* Do Gamma Correction
* Do Log Transform
* Save the Image

## Key Words
**AJAX, POST, GET, CGI**

There is nothing to get scared about these terms, they are just some fancy names.

* AJAX: Used for sending / receiving Information without reloading a web page

You can refer [this page](https://www.w3schools.com/xml/ajax_intro.asp) for a basic introduction and working examples.

* POST, GET: Method used for sharing Information in the above step

You can refer [this page](https://www.w3schools.com/tags/ref_httpmethods.asp) for more information.

* CGI: Used in APACHE settings to enable execution of python scripts

You can refer [this pgae](https://www.tutorialspoint.com/perl/perl_cgi.htm) for more information.

* .htaccess: settings can be mentioned in this file for each specific directory.

You can refer [this page](http://www.htaccess-guide.com/) for more information.

## SETUP
I have tested this code in xubuntu 16.04 and ubuntu 16.04, but i am 99% sure that this will work in all ubuntu machines..

Following are the steps to be followed for using this code on a fresh machine

* Setup APACHE.

`sudo apt install apache2`

* Copy this code to web directory (/var/www/html/)

`cd /var/www/html`

`git clone https://github.com/TummanapallyAnuraag/EE610_GUI.git gui`

* Enable CGI execution in apache2

`sudo a2enmod cgi`

`sudo service apache2 restart`

* Add the following lines of code in /etc/apache2/sites-enabled/000-default.conf

```
<Directory "/var/www/html/gui">
	AllowOverride All
</Directory>
```

* After any kind of changes to apache2 configuration files, we need to reload it.

`sudo service apache2 restart`

* Check if CGI scripts are being run, a hello world program is made for this special purpose only.

Check the CGI script working by going to [http://localhost/gui/scripts/hello.py](http://localhost/gui/scripts/hello.py)

* Once all the above steps are done, the GUI can be seen at [http://localhost/gui](http://localhost/gui)

But if you face any problems while any of the steps, you can debug them with help of next step

* (Optional) If you want debug information, add this line of code to the same 000-default.conf file

`LogLevel debug`

You can see the debug information in /var/log/apache2/error.log

This command comes in handy at times..

`tail -f /var/log/apache2/error.log`

Web Help: look in [StackOverflow](https://stackoverflow.com/)

Worst case scenario: You can always drop a mail to me. You can find my details [here](https://www.ee.iitb.ac.in/~anuraagt/)

* Remember: Always restart apache2 service whenever you chnage the configuration files of apache2

## SOME COMMON ISSUES

* If you are not able to upload images..

a) Check if the folder `images` has 777 permissions. If not you can do so by using

`sudo chmod -R 777 images/`

The -R is used for recursion (folder within folder scenario)

b) The image upload size must be more than the permissible limit.

You can check and change this *permissible limit* in /etc/php/7.0/apache2/php.ini
