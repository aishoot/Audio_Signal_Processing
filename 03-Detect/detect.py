import os
import wave
import shutil

problemCounter = 0
allAudioLength = 0
filePath = os.getcwd()
wavFileList = os.listdir(filePath)

problemFolder = os.path.join(filePath, "problem")
if not os.path.exists(problemFolder):
    os.makedirs(problemFolder)

for waveFile in wavFileList:
    if ".wav" in waveFile:
        f = wave.open(waveFile, "rb")
        nchannels, _, framerate, nframes = f.getparams()[:4]

        if nchannels!=2 or framerate!=44100:
            print("%s: not 2 channels or 44.1KHz."%waveFile)
            shutil.move(waveFile, problemFolder)
            problemCounter += 1
        else:
            length = nframes / framerate  #second
            allAudioLength += length

    elif waveFile != "detect.py":
        print("%s: not a .wav file!"%waveFile)
        shutil.move(waveFile, problemFolder)
        problemCounter += 1

if problemCounter == 0:
    print("All audio files have no problem.")
else:
    print("%s files have problems."%problemCounter)


hour = allAudioLength // 3600
min = allAudioLength % 3600 // 60
sec = allAudioLength % 3600 % 60
print("All right audio length: %sh %smin %ss."%(round(hour), round(min), round(sec)))