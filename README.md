![Logo](https://github.com/user-attachments/assets/10255357-c6aa-45f0-8b8f-2fdeae06cfae)
This script is a little help to run a huge pile of images with Lepy (https://github.com/tzlr-de/LEPY). 

It will ask you for an input folder conatining the pictures of individuals. This can be a parent directory with subfolders. Within this directory, LepyLoop will look for all images and move them into an "input" folder. 

You can execute Lepy with the help of LepyLoop for RGB moth images and paires of RGB and UV images. LepyLoop will ask you for one of these modi at the beginnig of its execution. 
Please note:
If you select RGB+UV as mode, LepyLoop checks for unmatched images. if one specimen is only represented with either UV or RGB image, these will be regarded as unpaired and are not be provided to LEPY. However, they can be analysed separately with LEPY. The logfile shows an overview of these unpaired images.

Most importanly, LEPYLoop creates packages of a certain number of images. You can specify this number in the beginning. Each package will be executed by LEPY. 
This approach might avoid an memory error on your device. Each package is executed with LEPY and a results folder is created, as you would expect it from LEPY. 
At the end, all result folders are combined to one RESULT Folder and a combined stats output table is generated, both in csv and excel. All analysed images are then sorted back

Tested on MACOS 15.1 and Python 3.12.0

Note for Windows users:

Please go to start - settings - App execution aliases and turn off python.exe and python3.exe
