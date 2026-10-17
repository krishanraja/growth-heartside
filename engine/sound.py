"""An original, quiet three-note score synthesized locally without provider spend."""
import math
import struct
import wave


def score(path, duration, beats):
    rate = 48000
    # C major add9, with a soft attack and no sampled or copyrighted recording.
    notes = [(0, 261.626), (0.18, 329.628), (0.36, 391.995)]
    notes += [(time, 523.251 if index % 2 else 391.995) for index, time in enumerate(beats) if time > .5]
    with wave.open(str(path), 'wb') as out:
        out.setnchannels(1); out.setsampwidth(2); out.setframerate(rate)
        chunk = bytearray()
        for frame in range(round(duration * rate)):
            time = frame / rate
            value = 0
            for start, frequency in notes:
                age = time - start
                if 0 <= age <= 3:
                    envelope = min(1, age / .04) * math.exp(-2.1 * age)
                    value += .075 * envelope * (math.sin(2 * math.pi * frequency * age) + .2 * math.sin(4 * math.pi * frequency * age))
            value *= min(1, max(0, (duration - time) / .4))
            chunk.extend(struct.pack('<h', int(max(-1, min(1, value)) * 32767)))
            if len(chunk) >= 96000:
                out.writeframesraw(chunk); chunk.clear()
        out.writeframes(chunk)
