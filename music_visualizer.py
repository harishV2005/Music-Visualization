import pygame
import numpy as np
import wave
import sys
import math 

filename = "Processing Audio Visualizer Project.wav"

try:
    wf = wave.open(filename, 'rb')
except wave.Error as e:
    print(f"Error opening WAV file: {e}")
    print("Please ensure the file is a valid, uncorrupted WAV file and exists in the same directory.")
    sys.exit(1) 
n_channels = wf.getnchannels()
sample_width = wf.getsampwidth()
frame_rate = wf.getframerate()
n_frames = wf.getnframes()
audio_data = wf.readframes(n_frames)
wf.close()
if not audio_data:
    print("Error: Audio file contains no data.")
    sys.exit(1)

sound_array = np.frombuffer(audio_data, dtype=np.int16)

if n_channels == 2:
    sound_array = sound_array[::2] 
pygame.init()
pygame.mixer.init()

try:
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
except pygame.error as e:
    print(f"Error loading or playing music with Pygame: {e}")
    print("Ensure the audio file format is supported by Pygame (e.g., uncompressed WAV).")
    sys.exit(1)

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Music Visualizer")

n_bars = 100
bar_width = width // n_bars
bar_color = (0, 255, 200)

running = True
frame_size = 1024 
current_frame = 0
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    if current_frame + frame_size <= len(sound_array): # Changed to <=
        frame_data = sound_array[current_frame:current_frame + frame_size]

        
        window = np.hanning(len(frame_data))
        windowed_frame_data = frame_data * window
        fft_result = np.abs(np.fft.fft(windowed_frame_data))[:n_bars]
        max_fft_val = np.max(fft_result)
        if max_fft_val == 0:
            
            fft_result_normalized = np.zeros_like(fft_result)
        else:
            
            fft_result_normalized = (fft_result / max_fft_val) * height

        current_frame += frame_size

        
        for i in range(n_bars):
            
            val = fft_result_normalized[i]

            
            if math.isnan(val) or math.isinf(val):
                bar_height = 0
            else:
                bar_height = int(val) # Convert to integer for drawing

            x = i * bar_width
            pygame.draw.rect(screen, bar_color, (x, height - bar_height, bar_width - 2, bar_height))
    else:
       
        running = False # Stop the loop when audio ends

    pygame.display.flip()
    clock.tick(30) # Limit frame rate to 30 FPS

pygame.quit()
sys.exit() 