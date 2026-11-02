"""The lock system must refuse drift, unapproved or edited lines, wrong-breed lines and altered renders."""
import copy, hashlib, json, os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'factory'))
import lock  # noqa: E402

SPECS = os.path.join(os.path.dirname(__file__), '..', 'factory', 'specs')


def load(name):
    return json.load(open(os.path.join(SPECS, name + '.json'), encoding='utf-8'))


class LockTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); lib = self.tmp.name
        os.makedirs(f'{lib}/renders'); os.makedirs(f'{lib}/locks')
        self._saved = (lock.LIB, copy.deepcopy(lock.RENDERS), lock.LEDGER, lock.HERE)
        lock.LIB = lib; lock.LEDGER = f'{lib}/ledger.json'
        for f, r in lock.RENDERS.items():  # stand-in render files, registered by their own checksum
            data = f'render {f}'.encode(); open(f'{lib}/renders/{f}', 'wb').write(data)
            r['sha256'] = hashlib.sha256(data).hexdigest()

    def tearDown(self):
        lock.LIB, renders, lock.LEDGER, lock.HERE = self._saved
        lock.RENDERS.clear(); lock.RENDERS.update(renders); self.tmp.cleanup()

    def problems(self, spec):
        return lock.check(spec)[0]

    def test_approved_roast_passes(self):
        self.assertEqual(self.problems(load('F06-frenchie')), [])

    def test_variants_share_the_fingerprint_and_drift_breaks_it(self):
        fr, la = load('F06-frenchie'), load('F06-lab')
        self.assertEqual(lock.fingerprint(fr), lock.fingerprint(la))
        drift = copy.deepcopy(la); drift['durs'][1] = 1.0
        self.assertNotEqual(lock.fingerprint(fr), lock.fingerprint(drift))
        drift = copy.deepcopy(la); drift['lines'] = drift['lines'][:2]
        self.assertNotEqual(lock.fingerprint(fr), lock.fingerprint(drift))

    def test_unapproved_lines_are_held(self):
        self.assertTrue(any('not approved' in p for p in self.problems(load('F06-lab'))))

    def test_wrong_breed_line_is_held(self):
        s = load('F10'); s['cast']['D'] = 'lab'
        s['end']['renders'] = ['mug-real-lab.jpg']
        self.assertTrue(any('tagged only for dachshund' in p for p in self.problems(s)))

    def test_edited_approved_line_is_held(self):
        line = lock.LINES['F10.c02']; saved = line['text']
        try:
            line['text'] = 'A really good stick, honestly.'
            self.assertTrue(any('edited after Krish approved' in p for p in self.problems(load('F10'))))
        finally:
            line['text'] = saved

    def test_altered_or_wrong_breed_render_is_held(self):
        s = load('F06-frenchie')
        open(f'{lock.LIB}/renders/{s["render"]}', 'wb').write(b'retouched')
        self.assertTrue(any('differs from the approved render' in p for p in self.problems(s)))
        s = load('F06-frenchie'); s['render'] = 'mug-real-lab.jpg'
        self.assertTrue(any('shows a lab' in p for p in self.problems(s)))

    def test_free_text_is_refused(self):
        s = load('F06-frenchie'); s['lines'][0] = 'Some brand new joke.'
        self.assertTrue(any('not in the joke bank' in p for p in self.problems(s)))

    def test_ramp_needs_krish_for_the_first_variants_and_declines_pause(self):
        lock.HERE = self.tmp.name
        master = load('F06-frenchie')
        json.dump({'id': 'F06-frenchie', 'status': 'locked', 'fingerprint': lock.fingerprint(master)}, open(f'{self.tmp.name}/locks/F06-frenchie.json', 'w'))
        v = load('F06-lab'); v['id'] = 'F06-lab-1'
        self.assertEqual(lock.ramp(v)[0], 'krish')
        lock.record(v, 'krish-decline', 'not funny'); lock.record(v, 'krish-decline', 'still not')
        self.assertEqual(json.load(open(f'{self.tmp.name}/locks/F06-frenchie.json'))['status'], 'paused')
        self.assertTrue(any(r['line'] == 'F06.la1' for r in lock.ledger()['retired']))


if __name__ == '__main__':
    unittest.main()
