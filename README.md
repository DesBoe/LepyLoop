This tool is a help to run a huge pile of images with LEPY (https://github.com/tzlr-de/LEPY). 
For detailed information, please refer to Correa-Carmona et al, 2025. Preprit @ https://doi.org/10.32942/X2WS78

Note: 
LEPY can be executed completely without this assistant scripts. However, this scripts might help you to organize your data in an easy way.


LLmain :

This script will ask you for an input folder conatining the pictures of individuals. This can be a parent directory with subfolders. Within this directory, LepyLoop will look for all images and move them into an "input" folder. 
For Lepy, you should provide paired images of moths. For that reason, individuals with only RGB or UV images are regarded as unpaired and will not be provided to LEPY. However, they can be analysed separately with LEPY. The logfile shows an overview of these unpaired images.

Most importanly, LEPYLoop creates packages of a certain number of images. You can specify this number in the beginning. Each package will be executed by LEPY. 
This approach might avoid an memory error on your device. Each package is executed with LEPY and a results folder is created, as you would expect it from LEPY. 
At the end, all result folders are combined to one RESULT Folder and a combined stats output table is generated, both in csv and xslx. All analysed images are then sorted back


LLCheck :

This script only checks for unpaired images of RGB + UV. you will need to provide a directory containing your images. Image names must follow a standardized naming scheme, e.g:
  EcEs-Lep-00001.tif
  EcEs-Lep-00001uv.tif
  EcEs-Lep-00002.tif
  EcEs-Lep-00002uv.tif
  EcEs-Lep-00003.tif
  EcEs-Lep-00003uv.tif
  ...
Next, youll get asked for the number of digits in the image names. in this example, it is 5.
The resut of this script is a logfile that states which RGB or UV images are missing
additnally, you get a csv table of all image names including extra photos and proboscis photos, if provided.


Happy analyzing :)


Tested on MACOS 15.1 and Python 3.12.0

Note for Windows users:

Please go to start - settings - App execution aliases and turn off python.exe and python3.exe
