import os
import wave
import shutil
import pandas as pd

filePath = os.path.join(os.getcwd(), "wav")
wavFileList = os.listdir(filePath)
name = []
min_sec = []
counter = 1
allWavLength = 0  #All audio time length

problemFolder = os.path.join(filePath, "problem")
renamedFolder = os.path.join(filePath, "renamed")
if not os.path.exists(problemFolder):
    os.makedirs(problemFolder)
if not os.path.exists(renamedFolder):
    os.makedirs(renamedFolder)

for waveFile in wavFileList:
    if not waveFile.startswith('.'):
        address = os.path.join(filePath, waveFile)
        f = wave.open(address, "rb")
        nchannels, _, framerate, nframes = f.getparams()[:4]

        if nchannels!=2 or framerate!=44100:
            print("%s: not 2 channels or 44.1KHz."%waveFile)
            shutil.move(address, os.path.join(filePath, "problem"))
        else:
            length = nframes / framerate  #second
            allWavLength += length
            min = length // 60
            sec = round(length % 60)

            nameStr = "6_%s.wav"%(counter)
            name.append(nameStr)
            min_sec.append("%s:%s"%(int(min), sec))
            os.rename(address, os.path.join(filePath, "renamed/%s.wav"%counter))

            print("name:"%name, "min_sec"%min_sec)
            counter += 1
    else:
        print("It is a hidden file")

print("All audio time length is: %sh%smin"%(allWavLength//3600, allWavLength%3600//60))
dataframe = pd.DataFrame({'min_sec':min_sec, 'name':name})
dataframe.to_csv("result.csv", index=False)