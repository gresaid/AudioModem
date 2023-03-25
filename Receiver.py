import wave
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
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
    # Get parameters
    num_channels = wav_file.getnchannels()
    sample_width = wav_file.getsampwidth()
    frame_rate = wav_file.getframerate()
    num_frames = wav_file.getnframes()

    audio_data = wav_file.readframes(num_frames)

binary_data = bytearray(audio_data)

with open("audio.bin", "wb") as bin_file:
    bin_file.write(binary_data)
    print("Successful")
