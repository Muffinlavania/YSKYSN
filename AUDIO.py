import wave
try:
    import audioop
except ImportError:
    import pyaudioop as audioop

def spawnsound(file, speed):
    with wave.open(file, 'rb') as wave_file:
        # Get the parameters of the input wave file
        channels, width, framerate, frames, _, _ = wave_file.getparams()

        # Read the audio data from the input wave file
        input_data = wave_file.readframes(frames)

    return audioop.ratecv(input_data, width, channels, framerate, int(framerate * speed), None)[0]
