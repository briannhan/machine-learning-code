#!/usr/bin/env python
# coding: utf-8

# # Species distribution
# 
# ### Author: Brian Nhan Thien Chung (UCI NATURE Research Technician)
# 
# #### Created on: Saturday August 15, 2020 by Brian Nhan Thien Chung
# #### Last edited on: Friday September 4, 2020 by Brian Nhan Thien Chung
# This Jupyter Notebook was created to analyze the species distribution of photos from the wildlife cameras operated by UCI NATURE. This Jupyter Notebook will run through a spreadsheet titled "Camera_METADATA_UCI" that records photos from each camera and describes the species of animal(s) in each photo. This notebook will then produce proportions of each species observed from each camera. This data will be used to create a training set of photos to train a neural network that identifies the species observed from the cameras operated by UCI NATURE.
# 
# Note: this spreadsheet does not contain any empty photos. Every photo contains an animal or a human vehicle.
# 
# This notebook is divided into sections with each section having a unique purpose. Each section will also produce at least 1 product. Depending on the nature of the product, some will be exported while others will be saved in this notebook. The exported products will be in the same directory as this notebook and as the "Camera_METADATA_UCI.csv" file. The exported products consist of graphs (which can be opened using any image viewer) and csv files (text files that can be opened up using any spreadsheet programs such as Microsoft Excel or Google Sheets). The sections are:
# #### Section 1
# Processing "Camera_METADATA_UCI.csv" spreadsheet to prevent the double counting of duplicate entries of the same photo by the same camera taken on the same day. The data is exported as a new csv file titled "re-labeled animal photos.csv"
# #### Section 2
# Read in the new csv file and count the species observed for each camera. This section will produce the total number of photos taken by each camera and a 2-dimensional numpy array describing the counts and proportions of species observed for each camera. This section does not export any of its products, but the products will be used and then exported in the following sections.
# #### Section 3
# Plot the products from section 2 (counts and proportions of each species from each camera) as bar graphs for each camera. The graphs will be saved in the same directory as this book. When the original author produced these graphs, he then moved these graphs to a new folder he created in the directory that holds this spreadsheet.
# #### Section 4
# Sort each camera by the number of photos each camera takes and then export this information as a new csv file titled "Total photos from each camera.csv"

# #### Edit dates
# Saturday 8/15/2020 - Brian Nhan Thien Chung
# 
# Sunday 8/16/2020 - Brian Nhan Thien Chung
# 
# Monday 8/17/2020 - Brian Nhan Thien Chung
# 
# Thursday 8/20/2020 - Brian Nhan Thien Chung
# 
# Friday 8/21/2020 - Brian Nhan Thien Chung
# 
# Friday 8/28/2020 - Brian Nhan Thien Chung
# 
# Friday 9/4/2020 - Brian Nhan Thien Chung

# In[58]:


import numpy as np
import matplotlib.pyplot as py
import pandas as pd

#this jupyter notebook was written using a dark theme. The dark theme is produced from
#the lines of code below. If future users wish to have the same theme, then
#the following lines of code installs the jupyterthemes module and sets the theme
#of this notebook to the monokai theme:
# !pip install jupyterthemes
# import jupyterthemes as jt
# !jt -t gruvboxd
# from jupyterthemes import jtplot
# jtplot.style(theme = "gruvboxd")

#the documentation of the jupyterthemes module can be referenced from this link:
#https://github.com/dunovank/jupyter-themes

#For uploading onto GitHub, the author will revert the theme back to the default theme
#of Jupyter Notebooks with the following line:
# !jt -r


# In[59]:


get_ipython().run_line_magic('autosave', '15')


# ### Section 1

# In[60]:


photoEntries = pd.read_csv("Camera_METADATA_UCI.csv")
lowerCaseSpecies = photoEntries["Species"].str.lower()
lowerCaseSpecies[lowerCaseSpecies == "s ke"] = "snake"
print(lowerCaseSpecies[lowerCaseSpecies == "snake"])
photoEntries["Species"] = lowerCaseSpecies
print(photoEntries)


# Reformatting time and date

# In[61]:


date = photoEntries["Date"]
print(date)
print('\n')

timeList = photoEntries["Time"].tolist()
print(timeList[:5])
print('\n')
for index in range(len(timeList)):
    if "PM" in timeList[index]:
        splittedTime = timeList[index].split(" ")
        formattedTime = splittedTime[0] + ":00"
        timeList[index] = formattedTime
        print(timeList[index])
print('\n')
for time in timeList:
    if "PM" in time:
        print(time)
time = pd.Series(timeList)
photoEntries["Time"] = time
print(time)
print('\n')
datetime = pd.to_datetime(date + " " + time)
print(datetime)
print('\n')
photoEntries.insert(8, "datetime", datetime)
# date = pd.to_datetime(arg = date, errors = "raise")
# photoEntries["Date"] = date
# print(date)
print('\n')
print(photoEntries)


# In[62]:


photoEntriesList = photoEntries.values.tolist()
for entry in photoEntriesList:
    print(entry)


# In[63]:


cameraCountsSeries = photoEntries.groupby("Location")["Location"].count()
cameras = cameraCountsSeries.index.tolist()


# While looking through the original spreadsheet, the original author of this notebook found that there are many entries of the same photo next to each other. An image would be reported in 2 rows next to each other. This is due to there being 2 different animals observed in the same photo. The following chunk(s) of code will process this so that the same photo is not counted twice. The image names will also be re-labeled, and the data will be re-formatted and be exported as a new csv file

# In[64]:


animalsList = []
for entry in photoEntriesList:
    animalName = entry[4].lower()
    if animalName not in animalsList:
        animalsList.append(animalName)

for animal in animalsList:
    print(animal)
    
#in the original spreadsheet, snake entries were denoted as "s ke" rather than "snake"
animalsList[-1] = "snake"
print(animalsList)

horseAndHumanObservations = []
dogAndHumanObservations = []
rabbitAndHumanObservations = []
coyoteAndRabbitObservations = []
duplicates = []
birdAndHumanObservations = []
rabbitAndUnknownObservations = []
miscellaneousObservations = []
otherDuplicates = []


actualTotalPhotos = []

for index in range(len(photoEntriesList)):
    animalIndex = 4
    
    previousEntry = photoEntriesList[index - 1]
    currentEntry = photoEntriesList[index]
    
    previousEntryImageNumber = previousEntry[2]
    previousEntryAnimal = previousEntry[animalIndex].lower()
    previousEntryDate = previousEntry[6]
    previousEntryTime = previousEntry[7]
    
    currentEntryImageNumber = currentEntry[2]
    currentEntryAnimal = currentEntry[animalIndex].lower()
    currentEntryDate = currentEntry[6]
    currentEntryTime = currentEntry[7]
    currentEntryDateTime = currentEntry[8]
    
    if previousEntryImageNumber == currentEntryImageNumber:
        newEntry = []
        camera = currentEntry[0]
        LocCode = currentEntry[1]
        ImageQuality = currentEntry[3]
        species = ""
        NumIndividuals = ""
        
        newEntry.append(camera)
        newEntry.append(LocCode)
        newEntry.append(currentEntryImageNumber)
        newEntry.append(ImageQuality)
        newEntry.append(species)
        newEntry.append(NumIndividuals)
        newEntry.append(currentEntryDate)
        newEntry.append(currentEntryTime)
        newEntry.append(currentEntryDateTime)
        
        if (previousEntryAnimal == "horse" and currentEntryAnimal == "human") or (previousEntryAnimal == "human" and currentEntryAnimal == "horse"):            
            species = "horse and human"
            horseAndHumanObservations.append(newEntry)
            
        elif (previousEntryAnimal == "domestic dog" and currentEntryAnimal == "human") or (previousEntryAnimal == "human" and currentEntryAnimal == "domestic dog"):
            species = "dog and human"
            dogAndHumanObservations.append(newEntry)
        
        elif (previousEntryAnimal == "rabbit" and currentEntryAnimal == "human") or (previousEntryAnimal == "human" and currentEntryAnimal == "rabbit"):
            species = "rabbit and human"
            rabbitAndHumanObservations.append(newEntry)
            
        elif (previousEntryAnimal == "rabbit" and currentEntryAnimal == "coyote") or (previousEntryAnimal == "coyote" and currentEntryAnimal == "rabbit"):
            species = "rabbit and coyote"
            coyoteAndRabbitObservations.append(newEntry)
        
        elif previousEntryAnimal == currentEntryAnimal:
            species = currentEntryAnimal
            newEntry.append("duplicate spreadsheet entries of a single species")
            duplicates.append(newEntry)
            
        elif (previousEntryAnimal == "bird" and currentEntryAnimal == "human") or (previousEntryAnimal == "human" and currentEntryAnimal == "bird"):
            species = "bird and human"
            birdAndHumanObservations.append(newEntry)
            
        elif (previousEntryAnimal == "rabbit" and currentEntryAnimal == "unknown") or (previousEntryAnimal == "unknown" and currentEntryAnimal == "rabbit"):
            species = "rabbit and unknown animal(s)"
            rabbitAndUnknownObservations.append(newEntry)
            
        elif previousEntryAnimal in animalsList and currentEntryAnimal in animalsList and previousEntryAnimal != currentEntryAnimal:
            species = previousEntryAnimal + " and " + currentEntryAnimal
            miscellaneousObservations.append(newEntry)
        
        else:
            species = "other duplicates"
            otherDuplicates.append(newEntry)
        newEntry[animalIndex] = species
    
    elif previousEntryImageNumber != currentEntryImageNumber:
        actualTotalPhotos.append(currentEntry)

print("There are", len(actualTotalPhotos), "total photos")


# In[65]:


coyoteAndRabbitObservations2 = []
for index in range(len(coyoteAndRabbitObservations)):
    currentEntry = coyoteAndRabbitObservations[index]
    
    previousImageName = coyoteAndRabbitObservations[index-1][2]
    previouscurrentTime = coyoteAndRabbitObservations[index-1][-1]
    
    currentImageName = currentEntry[2]
    currentTime = currentEntry[-1]

    imageName = coyoteAndRabbitObservations[index][2]
    time = coyoteAndRabbitObservations[index][-1]
    if imageName != "IMG_1261" or time != "1:44:00":
        coyoteAndRabbitObservations2.append(currentEntry)
    elif previousImageName == currentImageName and previouscurrentTime == currentTime:
        currentEntry[2] = "IMG_1264"
        coyoteAndRabbitObservations2.append(currentEntry)


# In[66]:


vehicleAndHumanObservations = []
birdAndRabbitObservations = []
species_3 = []
birdAndRaccoonObservations = []
for index in range(len(miscellaneousObservations)):
    currentEntry = miscellaneousObservations[index]
    previousEntry = miscellaneousObservations[index - 1]
    if currentEntry[4] == "vehicle and human" or currentEntry[4] == "human and vehicle":
        if currentEntry[2] == previousEntry[2]:
            vehicleAndHumanObservations.append(currentEntry)
        elif currentEntry[2] == "RCNX2314":
            vehicleAndHumanObservations.append(currentEntry)
            
    elif currentEntry[4] == "rabbit and bird" or currentEntry[4] == "bird and rabbit":
        birdAndRabbitObservations.append(currentEntry)
        
    elif currentEntry[2] == "IMG_0819" and currentEntry[0] == "Anteater_2":
        species = "human + dog + rabbit"
        currentEntry[4] = species
        species_3.append(currentEntry)
        print(currentEntry)
    elif currentEntry[4] == "raccoon and bird" or currentEntry[4] == "bird and raccoon":
        birdAndRaccoonObservations.append(currentEntry)


# In[67]:


for entry in dogAndHumanObservations:
    if entry[:3] == ['Anteater_2', 'AT', 'IMG_0819']:
        anomalousEntry = entry
        print(anomalousEntry)
dogAndHumanObservations.remove(anomalousEntry)


# In[68]:


for entry in horseAndHumanObservations:
    print(entry)
    
print('\n')

for entry in dogAndHumanObservations:
    print(entry)

print('\n')

for entry in rabbitAndHumanObservations:
    print(entry)

print('\n')

for entry in coyoteAndRabbitObservations2:
    print(entry)

print('\n')

for entry in duplicates:
    print(entry)

print('\n')

for entry in birdAndHumanObservations:
    print(entry)

print('\n')

for entry in rabbitAndUnknownObservations:
    print(entry)

print('\n')

for entry in vehicleAndHumanObservations:
    print(entry)

print('\n')

for entry in birdAndRabbitObservations:
    print(entry)

print('\n')

for entry in species_3:
    print(entry)

print('\n')

for entry in birdAndRaccoonObservations:
    print(entry)

print('\n')

print("There are", len(horseAndHumanObservations), "photos of horses and humans")
print("There are", len(dogAndHumanObservations), "photos of dogs and humans")
print("There are", len(rabbitAndHumanObservations), "photos of rabbits and humans")
print("There are", len(coyoteAndRabbitObservations2), "photos of coyotes and rabbits")
print("There are", len(duplicates), "duplicate entries of a single species")
print("There are", len(birdAndHumanObservations), "photos of birds and humans")
print("There are", len(rabbitAndUnknownObservations), "photos of rabbits and an unknown animal")
print("There are", len(vehicleAndHumanObservations), "photos of humans and vehicles")
print("There are", len(birdAndRabbitObservations), "photos of birds and rabbits")
print("There is", len(species_3), "photo of 3 different animals")
print("There are", len(birdAndRaccoonObservations), "photos of birds and raccoons")


# In[69]:


allDuplicates = []
allDuplicates.extend(horseAndHumanObservations)
allDuplicates.extend(dogAndHumanObservations)
allDuplicates.extend(rabbitAndHumanObservations)
allDuplicates.extend(coyoteAndRabbitObservations2)
allDuplicates.extend(duplicates)
allDuplicates.extend(birdAndHumanObservations)
allDuplicates.extend(rabbitAndUnknownObservations)
allDuplicates.extend(vehicleAndHumanObservations)
allDuplicates.extend(birdAndRabbitObservations)
allDuplicates.extend(species_3)
allDuplicates.extend(birdAndRaccoonObservations)

numOfDuplicates = len(allDuplicates)
print(numOfDuplicates)
for duplicate in allDuplicates:
    print(duplicate)


# In[70]:


totalNumOfPhotos = len(actualTotalPhotos)
print("The total number of photos in the spreadsheet are", totalNumOfPhotos)
singleSpeciesPhotosNum = totalNumOfPhotos - numOfDuplicates
print("There are {} photos that represent a single species".format(singleSpeciesPhotosNum))


# Doing some final formatting before publishing the data as a new csv. Each image is given a new name that contains the original image number, the camera location, and the date and time of the original image. The species of any duplicates will be changed. A newline character will be added at the end of each entry if there had been no newline character yet, so that the data can be exported to a csv file and when opened in Google Sheets or Excel, each entry appears as a separate entry.

# In[71]:


speciesIndex = 4
counter = 0
outputList = []
for entry in actualTotalPhotos:
    newEntry = entry
    for index in range(len(newEntry)):
        if type(newEntry[index]) != str:
            newEntry[index] = str(newEntry[index])
    LocCode = newEntry[1]
    Date = newEntry[6]
    Time = newEntry[7]
    datetime = newEntry[8]
    reformattedDate = datetime.split(" ")[0]
    oldImageNumber = newEntry[2]
    species = newEntry[4]
    newImageNumber = "-".join([oldImageNumber, LocCode, reformattedDate, species])
    newEntry[2] = newImageNumber
    counter += 1
    lineEnding = str(counter)
    for duplicate in allDuplicates:
        if (LocCode in duplicate) and (oldImageNumber in duplicate) and (Date in duplicate) and (Time in duplicate):
            newEntry = duplicate
            for index in range(len(newEntry)):
                if type(newEntry[index]) != str:
                    newEntry[index] = str(newEntry[index])
            species = newEntry[4]
            Date = newEntry[6]
            datetime = newEntry[8]
            reformattedDate = datetime.split(" ")[0]
            newImageNumber = "-".join([oldImageNumber, LocCode, reformattedDate, species])
            newEntry[2] = newImageNumber
            break
            
    while len(newEntry) < 10:
        newEntry.append("")
    if len(newEntry) == 10:
        newEntry.append(lineEnding)
    elif len(newEntry) == 11:
        newEntry[-1] = lineEnding
        
    outputList.append(newEntry)

for entry in outputList:
    print(entry)


# Now the processed data will be exported as a new csv file. The csv file is imported as a pandas dataframe to make it easier to count the species in each camera. The labels will be re-processed a bit more: photos that contain multiple species that are not dogs and humans or horses and humans will be combined into a new category called "multiple wild animals". Any photos containing a human and another wild animal will be combined into a new category called "animal and human". In the analysis above, the original author of this notebook found a photo that contains humans, dogs, and rabbits. This photo will also be relabeled with the latter new category

# In[72]:


headerList = photoEntries.columns.tolist()
headerList.append("Counter")
csvName = "re-labeled animal photos.csv"
outputDF = pd.DataFrame(outputList, columns = headerList)
outputDF.to_csv(csvName, index = False)


# ### Section 2

# In[73]:


relabeled_df = pd.read_csv("re-labeled animal photos.csv")
relabeled_df


# In[74]:


wildAnimalBool = relabeled_df["Species"].isin(["bird and raccoon", "rabbit and bird", "rabbit and coyote", "rabbit and unknown animal(s)", "human + dog + rabbit"])
relabeled_df.loc[wildAnimalBool, "Species"] = "wild animals"

animalAndHumanBool = relabeled_df["Species"].isin(["human + dog + rabbit", "rabbit and human", "bird and human"])
relabeled_df.loc[animalAndHumanBool, "Species"] = "animal and human"

relabeled_df["Species"] = relabeled_df["Species"].astype("category")
relabeled_df["Species"].cat.categories


# In[75]:


humans = relabeled_df[relabeled_df["Species"] == "human"]["Species"].count()
print(humans)
print(type(humans))


# In[76]:


def speciesDistribution(camera: str) -> "numpy array of species distribution, total number of photos":
    """Produces a numpy array of species distribution of a particular camera"""
    cameraPhotos = relabeled_df[relabeled_df["Location"] == camera]
    if camera == "Anteater":
        anteaterBool = relabeled_df["Location"].isin(["Anteater_1", "Anteater_2"])
        cameraPhotos = relabeled_df[anteaterBool]
    elif camera == "All":
        cameraPhotos = relabeled_df
    speciesSeries = cameraPhotos["Species"]
    
    totalPhotos = speciesSeries.count()
    
    humans = speciesSeries[speciesSeries == "human"].count()
    dogs = speciesSeries[speciesSeries == "domestic dog"].count()
    coyotes = speciesSeries[speciesSeries == "coyote"].count()
    rabbits = speciesSeries[speciesSeries == "rabbit"].count()
    unknowns = speciesSeries[speciesSeries == "unknown"].count()
    birds = speciesSeries[speciesSeries == "bird"].count()
    raccoons = speciesSeries[speciesSeries == "raccoon"].count()
    vehicles = speciesSeries[speciesSeries == "vehicle"].count()
    insects = speciesSeries[speciesSeries == "insect"].count()
    squirrels = speciesSeries[speciesSeries == "squirrel"].count()
    rats = speciesSeries[speciesSeries == "rat"].count()
    horses = speciesSeries[speciesSeries == "horse"].count()
    opossums = speciesSeries[speciesSeries == "opossum"].count()
    mice = speciesSeries[speciesSeries == "mouse"].count()
    lizards = speciesSeries[speciesSeries == "lizard"].count()
    snakes = speciesSeries[speciesSeries == "snake"].count()
    dogAndHuman = speciesSeries[speciesSeries == "dog and human"].count()
    horseAndHuman = speciesSeries[speciesSeries == "horse and human"].count()
    animalAndHuman = speciesSeries[speciesSeries == "animal and human"].count()
    vehicleAndHuman = speciesSeries[speciesSeries == "vehicle and human"].count()
    wildAnimals = speciesSeries[speciesSeries == "wild animals"].count()
    
    countsList = [humans, dogs, coyotes, rabbits, unknowns, birds, raccoons, vehicles, insects, squirrels, rats, horses, opossums, mice, lizards, snakes, dogAndHuman, horseAndHuman, animalAndHuman, vehicleAndHuman, wildAnimals]
    np.set_printoptions(precision = 4, suppress = True)
    speciesCounts = np.array(countsList)
    speciesDistribution = 100*speciesCounts/totalPhotos
    results = np.stack([speciesCounts, speciesDistribution], axis = 0)
    return totalPhotos, results


# In[77]:


Anteater1_total, Anteater1_results = speciesDistribution("Anteater_1")
print("Anteater_1")
print(Anteater1_total)
print(Anteater1_results)
print('\n')

Anteater2_total, Anteater2_results = speciesDistribution("Anteater_2")
print("Anteater_2")
print(Anteater2_total)
print(Anteater2_results)
print('\n')

Anteater_total, Anteater_results = speciesDistribution("Anteater")
print("Anteater - both camera angles")
print(Anteater_total)
print(Anteater_results)
print('\n')

BonitaCanyonBridge_total, BonitaCanyonBridge_results = speciesDistribution("BonitaCanyonBridge")
print("Bonita Canyon Bridge")
print(BonitaCanyonBridge_total)
print(BonitaCanyonBridge_results)
print("\n")

ChineseChurchCulvert_total, ChineseChurchCulvert_results = speciesDistribution("ChineseChurchCulvert")
print("Chinese Church Culvert")
print(ChineseChurchCulvert_total)
print(ChineseChurchCulvert_results)
print("\n")

ConcordiaCulvert_total, ConcordiaCulvert_results = speciesDistribution("ConcordiaCulvert")
print("Convordia culvert")
print(ConcordiaCulvert_total)
print(ConcordiaCulvert_results)
print("\n")

Coyotetrail_total, Coyotetrail_results = speciesDistribution("Coyotetrail")
print("Coyote Trail")
print(Coyotetrail_total)
print(Coyotetrail_results)
print("\n")

Culver_Culvert_total, Culver_Culvert_results = speciesDistribution("Culver_Culvert")
print("Culver culvert")
print(Culver_Culvert_total)
print(Culver_Culvert_results)
print("\n")

Ecopreserve_culvert_total, Ecopreserve_culvert_results = speciesDistribution("Ecopreserve_culvert")
print("Ecopreserve culvert")
print(Ecopreserve_culvert_total)
print(Ecopreserve_culvert_results)
print("\n")

MacArthurBridge_total, MacArthurBridge_results = speciesDistribution("MacArthurBridge")
print("MacArthur Bridge")
print(MacArthurBridge_total)
print(MacArthurBridge_results)
print("\n")

Historical_MarshTrail_total, Historical_MarshTrail_results = speciesDistribution("Historical_MarshTrail")
print("Historical Marsh Trail")
print(Historical_MarshTrail_total)
print(Historical_MarshTrail_results)
print("\n")

ResearchPark_Culvert_total, ResearchPark_Culvert_results = speciesDistribution("ResearchPark_Culvert")
print("Research Park culvert")
print(ResearchPark_Culvert_total)
print(ResearchPark_Culvert_results)
print("\n")

SDC_Hist_1_total, SDC_Hist_1_results = speciesDistribution("SDC_Hist_1")
print("SDC Historical 1")
print(SDC_Hist_1_total)
print(SDC_Hist_1_results)
print("\n")

allPhotos_total, allPhotos_results = speciesDistribution("All")
print("All photos")
print(allPhotos_total)
print(allPhotos_results)
print('\n')


# ### Section 3

# In[78]:


multipleAnimalsLabels = ["D + H", "H + H", "A + H", "V + H", "wild animals"]
labels = animalsList + multipleAnimalsLabels
print(labels)
x = np.arange(len(labels))
print(len(labels))


# In[79]:


def plotSpeciesDistribution(resultsArray: "numpy array of results generated above", total: int, cameraLocation: str):
    """Plots bar graphs of the proportion of species observed from each camera"""
    figure = py.figure(figsize = (25, 15))
    numberOfPhotosPlot = figure.add_subplot(2, 1, 1)
    speciesFrequencyPlot = figure.add_subplot(2, 1, 2)
    width = 0.6
    
    numberOfPhotosPlot.set_title("The number of photos of each species taken at " + cameraLocation + " - {} photos".format(total))
    rects1 = numberOfPhotosPlot.bar(x, resultsArray[0, :], width, label = "number of photos")
    numberOfPhotosPlot.set_xticks(x)
    numberOfPhotosPlot.set_xticklabels(labels)
    numberOfPhotosPlot.set_xlabel("Species in photo")
    numberOfPhotosPlot.set_ylabel("Number of photos taken for each category")
    for rectangle in rects1:
        height = int(rectangle.get_height())
        x_coord = rectangle.get_x() + (width/2)
        numberOfPhotosPlot.annotate(s = str(height), xy = (x_coord, height), xytext = (0, 3), textcoords = "offset points", ha = "center")
    
    speciesFrequencyPlot.set_title("The frequency of photos of each species taken at " + cameraLocation)
    rects2 = speciesFrequencyPlot.bar(x, resultsArray[1, :], width, label = "frequency")
    speciesFrequencyPlot.set_xticks(x)
    speciesFrequencyPlot.set_xticklabels(labels)
    speciesFrequencyPlot.set_xlabel("Species in photo")
    speciesFrequencyPlot.set_ylabel("Frequency of photos taken for each category (%)")
    speciesFrequencyPlot.set_ylim([0, 100])
    for rectangle in rects2:
        height = rectangle.get_height()
        x_coord = rectangle.get_x() + (width/2)
        speciesFrequencyPlot.annotate(s = "{:.2f}%".format(height), xy = (x_coord, height), xytext = (0, 3), textcoords = "offset points", ha = "center")
    
    fileName = cameraLocation + ".jpg"
    figure.savefig(fileName)
    return


# In[80]:


plotSpeciesDistribution(Anteater1_results, Anteater1_total, "Anteater Trail - 1st camera angle")


# In[81]:


plotSpeciesDistribution(Anteater2_results, Anteater2_total, "Anteater Trail - 2nd camera angle")


# In[82]:


plotSpeciesDistribution(Anteater_results, Anteater_total, "Anteater Trail - both camera angles")


# In[83]:


plotSpeciesDistribution(BonitaCanyonBridge_results, BonitaCanyonBridge_total, "Bonita Canyon Bridge")


# In[84]:


plotSpeciesDistribution(ChineseChurchCulvert_results, ChineseChurchCulvert_total, "Chinese Church culvert")


# In[85]:


plotSpeciesDistribution(Culver_Culvert_results, Culver_Culvert_total, "Culver culvert")


# In[86]:


plotSpeciesDistribution(Ecopreserve_culvert_results, Ecopreserve_culvert_total, "Ecopreserve culvert")


# In[87]:


plotSpeciesDistribution(Historical_MarshTrail_results, Historical_MarshTrail_total, "Historical Marsh Trail")


# In[88]:


plotSpeciesDistribution(MacArthurBridge_results, MacArthurBridge_total, "MacArthur Bridge")


# In[89]:


plotSpeciesDistribution(ResearchPark_Culvert_results, ResearchPark_Culvert_total, "Research Park culvert")


# In[90]:


plotSpeciesDistribution(SDC_Hist_1_results, SDC_Hist_1_total, "SDC Hist 1")


# In[91]:


plotSpeciesDistribution(ConcordiaCulvert_results, ConcordiaCulvert_total, "Concordia culvert")


# In[92]:


plotSpeciesDistribution(allPhotos_results, allPhotos_total, "every camera")


# In[93]:


plotSpeciesDistribution(Coyotetrail_results, Coyotetrail_total, "Coyote Trail")


# ### Section 4

# In[94]:


print(cameras)
totals = [Anteater_total, BonitaCanyonBridge_total, ChineseChurchCulvert_total, ConcordiaCulvert_total, Coyotetrail_total, Culver_Culvert_total, Ecopreserve_culvert_total, Historical_MarshTrail_total, MacArthurBridge_total, ResearchPark_Culvert_total, SDC_Hist_1_total]


# In[95]:


cameras2 = ["Anteater camera"]
cameras2.extend(cameras[2:])
rankingDataFrame = pd.DataFrame({"Cameras": cameras2,
                                "Total photos": totals})
sortedDataFrame = rankingDataFrame.sort_values(by = "Total photos", ascending = False)
sortedDataFrame.to_csv("Total photos from each camera.csv", index = False)

