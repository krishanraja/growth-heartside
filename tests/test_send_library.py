"""The Heartside library sender checks every file before it sends any, and names paths as the lane's rule does."""
import json, os, sys, tempfile, unittest, hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'factory'))
import send_library as sl  # noqa: E402


class SendLibraryTest(unittest.TestCase):
    def folder(self, items, tamper=None):
        d = tempfile.mkdtemp(); manifest = []
        for post, name, body in items:
            open(os.path.join(d, name), 'wb').write(body)
            manifest.append({'post': post, 'file': name, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()})
        if tamper:
            open(os.path.join(d, tamper), 'ab').write(b'x')
        json.dump(manifest, open(os.path.join(d, 'manifest.json'), 'w'))
        return d

    def test_paths_follow_the_lane_rule(self):
        d = self.folder([('F01', 'heartside_F01_becoming-the-mug_reel.mp4', b'reel'), ('F06-frenchie', 'heartside_F06-frenchie_roast-frenchie_slide1.jpg', b'slide')])
        self.assertEqual([p[0] for p in sl.plan(d)], ['Posts/F01/heartside_F01_becoming-the-mug_reel.mp4', 'Posts/F06-frenchie/heartside_F06-frenchie_roast-frenchie_slide1.jpg'])
        self.assertIn('the reel', sl.plan(d)[0][5])

    def test_one_changed_file_sends_nothing(self):
        d = self.folder([('F01', 'a_reel.mp4', b'reel'), ('F02', 'b_cover.jpg', b'cover')], tamper='b_cover.jpg')
        with self.assertRaises(sl.SendError):
            sl.plan(d)

    def test_a_bad_post_id_sends_nothing(self):
        d = self.folder([('f01', 'a_reel.mp4', b'reel')])
        with self.assertRaises(sl.SendError):
            sl.plan(d)

    def test_only_narrows_the_send(self):
        d = self.folder([('F01', 'a_reel.mp4', b'reel'), ('F02', 'b_reel.mp4', b'reel2')])
        self.assertEqual([p[0] for p in sl.plan(d, {'F02'})], ['Posts/F02/b_reel.mp4'])


if __name__ == '__main__':
    unittest.main()
