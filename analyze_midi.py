
import mido

midi_file = '1674.mid'

try:
    mid = mido.MidiFile(midi_file)
    print(f"Successfully loaded {midi_file}")
    print(f"Number of tracks: {len(mid.tracks)}")
    print(f"MIDI file type: {mid.type}")
    print(f"Ticks per beat: {mid.ticks_per_beat}")

except FileNotFoundError:
    print(f"Error: {midi_file} not found. Please make sure the file is in the correct directory.")
except Exception as e:
    print(f"An error occurred: {e}")
