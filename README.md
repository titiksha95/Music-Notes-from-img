# 🎵 Image-to-Music Generator

This project converts an input image into a unique musical composition using Python. It leverages image processing to extract features and map them to audio frequencies and durations to create a soundscape inspired by the image.

## 🧠 Technologies Used

- Python 3.x
- OpenCV
- NumPy
- PIL (Python Imaging Library)
- Matplotlib
- Sounddevice
- SciPy

## 🖼️ How It Works

1. **Input**: Load and preprocess an image.
2. **Processing**:
   - Convert the image to grayscale.
   - Resize and normalize pixel data.
   - Map pixel values to sound frequencies and durations.
3. **Output**: Generate and play audio that represents the image visually through sound.

## 📁 File Structure

- `image_to_music.py`: Main file containing the complete logic.
- `download.jpg`: An example image you can test the program with (you can use your own).
- `output.mp3`: Audio output (can be generated during runtime).
- `requirements.txt`: List of dependencies.


