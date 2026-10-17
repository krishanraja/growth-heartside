import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import wave

from engine import assets, voice

ROOT = Path(__file__).resolve().parents[1]


class VoiceBoundaryTests(unittest.TestCase):
    def test_scripts_are_bounded_before_loading_any_model(self):
        with patch('engine.voice.models', side_effect=AssertionError('must not load')):
            with self.assertRaises(ValueError):
                voice.synthesize(ROOT, 'word ' * 41, 'a'*40, 10)

    def test_unpinned_download_sources_are_refused(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root/'config').mkdir()
            (root/'config/voice-files.json').write_text(json.dumps({'voices-v1.0.bin': {'url':'https://example.com/model', 'size':10, 'sha256':'a'*64}}))
            with self.assertRaises(ValueError):
                voice.models(root)


@unittest.skipUnless(os.environ.get('RUN_VOICE_INTEGRATION') == '1' and importlib.util.find_spec('kokoro_onnx'),
                     'set RUN_VOICE_INTEGRATION=1 with media requirements for real local neural synthesis')
class NeuralVoiceTests(unittest.TestCase):
    def test_actual_synthesis_cache_and_duration_failure_preserve_good_audio(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root/'config').mkdir()
            shutil.copyfile(ROOT/'config/voice-files.json', root/'config/voice-files.json')
            if (ROOT/'local/voice/models').exists():
                shutil.copytree(ROOT/'local/voice/models', root/'local/voice/models')
            text = 'For the person your dog waits for. Your dog loves you too.'
            path = voice.synthesize(root, text, 'a'*40, 10)
            record = json.loads(path.read_text()); audio = assets.local_path(root, record['path'])
            self.assertEqual(record['generation_cost_usd'], 0)
            self.assertEqual(record['status'], 'draft_local_synthesis')
            with wave.open(str(audio)) as wav:
                self.assertEqual(wav.getframerate(), 24000)
                self.assertGreater(wav.getnframes(), 24000)
                self.assertLess(wav.getnframes(), 240000)
            checksum = assets.sha256(audio)
            with patch.object(voice._MODEL, 'create', side_effect=AssertionError('cached synthesis must not repeat')):
                self.assertEqual(voice.synthesize(root, text, 'a'*40, 10), path)
            with self.assertRaises(ValueError):
                voice.synthesize(root, text, 'a'*40, 1)
            self.assertEqual(assets.sha256(audio), checksum)


if __name__ == '__main__':
    unittest.main()
