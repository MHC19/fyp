import sounddevice as sd
from datetime import datetime
import numpy as np

def second():
    print("2nd callback\n\n--------\n")


def callback(indata, frames, time, status):
    global array_meanA
    global n

    volume_norm = np.linalg.norm(indata) * 10

    # Replace end of array with volume_norm
    array_meanA[n] = int(volume_norm)

    # Shift elements left by 1
    # Note: Final element will be the same as previous element
    for h in range(n):
        array_meanA[h] = array_meanA[(h + 1)]

    meanA = 0

    # Sum values in array_meanA
    for h in range(n):
        meanA = array_meanA[h] + meanA

    meanA = meanA / n
    print("1st callback\n*******\n")
    second()


n = 30
# Adding 0.0 for shifting
array_meanA = [0.0]
# Initialize array with n values of 0.0
for h in range(n):
    array_meanA.append(0.0)

start_time = datetime.now()

stream = sd.InputStream(callback=callback, blocksize=0)
print("Starting stream!\n\n")
stream.start()
stream_start = True

while stream_start:
    current_time = datetime.now()
    timer = (current_time - start_time).total_seconds()

    if timer >= 3:
        print("Ran for 3 seconds")
        stream_start = False
        stream.stop()
        print("Timer: %s" % timer)

print("Stopping stream!")
# stream.stop()