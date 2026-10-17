import copy
import json
from pathlib import Path
import tempfile
import unittest

from engine import assets, ledger, media, operations


class OperatorEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(); self.root = Path(self.temporary.name)
        self.db = ledger.connect(self.root/'local/engine.sqlite3')
        self.cid = 'IG_EMO_REEL_C90_H01_V1_20261017'; self.revision = 'a'*64
        path = self.root/'local/media/test/payload.bin'; path.parent.mkdir(parents=True); path.write_bytes(b'checked fixture output')
        manifest = {'version':media.VERSION, 'creative_id':self.cid, 'revision':self.revision,
                    'files':{role:{'path':str(path.relative_to(self.root)), 'sha256':assets.sha256(path)} for role in media.REQUIRED_ROLES}}
        (path.parent/'manifest.json').write_text(json.dumps(manifest))
        ledger.record_render(self.db,self.cid,self.revision,{},manifest)

    def tearDown(self):
        self.db.close(); self.temporary.cleanup()

    def event(self, status):
        return {'event_id':'test-'+status,'type':'creative_status','creative_id':self.cid,
                'revision':self.revision,'status':status,
                'url':'https://www.instagram.com/reel/example/' if status=='published' else None}

    def test_recorded_human_publication_roundtrips_idempotently_without_a_publisher(self):
        events = [self.event('approved'),self.event('published')]
        self.assertTrue(all(r['status']=='applied' for r in operations.apply(self.root,self.db,events)))
        self.assertTrue(all(r['status']=='already_applied' for r in operations.apply(self.root,self.db,events)))
        row = self.db.execute('SELECT status,published_url FROM creatives').fetchone()
        self.assertEqual(row['status'],'published')
        self.assertEqual(self.db.execute('SELECT count(*) FROM creative_events').fetchone()[0],3)
        changed = copy.deepcopy(events[0]); changed['status']='skipped'
        with self.assertRaises(ValueError):operations.apply(self.root,self.db,[changed])

    def test_tampered_files_and_extra_customer_fields_cannot_be_recorded(self):
        path=self.root/'local/media/test/payload.bin';path.write_bytes(b'tampered')
        with self.assertRaises(ValueError):operations.apply(self.root,self.db,[self.event('approved')])
        bad=self.event('reviewed');bad['customer_email']='forbidden field'
        with self.assertRaises(ValueError):operations.apply(self.root,self.db,[bad])
        self.assertEqual(self.db.execute('SELECT count(*) FROM operator_events').fetchone()[0],0)

    def test_partial_batch_replay_and_aggregate_insight_feed(self):
        invalid=self.event('published');invalid['status']='invalid'
        with self.assertRaises(ValueError):operations.apply(self.root,self.db,[self.event('approved'),invalid])
        result=operations.apply(self.root,self.db,[self.event('approved'),self.event('published')])
        self.assertEqual([r['status'] for r in result],['already_applied','applied'])
        event={'event_id':'native-observation-1','type':'insight','observation':{
            'creative_id':self.cid,'revision':self.revision,'platform':'instagram','source':'native',
            'source_url':'https://www.instagram.com/insights/','observed_at':'2026-10-17T09:00:00Z',
            'published_at':'2026-10-15T09:00:00Z','attribution':'none','values':{'reach':2000,'sends':10}}}
        operations.apply(self.root,self.db,[event]);operations.apply(self.root,self.db,[event])
        self.assertEqual(self.db.execute('SELECT count(*) FROM insights').fetchone()[0],1)
