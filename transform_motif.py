

import mido
import copy

def transform_beethoven_motif(midi_file_path, output_file_path):
    """Finds, transforms (inverts), and replaces the Beethoven motif in a MIDI file."""
    try:
        mid = mido.MidiFile(midi_file_path)
    except FileNotFoundError:
        print(f"Error: {midi_file_path} not found.")
        return

    ticks_per_beat = mid.ticks_per_beat
    new_mid = copy.deepcopy(mid)

    for track_idx, track in enumerate(mid.tracks):
        notes = []
        abs_time = 0
        open_notes = {}

        # First, extract all notes from the track
        for msg in track:
            abs_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                open_notes[msg.note] = (abs_time, msg.velocity)
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in open_notes:
                    start_time, velocity = open_notes.pop(msg.note)
                    duration = abs_time - start_time
                    notes.append({
                        'track': track_idx, 'pitch': msg.note, 'start': start_time,
                        'duration': duration, 'velocity': velocity
                    })
        
        notes.sort(key=lambda x: x['start'])

        # Now, find and transform the motif
        i = 0
        while i < len(notes) - 3:
            n1, n2, n3, n4 = notes[i:i+4]

            is_melodic_match = (n1['pitch'] == n2['pitch'] == n3['pitch'] and n4['pitch'] == n1['pitch'] - 3)
            if not is_melodic_match:
                i += 1
                continue

            short_avg = (n1['duration'] + n2['duration'] + n3['duration']) / 3
            is_rhythmic_match = (n4['duration'] > 2 * short_avg and abs(n1['duration'] - n2['duration']) < ticks_per_beat / 4)
            if not is_rhythmic_match:
                i += 1
                continue

            is_proximate = (
                abs(n2['start'] - (n1['start'] + n1['duration'])) < ticks_per_beat / 2 and
                abs(n3['start'] - (n2['start'] + n2['duration'])) < ticks_per_beat / 2
            )
            if not is_proximate:
                i += 1
                continue

            # --- Transformation: Inversion ---
            # We found a motif. Let's invert the last note.
            # The interval is a minor third down (-3 semitones). We invert it to a minor third up (+3 semitones).
            original_pitch = n1['pitch']
            inverted_pitch = original_pitch + 3 # The transformation!

            # Find the corresponding note message in the new MIDI track and change its pitch
            time_cursor = 0
            for msg in new_mid.tracks[track_idx]:
                time_cursor += msg.time
                if time_cursor == n4['start'] and msg.type == 'note_on' and msg.note == n4['pitch']:
                    msg.note = inverted_pitch
                    print(f"Transformed motif at beat {round(n1['start'] / ticks_per_beat, 2)} in Track {track_idx}")
                    break
            
            # Skip past the notes of this motif to avoid overlapping finds
            i += 4

    # Write the transformed MIDI to a new file
    new_mid.save(output_file_path)
    print(f"\nSuccessfully created transformed file: {output_file_path}")

if __name__ == "__main__":
    transform_beethoven_motif("1674.mid", "beethoven_transformed.mid")
