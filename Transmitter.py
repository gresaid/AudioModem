import wave

print("Open file...")
with open("audio.bin", "rb") as bin_file:
data = bin_file.read()
n = 0
while 2 ** n <= len(data) + n:
    n += 1

# remove the parity bits from the data
decoded_data = []
for i in range(len(data)):
    # check if the bit is a parity bit
    if i + 1 not in [2 ** j - 1 for j in range(n)]:
        # append the data bit to the decoded data
        decoded_data.append(data[i])

decoded_data = bytes(decoded_data)


num_channels = 1  # Mono
sample_width = 2  # 16-bit
frame_rate = 44100  # sample rate
num_frames = len(audio_data) // (num_channels * sample_width)
with wave.open("audio.wav", "wb") as wav_file:
    wav_file.setnchannels(num_channels)
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(frame_rate)
    wav_file.setnframes(num_frames)
    wav_file.writeframes(decoded_data)
    print("Successful")
