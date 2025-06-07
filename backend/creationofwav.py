from pydub import AudioSegment
from pydub.generators import Sine

# Generate a sine wave tone
tone = Sine(440).to_audio_segment(duration=2000)  # 440 Hz for 2 seconds
tone.export("alert.wav", format="wav")
