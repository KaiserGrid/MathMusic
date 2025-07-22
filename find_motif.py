
import mido

def find_beethoven_motif(midi_file_path):
    """Parses a MIDI file and searches for Beethoven's 5th motif."""
    try:
        mid = mido.MidiFile(midi_file_path)
    except FileNotFoundError:
        print(f"Error: {midi_file_path} not found.")
        return

    all_notes = []
    ticks_per_beat = mid.ticks_per_beat

    for track_idx, track in enumerate(mid.tracks):
        abs_time = 0
        open_notes = {}
        for msg in track:
            abs_time += msg.time

            if msg.type == 'note_on' and msg.velocity > 0:
                open_notes[msg.note] = (abs_time, msg.velocity)
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in open_notes:
                    start_time, velocity = open_notes.pop(msg.note)
                    duration = abs_time - start_time
                    all_notes.append({
                        'track': track_idx,
                        'pitch': msg.note,
                        'start_time_ticks': start_time,
                        'duration_ticks': duration,
                        'velocity': velocity
                    })
    
    # Sort notes by their start time
    all_notes.sort(key=lambda x: x['start_time_ticks'])

    # --- Motif Search ---
    found_motifs = []
    for i in range(len(all_notes) - 3):
        n1, n2, n3, n4 = all_notes[i:i+4]

        # 1. Melodic check (G-G-G-Eb pattern)
        is_melodic_match = (
            n1['pitch'] == n2['pitch'] == n3['pitch'] and
            n4['pitch'] == n1['pitch'] - 3
        )

        if not is_melodic_match:
            continue

        # 2. Rhythmic check (short-short-short-long)
        # Allow for some timing variation
        short_duration_avg = (n1['duration_ticks'] + n2['duration_ticks'] + n3['duration_ticks']) / 3
        is_rhythmic_match = (
            n4['duration_ticks'] > 2 * short_duration_avg and
            abs(n1['duration_ticks'] - n2['duration_ticks']) < ticks_per_beat / 4 and
            abs(n2['duration_ticks'] - n3['duration_ticks']) < ticks_per_beat / 4
        )

        if not is_rhythmic_match:
            continue

        # 3. Proximity check (notes must be consecutive)
        # Check if the start of the next note is close to the end of the previous one
        is_proximate = (
            abs(n2['start_time_ticks'] - (n1['start_time_ticks'] + n1['duration_ticks'])) < ticks_per_beat / 2 and
            abs(n3['start_time_ticks'] - (n2['start_time_ticks'] + n2['duration_ticks'])) < ticks_per_beat / 2 and
            abs(n4['start_time_ticks'] - (n3['start_time_ticks'] + n3['duration_ticks'])) < ticks_per_beat / 2
        )

        if is_melodic_match and is_rhythmic_match and is_proximate:
            # Convert start time to beat number for readability
            start_beat = round(n1['start_time_ticks'] / ticks_per_beat, 2)
            found_motifs.append({'track': n1['track'], 'start_beat': start_beat, 'pitch': n1['pitch']})

    # --- Report Findings ---
    if not found_motifs:
        print("Could not find any instances of the motif.")
        return

    print(f"Found {len(found_motifs)} instances of the 'short-short-short-long' motif:")
    # Group by track to make it readable
    motifs_by_track = {}
    for motif in found_motifs:
        track = motif['track']
        if track not in motifs_by_track:
            motifs_by_track[track] = []
        motifs_by_track[track].append(motif['start_beat'])
    
    for track, beats in sorted(motifs_by_track.items()):
        print(f"  - Track {track}: Found at beats {sorted(list(set(beats)))}")

if __name__ == "__main__":
    find_beethoven_motif("1674.mid")
