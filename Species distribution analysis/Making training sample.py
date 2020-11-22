#!/usr/bin/env python
# coding: utf-8

# # Making training sample
# ## Author(s): Brian Nhan Thien Chung (UCI NATURE research technician)
# ### Created on: Wednesday September 9, 2020 by Brian Nhan Thien Chung
# ### Last edited on: Sunday September 13, 2020 by Brian Nhan Thien Chung
# The purpose of this notebook is to try to make a training sample based on the species distribution of each camera. A proof of concept is conducted using animal photos from Anteater Trail. After this proof of concept is shown to be successful, a function is written to automate this process. This function exports csv files of animal photos that are part of the training sample of a camera.

# In[14]:


import pandas as pd


# In[1]:


get_ipython().run_line_magic('autosave', '15')


# In[16]:


relabeledPhotos = pd.read_csv("re-labeled animal photos.csv")
relabeledPhotos.head()


# In[17]:


species = relabeledPhotos.groupby("Species")["Species"].count()
species.index


# In[18]:


wildAnimalBool = relabeledPhotos["Species"].isin(["bird and raccoon", "rabbit and bird", "rabbit and coyote", "rabbit and unknown animal(s)", "human + dog + rabbit"])
relabeledPhotos.loc[wildAnimalBool, "Species"] = "wild animals"

animalAndHumanBool = relabeledPhotos["Species"].isin(["human + dog + rabbit", "rabbit and human", "bird and human"])
relabeledPhotos.loc[animalAndHumanBool, "Species"] = "animal and human"

relabeledPhotos = relabeledPhotos[relabeledPhotos["Species"] != "unknown"]

species = relabeledPhotos.groupby("Species")["Species"].count()
species.index


# In[19]:


locCodeCounts = relabeledPhotos.groupby("LocCode")["LocCode"].count()
locCodeCounts


# ## Section 1: proof of concept

# In[20]:


anteater = relabeledPhotos[relabeledPhotos["LocCode"] == "AT"]

anteater.head()


# In[21]:


anteaterSpeciesCounts = anteater.groupby("Species")["Species"].count()
anteaterSpeciesIndex = anteaterSpeciesCounts.index
print(anteaterSpeciesIndex)
for index in anteaterSpeciesIndex:
    if "human" in index:
        print(index)


# In[22]:


print(anteaterSpeciesCounts)
print(anteaterSpeciesCounts["bird"])
anteaterTotal = anteater["Species"].count()
print(anteaterTotal)
print('\n')
anteaterSpeciesProportions = 100*anteaterSpeciesCounts/anteaterTotal
print(anteaterSpeciesProportions)


# In[23]:


sampleSize = int(0.10*anteaterTotal)
anteaterSample = anteater.sample(sampleSize)
print(anteaterSample)


# In[24]:


anteaterSampleSpeciesCounts = anteaterSample.groupby("Species")["Species"].count()
print(anteaterSampleSpeciesCounts)
anteaterSampleTotal = anteaterSample["Species"].count()
print(anteaterSampleTotal)
print('\n')
anteaterSampleSpeciesProportions = 100*anteaterSampleSpeciesCounts/anteaterSampleTotal
print(anteaterSpeciesProportions)


# ## Section 2: Making training samples

# In[32]:


def animalTrainingSample(cameraCode: "2 letter camera code", cameraName: str, trainingFraction: float) -> None:
    """Makes a csv file of photos from a camera to be included in a training set"""
    cameraPhotos = relabeledPhotos[relabeledPhotos["LocCode"] == cameraCode]
    cameraSpeciesCounts = cameraPhotos.groupby("Species")["Species"].count()
    cameraTotal = cameraPhotos["Species"].count()
    print("Species proportions for {0} out of {1} photos:".format(cameraName, cameraTotal))
    print(100*cameraSpeciesCounts/cameraTotal)
    print('\n')
    
    trainingSet = cameraPhotos.sample(frac = trainingFraction)
    trainingSetSpeciesCounts = trainingSet.groupby("Species")["Species"].count()
    trainingSetTotal = trainingSet["Species"].count()
    print("Species counts for the training set of {0} out of {1} training photos:".format(cameraName, trainingSetTotal))
    print(100*trainingSetSpeciesCounts/trainingSetTotal)
    print('\n')
    print('\n')
    title = "{} training photos - animals only.csv".format(cameraName)
    trainingSet.to_csv(title, index = False)
    return


# In[33]:


# This is the fraction of animal photos that will be included in the training sample.
# Please change this fraction as necessary
trainingFractionPerCamera = 0.10

animalTrainingSample("RP", "Research Park", trainingFractionPerCamera)
animalTrainingSample("MT", "Historical Marsh Trail", trainingFractionPerCamera)
animalTrainingSample("MB", "MacArthur Bridge", trainingFractionPerCamera)
animalTrainingSample("CB", "Culver culvert", trainingFractionPerCamera)
animalTrainingSample("CH", "Concordia culvert", trainingFractionPerCamera)
animalTrainingSample("BC", "Bonita Canyon Bridge", trainingFractionPerCamera)

