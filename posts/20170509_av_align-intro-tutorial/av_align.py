import numpy as np
import wave
import struct
from random import randint
import math
import pyfftw
import timeit
import glob
import sys
import os
import re
import itertools
import difflib
import subprocess
import argparse
import json
from distutils import spawn

g_sampleRate = 8000
g_sampleRateHq = 48000

parser = argparse.ArgumentParser(description='.', formatter_class=argparse.RawDescriptionHelpFormatter)

#parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
parser.add_argument('-t', '--tmp', dest='tmpDir', help='Temporary directory, default is <inputDir>/tmp', default = '')
parser.add_argument('-d', '--indir', dest='inputDir', help='Input directory, default=\'.\'', default = '.')
parser.add_argument('-f', '--ffmpegpath', dest='ffmpegPath', help='Path to ffmpeg executable (including exe), default=\'ffmpeg\'', default = '')
parser.add_argument('-v', '--verbose', dest='verbose', help='Turn on piping all ffmpeg output to the std streams (otherwise it is hidden), defaults to False', action="store_true")
#parser.add_argument('-r', '--transfmt', dest='transcriptFormat', help='Transcript format override option. Use if there are more than one in the fo, default=\'\'', default = '')

args = parser.parse_args()

g_baseDir = args.inputDir;
g_tmpDir = os.path.join(g_baseDir, "tmp");

if args.tmpDir != '':
    g_tmpDir = args.tmpDir

g_outDir = os.path.join(g_baseDir, "output");


#g_ffmpegExe = "c:\\tools\\ffmpeg\\bin\\ffmpeg"
g_ffmpegExe = spawn.find_executable(os.path.join(args.ffmpegPath, "ffmpeg"))
g_ffprobeExe = spawn.find_executable(os.path.join(args.ffmpegPath, "ffprobe"))

if g_ffmpegExe == None or g_ffprobeExe == None:
    print("Could not find ffmpeg! Please ensure full path is given using '-f' or that the bin directory is on the system path!");
    print("  ffmpeg path: %s"%g_ffmpegExe)
    print("  ffprobe path: %s"%g_ffprobeExe)
    sys.exit(1)

g_verboseOutput = args.verbose

if g_verboseOutput:
    print(g_baseDir)
    print(g_tmpDir)
    print(g_ffmpegExe)


# Create temp directory if not there
if not os.path.exists(g_tmpDir):
    os.makedirs(g_tmpDir)

if not os.path.exists(g_outDir):
    os.makedirs(g_outDir)

def nextPot(v):
    return int(math.pow(2, int(math.ceil(math.log(float(v), 2)) + 0.5)) + 0.5)

def wavLoad(fname):
    wav = wave.open (fname, "r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
    frames = wav.readframes (nframes * nchannels)
    out = struct.unpack_from ("%dh" % nframes * nchannels, frames)

    if g_verboseOutput:
        print("%0.2f min"%(nframes / float(framerate * 60.0)))
        print("Sample Rate: %0.1f kHz"%(framerate/1000.0))

    # Convert 2 channles to numpy arrays
    if nchannels == 2:
        out = out[0::2]

    out = np.array(out, np.float32)
    return out / 32768.0


def wavStore(fname, data, sampleRate):
    with wave.open(fname, "wb") as wf:
        wf.setnchannels(1)
        wf.setframerate(sampleRate)
        wf.setsampwidth(2)
        tmp = np.array(data * 32768.0, np.int16)
        wf.writeframes(tmp)

# 2. Uses numpy's built in fft, this is a lot slower.
def findOffset(sound1, sound2):
    N = max(len(sound1), len(sound2))
    # Note: this pads with zeroes up to next power of two, to ensure good fft alg perf. However, we should really just 
    # ensure the number is factorizable into primes in range 1-9 or some such, whatever the library likes...)
    #print(str(N))
    #N = nextPot(N)
    #print(str(N))
    MN = 2 * N - 1

    s1p = np.append(np.zeros(N - 1), sound1)
    s1p = np.append(s1p, np.zeros(MN - len(s1p)))
    s2p = np.append(sound2, np.zeros(MN - len(sound2)))

    fs1 = np.fft.rfft(s1p)
    fs2 = np.fft.rfft(s2p) 

    scale = 1.0 / float(MN)
    fcorr = fs1 * np.conj(fs2) * scale

    corr = np.fft.irfft(fcorr)
    return np.argmax(corr) - N;


# 2. 
def findOffsetFftw(sound1, sound2):
    N = max(len(sound1), len(sound2))
    #print(str(N))
    #N = nextPot(N)
    #print(str(N))
    MN = 2 * N - 1

    s1p = pyfftw.empty_aligned(MN, dtype='float32')
    s1p[:] = 0.0
    s2p = pyfftw.empty_aligned(MN, dtype='float32')
    s2p[:] = 0.0
    
    s1p[N-1:N-1+len(sound1)] = sound1
    s2p[0:len(sound2)] = sound2

    fs1 = pyfftw.interfaces.numpy_fft.rfft(s1p, planner_effort='FFTW_ESTIMATE')
    fs2 = pyfftw.interfaces.numpy_fft.rfft(s2p, planner_effort='FFTW_ESTIMATE') 

    scale = 1.0 / float(MN)
    fcorr = fs1 * np.conj(fs2) * scale

    corr = pyfftw.interfaces.numpy_fft.irfft(fcorr, planner_effort='FFTW_ESTIMATE')
    return np.argmax(corr) - N;



def execProc(procArgs, progressPattern):
    global g_verboseOutput

    if g_verboseOutput:
        subprocess.call(procArgs)
        return

    procArgs.append("-y")
    process = subprocess.Popen(procArgs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    count=0    
    tmpStr = ""
    while process.poll() == None:
        buff = process.stdout.read(1)

        tmpStr += buff.decode()

        if g_verboseOutput:
            sys.stdout.write(buff.decode())#, end = '', flush = True)
            sys.stdout.flush()

        tmpStr.replace('\r', '\n')

        #if tmpStr.find('frame') > -1:
        #    tmpStr = tmpStr[tmpStr.find('frame'):]

        result = re.search(progressPattern, tmpStr)
        if result != None and 'progress' in result.groupdict():
            sys.stdout.write("\rframe=%s"%result.groupdict()['progress'])#, end = '', flush = True)
            sys.stdout.flush()
            tmpStr = ""

    process.wait()


def findFirstFileByExt(setOfAllFiles, exts):
    for f in setOfAllFiles:
        name, ext = os.path.splitext(f)
        if ("*" + ext.lower()) in exts:
            return f
    return ""
    
def condLog(cond, text):
    if cond:
        sys.stdout.write(text)
        sys.stdout.flush()


allFilesInDir = set(glob.glob(os.path.join(g_baseDir, "*.*")))

movieName = findFirstFileByExt(allFilesInDir, ["*.mp4", "*.mov"])#list(movieList)[0]
condLog(g_verboseOutput, "Movie file name:'" + movieName + "'\n");
audioName = findFirstFileByExt(allFilesInDir, ["*.wav", "*.mp3"])#list(movieList)[0]
condLog(g_verboseOutput, "Audio file name:'" + audioName + "'\n");
transcriptFileName = findFirstFileByExt(allFilesInDir, ["*.cha", "*.eaf"])#list(movieList)[0]
condLog(g_verboseOutput, "Transcript file name:'" + transcriptFileName + "'\n");

sourceList = [movieName, audioName]
# TODO: warning if more than one of each type in folders
#if len(movieList) > 1:
#    if g_verboseOutput:
#        sys.stdout.write("More than one video file, selecting the first one")


# Extract audio tracks:
def getWavName(movieName):
    dir,name = os.path.split(movieName)
    #outName, ext = os.path.splitext(name)
    return os.path.join(g_tmpDir, name.replace(".", "_") + "_8k.wav")

def getHqWavName(movieName):
    dir,name = os.path.split(movieName)
    #outName, ext = os.path.splitext(name)
    return os.path.join(g_tmpDir, name.replace(".", "_") + "_hq.wav")


def adjustTranscript(fileName, outFileName, offsetInMs):
    isChaTrans = os.path.splitext(fileName)[1] == ".cha"
    transcript = []
    with open(fileName, 'r') as transcriptFile:
        transcript = transcriptFile.readlines()    
    with open(outFileName, 'w') as outTranscriptFile:
        for line in transcript:
            if isChaTrans:
                if not line.startswith("@"):
                    line = re.sub(r'([0-9]+)_([0-9]+)', lambda m: "%d_%d"%(int(m.group(1)) + offsetInMs, int(m.group(2)) + offsetInMs), line)
            else:
                line = re.sub(r'(<TIME_SLOT\s+TIME_SLOT_ID="[^"]+"\s+TIME_VALUE=)"([0-9]+)"', lambda m: '%s"%d"'%(m.group(1), int(m.group(2)) + offsetInMs), line)
            outTranscriptFile.write(line);                                


# used for testing the adjustment code
#outTranscriptName = os.path.join(g_outDir, "ext_" + os.path.basename(transcriptFileName))
#adjustTranscript(transcriptFileName, outTranscriptName, int(1000.0))

print("\rExtracting Audio:");

g_vidWidth = 0
g_vidHeight = 0
g_sampleAspectRatio = [1,1]

for m in sourceList:
    print(m)
    #p = subprocess.Popen([g_ffprobeExe, "-v", "error", "-show_entries", "stream=width,height", "-select_streams", "v:0", "-of", "json", m], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p = subprocess.Popen([g_ffprobeExe, "-v", "error", "-show_streams", "-select_streams", "v:0", "-of", "json", m], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tt,_ = p.communicate()
    if g_verboseOutput:
        print(tt.decode())
    jj = json.loads(tt.decode())
    print(jj)
    if len(jj["streams"]) > 0:
        g_vidWidth = max(g_vidWidth, jj["streams"][0]["width"]);    
        g_vidHeight = max(g_vidHeight, jj["streams"][0]["height"]);    
        sarStr = jj["streams"][0]["sample_aspect_ratio"]
        if sarStr != "1:1":
            g_sampleAspectRatio = [int(s) for s in sarStr.split(":")]

    print('  %s -> %s'%(m, getWavName(m)));
    execProc([g_ffmpegExe, "-i", m, "-af", "aformat=channel_layouts=mono,aresample=%d"%(int(g_sampleRate)), "-acodec", "pcm_s16le", "-ac", "1", getWavName(m)], "time=\s*(?P<progress>\S+)\s")
    #print('              \r', end = '')

# Now lets find offsets between the movie & audio file
print("Finding offsets:       ")
sounds = {m : wavLoad(getWavName(m)) for m in sourceList}
offset = findOffsetFftw(sounds[movieName], sounds[audioName])

print("  %s -> %s = %d = %6.4fs"%(movieName, audioName, offset, float(offset) / float(g_sampleRate)))

# extend one or the other
if offset < 0:
    #extendMovie(movieName, -offset)
    resName = os.path.join(g_outDir, "ext_" + os.path.basename(movieName))
    print("Extending the movie by %6.4fs -> '%s'"%(float(-offset) / float(g_sampleRate), resName))
    argList = [g_ffmpegExe]
    offsetSecs = float(-offset) / float(g_sampleRate)
    #argList.extend(["-itsoffset", str(offsetSecs), "-i", movieName, "extended.mov"])
	 # This is the original line of code for adding grey frames:
    argList.extend(["-f", "lavfi",  "-i", "color=c=gray:s=%dx%d:r=25:d=%f,setsar=%d:%d"%(g_vidWidth, g_vidHeight, offsetSecs, g_sampleAspectRatio[0], g_sampleAspectRatio[1]),  "-f", "lavfi", "-i", "aevalsrc=0:d=%f"%offsetSecs,  "-i", movieName, "-filter_complex", "[0:v] [1:a] [2:v] [2:a] concat=n=2:v=1:a=1 [v] [a]", "-map", "[v]", "-map", "[a]", "-strict", "-2", resName])
    execProc(argList, 'frame=\s*(?P<progress>\d+)\s')
elif offset > 0:
    #extendAudio(audioName, offset)
    resName = os.path.join(g_outDir, "ext_" + os.path.basename(audioName))
    offsetSecs = float(offset) / float(g_sampleRate)
    print("Extending the audio file by %6.4fs -> '%s'"%(offsetSecs, resName))
    argList = [g_ffmpegExe]
    argList.extend(["-f", "lavfi", "-i", "aevalsrc=0:d=%f"%offsetSecs, "-i", audioName, "-filter_complex", "[0:0] [1:0] concat=n=2:v=0:a=1", resName])
    execProc(argList, 'frame=\s*(?P<progress>\d+)\s')
    # Allow running the script when there is no transcript
    if len(transcriptFileName) > 0:
        # If the audio file was padded, then we also must update the offsets in the transcript:
        outTranscriptName = os.path.join(g_outDir, "ext_" + os.path.basename(transcriptFileName))
        print("adjusting the transcript by %dms -> '%s'"%(int(offsetSecs * 1000.0), outTranscriptName))
        adjustTranscript(transcriptFileName, outTranscriptName, int(offsetSecs * 1000.0))
    else:
        print("No transcript file to adjust found.")

