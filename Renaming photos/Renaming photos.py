#!/usr/bin/env python
# coding: utf-8

# # Renaming photos
# ## Author(s): Brian Nhan Thien Chung (UCI NATURE research technician)
# ### Created on: Friday August 28, 2020 by Brian Nhan Thien Chung
# ### Last edited on: Wednesday September 9, 2020 by Brian Nhan Thien Chung
# 
# The purpose of this Jupyter Notebook is to rename photos. As a proof of concept, photos taken at Bonita Canyon will be renamed before photos from other camera locations are renamed.
# 
# After a successful proof of concept, functions are generated out of the code that was used to rename photos taken at Bonita Canyon. This allows for an abstraction of the renaming process down to a single step: calling a single function to rename photos from a camera.
# 
# This Jupyter Notebook reads in a csv file of re-labeled animal photos as a pandas dataframe. This notebook can rename photos from one camera at a time. It assumes that photos that the user wants to rename from a particular camera are in an unzipped folder that is in the same directory as this notebook. The location of the csv file is assumed to be in the directory titled "Species distribution analysis". If these assumptions are not met, then this notebook cannot rename photos, and the user will have to manually code out the renaming process.
# 
# The notebook will compare the photos of the camera that the user wants to rename with the photos in the csv file of re-labeled animal photos. The photos will be copied, and each copied photo will have a name with the following components:
# 
# (1) The original image number
# 
# (2) 2-letter camera code
# 
# (3) Date the photo was taken
# 
# (4, optional) Species, if the photo was noted to have a species in the csv file. If not, then this element is missing.
# 
# To rename photos of a particular camera, please ensure that the above assumptions are met first. Then simply call the following function: renamePhotosInCamera(). This function will then call 2 other functions. Ignore these 2 other functions unless if there is a bug and just call this function. This function takes 2 arguments in the following order:
# 
# (1) Folder name of the camera whose photos the user wants to rename. Simply copy and paste the folder name in for this argument.
# 
# (2) 2-letter camera code of the particular camera whose photos the user wants to rename
# 
# Both arguments must have the string data type.
# 
# The function does not return anything. It can only rename photos from one camera at a time. To rename multiple cameras, simply repeat the steps and follow the assumptions above: the user must ensure that each camera whose photos the user wants to rename each have a directory that is in the same directory as this notebook. The user must then call this function and put in the folder name and the 2-letter camera code as strings. Simply repeat the steps and follow the assumptions above multiple times until photos from every camera the user wants to rename had been renamed.
# 
# The following folder structures are the only acceptable folder structures for this notebook:
# 
# (1) overall camera folder -------> subfolders ----------> photos
# 
# (2) overall camera folder -------> photos
# 
# Please ensure that these folder structures are met. No other structures are acceptable in this notebook.
# 
# Please ensure that there are no periods in photo names other than the period before the photo's file extension.
# 
# Also, this is intended to rename very large amounts of photos. Photos from Research Park alone numbered approximately 32 gigabytes. Since this code duplicates photos, the total number of photos jumped up to 64 gigabytes after renaming. Please ensure that your machine has enough storage space to rename photos.
# 
# Now, have fun!

# In[3]:


get_ipython().run_line_magic('autosave', '10')


# In[4]:


import os
import shutil
from pathlib import Path
import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS


# In[5]:


ogcwdStr = os.getcwd()
ogcwd = Path(ogcwdStr)
os.chdir(ogcwd)
dirList = os.listdir()
# print(os.getcwd())
print(dirList)


# In[6]:


overallDirectory = Path(os.path.dirname(ogcwd))
speciesDistriAnalyDir = "Species distribution analysis"
relabeledPhotosDir = overallDirectory/speciesDistriAnalyDir
relabeledPhotos = "re-labeled animal photos.csv"

relabeledPhotos = pd.read_csv(relabeledPhotosDir/relabeledPhotos)
relabeledPhotoNames = relabeledPhotos["ImageNumber"].tolist()
cameraCounts = relabeledPhotos.groupby("LocCode")["LocCode"].count()
cameraCodes = cameraCounts.index.tolist()
cameraCodes


# In[7]:


def makeRenamedDirectories(overallCameraDir: "name of camera folder"):
    """Make directories to contain renamed photos. Please copy in the name of the camera folder
    in for the parameter of this function. This function returns 2 lists of subdirectory paths
    (Path object) and 2 path objects: the path of overallCameraDir and the path for the renamed
    version of overallCameraDir"""
    overallCameraDir_renamed = overallCameraDir + " - renamed"
    overallCameraDir_renamedPath = ogcwd/overallCameraDir_renamed
    if os.path.exists(overallCameraDir_renamedPath) == False:
        os.mkdir(overallCameraDir_renamedPath)
    overallCameraDirPath = ogcwd/overallCameraDir
    cameraFileAndSubdirList = os.listdir(overallCameraDirPath)
    cameraSubdirList = []
    for fileOrSubdirectory in cameraFileAndSubdirList:
        fileOrSubdirectoryPath = overallCameraDirPath/fileOrSubdirectory
        if os.path.isdir(fileOrSubdirectoryPath) and "renamed" not in fileOrSubdirectory:
            cameraSubdirList.append(fileOrSubdirectory)
    cameraSubdirList_renamed = []
    for index in range(len(cameraSubdirList)):
        subdirectory_renamed = cameraSubdirList[index] + " - renamed"
        cameraSubdirList[index] = overallCameraDirPath/cameraSubdirList[index]
        subdirectory_renamedPath = overallCameraDir_renamedPath/subdirectory_renamed
        cameraSubdirList_renamed.append(subdirectory_renamedPath)
        if os.path.exists(subdirectory_renamedPath) == False:
            os.mkdir(subdirectory_renamedPath)
        print(subdirectory_renamed)
    return cameraSubdirList, cameraSubdirList_renamed, overallCameraDirPath, overallCameraDir_renamedPath


# In[8]:


def renamingPhotosInSingleDirectory(directoryPath, renameddirectoryPath, cameraCode: "2 letter camera code") -> None:
    """Rename photos in only a single directory. If a camera has multiple subdirectories for photos
    from multiple periods, then this function needs to be called multiple times to rename every photo
    in each subdirectory. If a camera has no subdirectories, then this function will rename every photo
    within that camera directory"""

    files = os.listdir(directoryPath)
    ogImages = []
    for file in files:
        extension = file.split(".")[-1]
        if extension.lower() == "jpg" or extension.lower() == "jpeg":
            ogImages.append(file)
    for OldImage in ogImages:
        PILimage = Image.open(directoryPath/OldImage)
        exifOldImage = PILimage.getexif()
        tagsList = []
        dataList = []
        for tag_id in exifOldImage:
        # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exifOldImage.get(tag_id)
        # decode bytes 
            if isinstance(data, bytes):
                try:
                    data = data.decode()
                except:
                    print("Unicode decode error for " + OldImage + "; Should be inconsequential.")
            tagsList.append(tag)
            dataList.append(data)
        metadata = {tagsList[index]: dataList[index] for index in range(len(tagsList))}
        dateTime = metadata["DateTimeOriginal"]
        dateTimeList = dateTime.split(" ")
        dateComponents = dateTimeList[0].split(":")
        year = dateComponents[0]
        month = dateComponents[1]
        day = dateComponents[2]
        formattedDate = "-".join([year, month, day])

        oldImageNameParts = OldImage.split(".")
        oldImageName = oldImageNameParts[0]
        fileExtension = "." + oldImageNameParts[1]
        newImageNameList = [oldImageName, cameraCode, formattedDate]
        temporaryName = "-".join(newImageNameList)
        speciesList = []
        for image in relabeledPhotoNames:
            ogImageNameList = image.split("-")
            ogImageName = ogImageNameList[0]
            ogImageCameraCode = ogImageNameList[1]
            ogImageDateParts = [ogImageNameList[2], ogImageNameList[3], ogImageNameList[4]]
            ogImageFormattedDate = "-".join(ogImageDateParts)
            if (ogImageName in oldImageName and ogImageCameraCode == cameraCode and ogImageFormattedDate == formattedDate) or (temporaryName in image):
                print("The original image name on the relabeled photos csv is {}".format(ogImageName))
                species = ogImageNameList[-1]
                temporaryName = image
                if species not in speciesList:
                    speciesList.append(species)
                break
        wildAnimals = ["bird and raccoon", "rabbit and bird", 
                       "rabbit and coyote", "rabbit and unknown animal(s)"]
        wildAnimalAndHuman = ["bird and human", "human + dog + rabbit", "rabbit and human"]
        
        processedSpeciesList = []
        for index in range(len(speciesList)):
            if speciesList[index] not in wildAnimals and speciesList[index] not in wildAnimalAndHuman:
                processedSpeciesList.append(speciesList[index])
            elif speciesList[index] in wildAnimals and "wild animals" not in processedSpeciesList:
                processedSpeciesList.append("wild animals")
            elif speciesList[index] in wildAnimalAndHuman and "animal and human" not in processedSpeciesList:
                processedSpeciesList.append("animal and human")
        speciesList = processedSpeciesList
        for species in speciesList:
            speciesFolderPath = renameddirectoryPath/species
            if os.path.exists(speciesFolderPath) == False:
                os.mkdir(speciesFolderPath)
        temporaryNameSplitted = temporaryName.split("-")
        species = temporaryNameSplitted[-1]
        newImageName = temporaryName + fileExtension
        oldImagePath = str(directoryPath/OldImage)
        miscellaneousFolderPath = renameddirectoryPath/"miscellaneous"
        if os.path.exists(miscellaneousFolderPath) == False:
            os.mkdir(miscellaneousFolderPath)
        if species in speciesList or species in wildAnimals or species in wildAnimalAndHuman:
            if species in wildAnimals:
                species = "wild animals"
            elif species in wildAnimalAndHuman:
                species = "animal and human"
            speciesFolderPath = renameddirectoryPath/species
            newImagePath = str(speciesFolderPath/newImageName)
        else:
            newImagePath = str(miscellaneousFolderPath/newImageName)

        print(newImageName)
        if os.path.exists(newImagePath) == False:
            shutil.copy(oldImagePath, newImagePath)
    return


# In[9]:


speciesCounts = relabeledPhotos.groupby("Species")["Species"].count()
speciesCounts


# In[10]:


def renamePhotosInCamera(cameraName: "string representing name of camera folder", cameraCode: "2-letter camera code"):
    """Renames photos of a camera. This initially calls the makeRenamedDirectories() function to make
    empty directories that will later hold renamed photos. It will then call
    the renamingPhotosInSubdirectory() function a few times depending on how many subdirectories
    are in the original camera folder."""
    subdirPaths, subdir_renamedPaths, cameraPath, renamedCameraPath = makeRenamedDirectories(cameraName)
    if len(subdirPaths) == 0:
        renamingPhotosInSingleDirectory(cameraPath, renamedCameraPath, cameraCode)
    elif len(subdirPaths) > 0:
        for index in range(len(subdirPaths)):
            subdirPath = subdirPaths[index]
            subdir_renamedPath = subdir_renamedPaths[index]
            renamingPhotosInSingleDirectory(subdirPath, subdir_renamedPath, cameraCode)
    return
    


# In[11]:


# renamePhotosInCamera("Bonita Canyon (Under the Bridge)", "BC")
# renamePhotosInCamera("Research Park", "RP")
# renamePhotosInCamera("test camera", "AT")


# ## Research Park

# In[12]:


# renamePhotosInCamera("1_Respark_032219_040419", "RP")


# In[13]:


# renamePhotosInCamera("2_Respark_040419_042519", "RP")


# In[14]:


# renamePhotosInCamera("3_Respark_042519_050919", "RP")


# In[15]:


# renamePhotosInCamera("4_Respark_050919_052319", "RP")


# Here's some code to check the species distribution of the actual renamed photos vs the csv file of relabeled animal photos. This chunk was originally written to look at the species distribution of the actual renamed photos in Research Park, NOT the relabeled animal photos of Research Park in the csv file of relabeled animal photos. However, this chunk of code can be customized for other cameras as well. Please customize this however you see fit.

# In[16]:


# renamedFolders = []
# for directory in dirList:
#     if "renamed" in directory:
#         renamedFolders.append(directory)

# overallCounts = []
# for indexRenamed in range(len(renamedFolders)):
#     directoryPath = ogcwd/renamedFolders[indexRenamed]
#     speciesFolders = os.listdir(directoryPath)
#     folderName = renamedFolders[indexRenamed]
#     for indexSpecies in range(len(speciesFolders)):
#         speciesFolderPath = directoryPath/speciesFolders[indexSpecies]
#         speciesFolder = speciesFolders[indexSpecies]
#         speciesCount = len(os.listdir(speciesFolderPath))
#         entry = [folderName, speciesFolder, speciesCount]
#         print(entry)
#         overallCounts.append(entry)

# columnLabels = ["Photo period", "Species", "Count"]

# researchParkCounts = pd.DataFrame(data = overallCounts, columns = columnLabels)
# researchParkCounts

# counts = researchParkCounts.groupby("Species")["Count"].sum()
# counts


# In conclusion, I think that my renaming algorithm keeps similar enough species proportions despite the renaming algorithm resulting in some animal photos being misclassified as "miscellaneous", so the actual number of animal photos for certain animals are lower. This lowering is due to initial human error (just error that's not from me) from entering data into the spreadsheets that were compiled into the overall Camera_METADATA_UCI spreadsheet and then analyzed by me. The dates the CEB interns or anyone who manually reviewed photos entered into these spreadsheets were different from the dates in the actual photo.
