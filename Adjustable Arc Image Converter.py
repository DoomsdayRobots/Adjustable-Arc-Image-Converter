# This program was written by David Metcalf
# on or about the time of ‎‎December ‎31, ‎2020, ‏‎7:05:03 AM
# Please give credit where credit is due.
#
# I googled a picture of a "cat head" I honestly do not know who
# owns the rights to this picture, if any one know who this
# picture belongs to, I would be happy to give them credit
# here, or ask for their permission to use the image.
# Please drop a note in the readme file if you know who
# ons the rights to this picture.
#
# I found some of the code I'm using over here at this web page.
# https://github.com/aydal/Cylinderical-Anamorphosis/blob/master/anamorph.py
# I found the above formentioned web page, when I found the one below.
# I found the one below, by typing "opencv python animorphic"
# into a google web search.
# https://stackoverflow.com/questions/54271864/anamorphosis-in-python
# with in this web page their was another link to a git hub page found here
# https://github.com/aydal/Cylinderical-Anamorphosis/blob/master/anamorph.py
#
# my current github repo is here
# https://github.com/DoomsdayRobots/Adjustable-Arch-Image-Converter
# Ok.. Lets get started!!!


def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
        #print("The package '"+str(package)+"' is already installed.")
        #print("")
    except ImportError:
        #print("The package "+str(package) +" is not installed.")
        #cont1 = input(str("Did you want to install '"+package+"'? ( Y/N ) "))
        #print("")
        #if cont1 == 'Y' or cont1 == 'y':
            import pip
            pip.main(['install', package])
            globals()[package] = importlib.import_module(package)
            print("The package '"+str(package)+"' was missing.")
            print("Installed '"+str(package)+".")
            print("")

def percent_scale(src,percentageToScaleBy):
    oh,ow = src.shape[:2] # get shape information
    scale = percentageToScaleBy 
    scaleW = int(ow * (scale / 100)) # scale width by percentage
    scaleH = int(oh * (scale / 100)) # scale Height by percentage
    src = cv2.resize(src,(scaleW,scaleH), interpolation = cv2.INTER_AREA)
    #cv2.imshow("Scaled Picture",src)
    return src

# This is the trackbar callback fucntion.
# It does nothing, but it is still required
# for the trackbar to work properly.
def nothing(x):
	pass

def convt(R,b,c):
        q = int(math.trunc((b*cols/(2*math.asin(1)))))
        p = int(math.trunc(c-R))
        result = (q,p)
        return result

def arch_Image(sourceImage,innerRadius,offset = True):
        modifier = 10
        innerRadius = innerRadius * modifier
        innerDiameter =  innerRadius*2 
        c = int(innerRadius + rows)
        
        if offset == False:
                imageCylinderPlaceHolderOffset = 0
        else:
                imageCylinderPlaceHolderOffset = innerRadius
                
        # make a new blank image to place the freshly created warped image into
        # with enough room for placing a cylinderical object to project onto.
        blank = np.zeros([int(c + imageCylinderPlaceHolderOffset),2*c,3],dtype = np.uint8)
        blank.fill(0)

        # We will warp our original image.    
        for i in range (0,2*c):
                for j in range (1,c):
                        b = math.atan2(j,i-c)
                        R = math.sqrt(j * j + math.pow(i - c, 2))
                        
                        if R >= innerRadius and R <= c:
                                (q,p) = convt(R,b,c)
                                #Lets put our warped image into the blank image space.
                                blank[c-j,i-1] = sourceImage[p-1,q-1]
        return blank

def get_image_name():
    # get user input for which image to use.
    user_input = False
    while user_input == False:
        print("Please make sure your file is in the same file location as.")
        print("'Adjustable Arc Image Converter.py'.  ")
        print("Please enter the name of the image you wish to use.")
        print("please include the extention type in the name you enter.")
        print("For example you could type 'cat.jpg' as the name to enter.")
        image_name = input(str("Give it a try...   "))
        print("")
        file_exists = os.path.exists(image_name)

        if file_exists == False:
            print("Oops! looks like the file name you entered dosen't exsist")
            print("or it's not with in the same directory as this program.")
            print("Please Try again...")
            print("")
        if file_exists == True:
            user_input = True    
            return image_name
        
# Check if the required libraries are installed.
# If not then install them for the user.                  
install_and_import('cv2')
install_and_import('numpy')
install_and_import('math')

import cv2
import numpy as np
import math
# The os module, comes as a pre-installed module in python.
# Their is no need to check if it is installed.
import os 
from os.path import exists


# Some variable that will help us throughout the program. 
slider1_max = 20
slider1_min = 0

title_window = "Adjustable Arc Image Converter"
trackbar_message = "Inner Dia"

global val
val = 0

# Main program starts here....

# Get image to use through user input.
image_name = get_image_name()

img = cv2.imread(image_name)
#cv2.imshow("Original Image",img) # Displays the original image.

# Scales original image
img = percent_scale(img,25) # Scales original image by a set percentage.
#cv2.imshow("Scaled Image",img) # Displays the scaled image.

# Get image shape info to use later on.
(rows,cols) = img.shape[:2]

print("To save your output press the 's' key while your cursor")
print("is in the 'Adjustable Arc Image Converter' window.")
print("")
print("To quit this program press the 'esc' key while your cursor")
print("is in the 'Adjustable Arc Image Converter' window.")

# Creates a fraimed window in which to display things.
cv2.namedWindow(title_window)

# Creates a trackbar for the user to interact with.
cv2.createTrackbar(trackbar_message, title_window, slider1_min, slider1_max,nothing)

# Update the image baised on the user defined trackbar position.
while(1):
    trackbar_val = cv2.getTrackbarPos(trackbar_message, title_window)
    arc = arch_Image(img,trackbar_val)
    cv2.imshow(title_window,arc)

    # Allow the user to save the picture if they want to.
    k = cv2.waitKey(1)
    if k == ord('S') or k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('filername1.jpg',arc)
        print("saved picture")
        #cv2.destroyAllWindows()
        #break
        
    #k = cv2.waitKey(1)
    elif k == 27: # wait for ESC key to exit
        print("Done running program!")
        cv2.destroyAllWindows()
        break
