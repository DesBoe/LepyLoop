This script is a little help to run a huge pile of images with mothseg (https://github.com/tzlr-de/LEPY). 

It will ask you for an input folder conatining the pictures of individuals. This can be a parent directory with subfolders. Within this directory, LepyLoop will look for all images and move them into an "input" folder. 
For Lepy, you should provide paired images of moths. For that reason, individuals with only RGB or UV images are regarded as unpaired and will not be provided to LEPY. However, they can be analysed separately with LEPY. The logfile shows an overview of these unpaired images.

Most importanly, LEPYLoop creates packages of a certain number of images. You can specify this number in the beginning. Each package will be executed by LEPY. 
This approach might avoid an memory error on your device. Each package is executed with LEPY and a results folder is created, as you would expect it from LEPY. 
At the end, all result folders are combined to one RESULT Folder and a combined stats output table is generated, both in csv and excel. All analysed images are then sorted back

Tested on MACOS 15.1 and Python 3.12.0

Note for Windows users:

Please go to start - settings - App execution aliases and turn off python.exe and python3.exe
