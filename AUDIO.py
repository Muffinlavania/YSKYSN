from pydub import AudioSegment
#from pydub.playback import play as PLAY

def speed_change(filename, speed=1.0):
    sound = AudioSegment.from_file(filename)
    alteredframes = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })

    # convert the sound with altered frame rate to a standard frame rate so that regular playback programs will work right. They often only know how to play audio at standard frame rate (like 44.1k)
    return alteredframes.set_frame_rate(sound.frame_rate).raw_data
    
#play(speed_change("YSKYSN/dial1.wav", 3))
#print("hi")
