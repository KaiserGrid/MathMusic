

import mido

def extract_notes(midi_file_path, output_txt_path):
    """Extracts all notes from a MIDI file and saves them to a text file."""
    try:
        mid = mido.MidiFile(midi_file_path)
        with open(output_txt_path, "w") as f:
            f.write(f"Note Extraction from {midi_file_path}\n")
            f.write("-" * 40 + "\n")
            
            for i, track in enumerate(mid.tracks):
                f.write(f"\n--- Track {i}: {track.name} ---\n")
                current_time = 0
                for msg in track:
                    current_time += msg.time
                    if msg.type == 'note_on':
                        f.write(f"Time: {current_time}, Note: {msg.note}, Velocity: {msg.velocity}\n")
        print(f"Successfully extracted notes to {output_txt_path}")

    except FileNotFoundError:
        print(f"Error: {midi_file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    extract_notes("1674.mid", "beethoven_notes.txt")

