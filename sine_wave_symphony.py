
import math
from midiutil import MIDIFile

# Parameters
duration_seconds = 60  # Total duration of the piece in seconds
tempo_bpm = 60         # Beats per minute
volume = 100           # MIDI velocity (0-127)

# MIDI setup
track = 0
channel = 0
time = 0  # Start time of the track

# Create the MIDIFile Object
MyMIDI = MIDIFile(1)  # One track
MyMIDI.addTempo(track, time, tempo_bpm)

# Generate notes from a sine wave
num_notes = int(duration_seconds * (tempo_bpm / 60))
for i in range(num_notes):
    # Sine wave calculation
    # The frequency of the sine wave will determine how quickly the melody rises and falls
    # The amplitude will determine the range of pitches
    pitch = int(60 + 12 * math.sin(2 * math.pi * i / (num_notes / 4))) # Map sine wave to a nice piano range

    # Add a note
    MyMIDI.addNote(track, channel, pitch, time, 1, volume)
    time += 1 # Move to the next beat

# Write it to disk
with open("sine_wave_symphony.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

print("Successfully created sine_wave_symphony.mid")
