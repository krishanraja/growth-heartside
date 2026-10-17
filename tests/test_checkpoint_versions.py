import hashlib
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

from engine import state_store


class CheckpointVersionTests(unittest.TestCase):
    def test_identical_content_is_stored_once_and_restores_as_independent_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); folder=root/'local/assets';folder.mkdir(parents=True)
            (folder/'a.bin').write_bytes(b'same approved asset'*1000)
            (folder/'b.bin').write_bytes((folder/'a.bin').read_bytes())
            state_store.export(root,'local/backups/state.tgz')
            with tarfile.open(root/'local/backups/state.tgz') as archive:
                self.assertEqual(sum(m.islnk() for m in archive.getmembers()),1)
            (folder/'A.bin').write_bytes(b'case collision')
            with self.assertRaises(ValueError):state_store.export(root,'local/backups/collision.tgz')
            (folder/'A.bin').unlink()
            target=root/'another-machine';target.mkdir()
            state_store.restore(target,root/'local/backups/state.tgz')
            (target/'local/assets/a.bin').write_bytes(b'edited')
            self.assertEqual((target/'local/assets/b.bin').read_bytes(),b'same approved asset'*1000)

    def archive(self, path, version, bad_link=False):
        data=b'verified old state';checksum=hashlib.sha256(data).hexdigest()
        files={'local/assets/a.bin':{'sha256':checksum,'size':len(data)}}
        if bad_link:files['local/assets/b.bin']=files['local/assets/a.bin']
        with tarfile.open(path,'w:gz') as out:
            payload=json.dumps({'version':version,'files':files}).encode()
            header=tarfile.TarInfo('checkpoint.json');header.size=len(payload);out.addfile(header,io.BytesIO(payload))
            entry=tarfile.TarInfo('local/assets/a.bin');entry.size=len(data);out.addfile(entry,io.BytesIO(data))
            if bad_link:
                entry=tarfile.TarInfo('local/assets/b.bin');entry.type=tarfile.LNKTYPE;entry.linkname='../../outside';out.addfile(entry)

    def test_original_version_one_checkpoint_still_restores(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.archive(root/'old.tgz',1)
            state_store.restore(root,root/'old.tgz')
            self.assertEqual((root/'local/assets/a.bin').read_bytes(),b'verified old state')

    def test_external_hardlink_is_rejected_before_existing_state_changes(self):
        for name in ('local/assets/..\\..\\escape', 'local/assets/./a.bin', 'local//assets/a.bin', 'local/assets/a.bin:stream', 'local/assets/a.bin.'):
            self.assertFalse(state_store.permitted(name))
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.archive(root/'bad.tgz',2,True)
            marker=root/'local/assets/keep';marker.parent.mkdir(parents=True);marker.write_text('keep')
            with self.assertRaises(ValueError):state_store.restore(root,root/'bad.tgz',True)
            self.assertEqual(marker.read_text(),'keep')
