import wave

print("Open file...")
with open("audio.bin", "rb") as bin_file:
    binary_data = bin_file.read()

audio_data = bytes(binary_data)

num_channels = 1  # Mono
sample_width = 2  # 16-bit
frame_rate = 44100  # sample rate
num_frames = len(audio_data) // (num_channels * sample_width)
with wave.open("audio.wav", "wb") as wav_file:
    wav_file.setnchannels(num_channels)
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(frame_rate)
    wav_file.setnframes(num_frames)
    wav_file.writeframes(audio_data)
print("Successful")
