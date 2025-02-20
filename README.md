This script is a little help to run a huge pile of images with mothseg (https://github.com/DiKorsch/mothseg). 
It expects a directory with  images. these can be of any type. It will look for all images and move them into an input folder. 
For Lepy, we need paired images of the moths, so it detects individuals with only RGB or UV images and regards them to a unpaired folder. 
The logfile shows an overview. Some moths might have additional photos, these will be listed as extra photos.
Most importanly, it creates packages of a certain number of images. each package will be executed by mothseg. 
This approach might avoid an memory error on your device. Each package is executed with mothseg and a results folder is created, as you would expect it from Lepy. 
At the end, all result folders are combined to one RESULT Folder and a combined stats output table is generated, both in csv and excel. All analysed images are then sorted back

Tested on MACOS 15.1 and Python 3.12.0

Note for Windows users:

Please go to start - settings - App execution aliases and turn off python.exe and python3.exe
