
import numpy as np
from midiutil import MIDIFile

# Lorenz attractor parameters
sigma, rho, beta = 10, 28, 8/3
dt = 0.01
num_steps = 4000

# Initial state
x, y, z = 0.1, 0, 0

# Store the points
points = np.zeros((num_steps, 3))
for i in range(num_steps):
    dx = sigma * (y - x) * dt
    dy = (x * (rho - z) - y) * dt
    dz = (x * y - beta * z) * dt
    x, y, z = x + dx, y + dy, z + dz
    points[i] = [x, y, z]

# --- Music Generation ---

# Musical parameters
tempo_bpm = 140
note_duration = 0.25  # Sixteenth notes

# MIDI setup
track = 0
channel = 0
time = 0
MyMIDI = MIDIFile(1)
MyMIDI.addTempo(track, time, tempo_bpm)

# Map points to music
y_coords = points[:, 1]
z_coords = points[:, 2]

# Normalize y to a nice piano range (e.g., 3 octaves from C4)
y_min, y_max = y_coords.min(), y_coords.max()
pitches = 48 + 36 * (y_coords - y_min) / (y_max - y_min)

# Normalize z to a velocity range
z_min, z_max = z_coords.min(), z_coords.max()
velocities = 60 + 47 * (z_coords - z_min) / (z_max - z_min)

# C-Major scale (MIDI note numbers)
c_major_scale = [0, 2, 4, 5, 7, 9, 11]

def snap_to_scale(pitch, scale, base_note=48):
    """Snaps a pitch to the nearest note in a scale."""
    pitch_class = int(round(pitch)) - base_note
    octave = pitch_class // 12
    semitone = pitch_class % 12
    
    # Find the closest scale degree
    closest_degree = min(scale, key=lambda x: abs(x - semitone))
    
    return base_note + octave * 12 + closest_degree

# Generate notes
for i in range(num_steps):
    pitch = snap_to_scale(pitches[i], c_major_scale)
    velocity = int(velocities[i])
    
    MyMIDI.addNote(track, channel, pitch, time, note_duration, velocity)
    time += note_duration

# Write to disk
with open("lorenz_attractor_symphony.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

print("Successfully created lorenz_attractor_symphony.mid")
