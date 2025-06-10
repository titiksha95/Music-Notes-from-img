import cv2
import numpy as np
import pygame
from PIL import Image
import os
from pydub import AudioSegment

class ImageToMusicConverter:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()

        self.note_frequencies = {
            60: 261.63, 61: 277.18, 62: 293.66, 63: 311.13, 64: 329.63,
            65: 349.23, 66: 369.99, 67: 392.00, 68: 415.30, 69: 440.00,
            70: 466.16, 71: 493.88, 72: 523.25, 73: 554.37, 74: 587.33,
            75: 622.25, 76: 659.25, 77: 698.46, 78: 739.99, 79: 783.99,
            80: 830.61, 81: 880.00, 82: 932.33, 83: 987.77, 84: 1046.50
        }

    def brightness_to_note(self, value):
        """Convert a color value (0-255) to a MIDI note number (60-84)"""
        min_note = 60
        max_note = 84
        note = int((value / 255.0) * (max_note - min_note) + min_note)
        return max(min(note, max_note), min_note)

    def image_to_audio_array(self, image_path, image_size=(24, 24), note_duration=0.12):
        """Convert RGB image to stereo audio"""
        print("[→] Converting image to detailed audio...")
        img = Image.open(image_path).convert('RGB').resize(image_size, Image.Resampling.LANCZOS)
        img_array = np.array(img)

        sample_rate = 44100
        total_samples = int(note_duration * sample_rate)
        left_channel = np.zeros(0, dtype=np.float32)
        right_channel = np.zeros(0, dtype=np.float32)

        for y in range(img_array.shape[0]):
            for x in range(img_array.shape[1]):
                r, g, b = img_array[y, x]
                midi_r = self.brightness_to_note(r)
                midi_g = self.brightness_to_note(g)
                midi_b = self.brightness_to_note(b)

                freq_r = self.note_frequencies.get(midi_r, 440)
                freq_g = self.note_frequencies.get(midi_g, 440)
                freq_b = self.note_frequencies.get(midi_b, 440)

                t = np.linspace(0, note_duration, total_samples, False)
                tone = (
                    0.33 * np.sin(2 * np.pi * freq_r * t) +
                    0.33 * np.sin(2 * np.pi * freq_g * t) +
                    0.33 * np.sin(2 * np.pi * freq_b * t)
                ).astype(np.float32)

                fade_samples = int(0.01 * sample_rate)
                for i in range(fade_samples):
                    tone[i] *= i / fade_samples
                    tone[-(i+1)] *= i / fade_samples

                brightness = (r + g + b) / 3.0
                volume = brightness / 255.0
                tone *= volume

                pan = x / image_size[0]
                left = tone * (1 - pan)
                right = tone * pan

                left_channel = np.concatenate([left_channel, left])
                right_channel = np.concatenate([right_channel, right])

        stereo = np.stack([left_channel, right_channel], axis=1)
        return stereo  

    def save_audio_as_mp3(self, stereo_data, output_path, sample_rate=44100):
        """Save stereo audio data as MP3"""
        print("[→] Saving stereo audio as MP3...")
        stereo_data = np.clip(stereo_data, -1, 1)
        stereo_int16 = (stereo_data * 32767).astype(np.int16)
        interleaved = stereo_int16.flatten()

        audio_segment = AudioSegment(
            interleaved.tobytes(),
            frame_rate=sample_rate,
            sample_width=2,
            channels=2
        )
        audio_segment.export(output_path, format="mp3", bitrate="192k")
        print(f"[✔] MP3 saved: {output_path}")

    def convert_image_to_mp3(self, image_path, output_path, image_size=(24, 24), note_duration=0.12):
        try:
            print(f"[→] Starting conversion: {image_path}")
            audio_data = self.image_to_audio_array(image_path, image_size, note_duration)
            self.save_audio_as_mp3(audio_data, output_path)
            duration = len(audio_data) / 44100
            print(f"[✔] Done! Duration: {duration:.2f}s | Output: {output_path}")
        except Exception as e:
            print(f"[✗] Error: {e}")
            raise

def main():
    converter = ImageToMusicConverter()
    # Update this path to your image file
    image_path = "C:/Users/jangi/OneDrive/Desktop/DreamTeam/Music Note/download.jpg"
    output_path = "output_music.mp3"

    if not os.path.exists(image_path):
        print("[!] Image not found.")
        return

    converter.convert_image_to_mp3(
        image_path=image_path,
        output_path=output_path,
        image_size=(24, 24),
        note_duration=0.12
    )

if __name__ == "__main__":
    main()