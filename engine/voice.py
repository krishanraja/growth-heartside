"""Local neural narration with pinned Apache-2.0 Kokoro weights. No paid API.

Generated narration remains a draft for human review. It is not an imitation
of a customer, creator or founder and supplies no testimonial evidence.
"""
import json
from pathlib import Path
import tempfile
import urllib.request
import wave

from . import assets, ledger

ENGINE_VERSION = 1
_MODEL = None
_MODEL_KEY = None


def models(root):
    root = Path(root)
    records = json.loads((root / 'config/voice-files.json').read_text())
    folder = assets.local_path(root, 'local/voice/models')
    folder.mkdir(parents=True, exist_ok=True)
    for name, record in records.items():
        if name not in {'kokoro-v1.0.int8.onnx', 'voices-v1.0.bin'}:
            raise ValueError('unrecognized voice model file')
        target = folder / name
        if target.exists() and assets.sha256(target) == record['sha256']:
            continue
        # The source, size and checksum are reviewed and pinned in this repository.
        if record['url'] != 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/' + name:
            raise ValueError('voice weights must come from the pinned upstream release')
        temporary = target.with_suffix(target.suffix + '.tmp')
        try:
            with urllib.request.urlopen(record['url'], timeout=60) as source, temporary.open('wb') as out:
                size = 0
                while chunk := source.read(1024 * 1024):
                    size += len(chunk)
                    if size > record['size']:
                        raise ValueError('voice model download exceeded its declared size')
                    out.write(chunk)
            if size != record['size'] or assets.sha256(temporary) != record['sha256']:
                raise ValueError('voice model checksum mismatch')
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
    return folder, records


def synthesize(root, transcript, source_sha, limit_seconds):
    global _MODEL, _MODEL_KEY
    if not isinstance(transcript, str) or not 1 <= len(transcript.split()) <= 40:
        raise ValueError('local narration must be a checked script of at most forty words')
    folder, records = models(root)
    identity = {'engine': 'kokoro-onnx', 'version': ENGINE_VERSION, 'voice': 'af_heart', 'speed': 1.05,
                'transcript': transcript, 'source_sha': source_sha, 'weights': records}
    key = ledger.digest(identity)
    target = assets.local_path(root, f'local/provider-assets/kokoro/{key}')
    record_path = target / 'narration.json'
    if record_path.exists():
        existing = json.loads(record_path.read_text())
        file = assets.local_path(root, existing['path'])
        if all(existing.get(k) == v for k, v in identity.items()) and file.exists() and existing.get('sha256') == assets.sha256(file) and existing.get('seconds', 999) <= limit_seconds:
            return record_path
    import numpy as np
    import onnxruntime as ort
    import soundfile as sf
    from kokoro_onnx import Kokoro
    model_key = str(folder)
    if _MODEL_KEY != model_key:
        options = ort.SessionOptions(); options.intra_op_num_threads = 2; options.inter_op_num_threads = 1
        session = ort.InferenceSession(str(folder / 'kokoro-v1.0.int8.onnx'), sess_options=options, providers=['CPUExecutionProvider'])
        _MODEL = Kokoro.from_session(session, str(folder / 'voices-v1.0.bin'))
        _MODEL_KEY = model_key
    samples, sample_rate = _MODEL.create(transcript, voice='af_heart', speed=1.05, lang='en-us')
    seconds = len(samples) / sample_rate
    if seconds > limit_seconds or seconds < 1 or not np.isfinite(samples).all() or float(np.max(np.abs(samples))) < .01:
        raise ValueError('neural narration is silent, invalid or longer than the film; use a shorter script')
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target) as work:
        work = Path(work)
        sf.write(work / 'voice.wav', samples, sample_rate, subtype='PCM_16')
        record = {**identity, 'path': str((target / 'voice.wav').relative_to(root)),
                  'sha256': assets.sha256(work / 'voice.wav'), 'role': 'narration', 'status': 'draft_local_synthesis',
                  'provider': 'kokoro-local', 'seconds': seconds,
                  'rights': 'Kokoro-82M model and voices: Apache-2.0; kokoro-onnx runtime: MIT. See docs/VOICE-LICENSES.md.',
                  'disclosure': 'Synthetic brand narration. Buddy is a fictional AI character.', 'generation_cost_usd': 0}
        (work / 'voice.wav').replace(target / 'voice.wav')
        (work / 'narration.json').write_text(json.dumps(record, indent=2) + '\n')
        (work / 'narration.json').replace(record_path)
    return record_path
