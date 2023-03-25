import wave
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "received_audio.wav"
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Recording...")

# rec audio data
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("Finished recording!")

# stop rec
stream.stop_stream()
stream.close()
p.terminate()

with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wav_file:
    wav_file.setnchannels(CHANNELS)
    wav_file.setsampwidth(p.get_sample_size(FORMAT))
    wav_file.setframerate(RATE)
    wav_file.writeframes(b''.join(frames))

print("Saved as", WAVE_OUTPUT_FILENAME)
print("Encode starting.... ")

with wave.open("received_audio.wav", "rb") as wav_file:
    channels = wav_file.getnchannels()
    sample_width = wav_file.getsampwidth()
    frame_rate = wav_file.getframerate()
    num_frames = wav_file.getnframes()

    wav_data = wav_file.readframes(num_frames)
    # convert the WAV data to a list of bytes
    wav_bytes = [wav_data[i:i + 2] for i in range(0, len(wav_data), 2)]

    n = 0
    while 2 ** n <= len(wav_bytes):
        n += 1

    encoded_data = []
    wav_bytes_copy = wav_bytes.copy()  # make a copy of the list of bytes
    for i in range(len(wav_bytes)):
        # check if the bit is a parity bit
        if i + 1 in [2 ** j - 1 for j in range(n)]:
            encoded_data.append(0)
        else:
            if wav_bytes_copy:
                encoded_data.append(int.from_bytes(wav_bytes_copy.pop(0), byteorder='big'))

    for i in range(n):
        parity = 0
        for j in range(2 ** i - 1, len(encoded_data), 2 ** (i + 1)):
            for k in range(2 ** i):
                if j + k < len(encoded_data):
                    parity ^= encoded_data[j + k]
        encoded_data[2 ** i - 1] = parity
    encoded_data_bytes = bytes([x % 256 for x in encoded_data])

with open("audio.bin", "wb") as bin_file:
    bin_file.write(encoded_data_bytes)
print("Successful")
