"""Portable, verified state checkpoints. No lists, raw customer data or credentials.

GitHub Actions stores this archive as a restricted-download artifact and restores
it before the next run. One workflow concurrency group owns the writer lock.
"""
from contextlib import closing
import io
import json
from pathlib import Path, PurePosixPath
import shutil
import sqlite3
import tarfile
import tempfile
import uuid

from . import assets, ledger

DIRECTORIES = {'state', 'assets', 'media', 'provider-assets', 'automation'}
MAX_BYTES = 500 * 1024 * 1024
MAX_FILES = 12000
MAX_EXPANDED_BYTES = 2 * 1024 * 1024 * 1024


def permitted(name):
    path = PurePosixPath(name)
    return (not path.is_absolute() and '..' not in path.parts and len(path.parts) >= 2
            and path.parts[0] == 'local' and (path.parts[1] in DIRECTORIES or name == 'local/engine.sqlite3'))


def export(root, destination):
    root = Path(root)
    destination = assets.local_path(root, destination)
    if destination.exists():
        raise ValueError('choose a new snapshot file; checkpoints are immutable')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        stage = Path(temporary)
        files = {}
        for directory in sorted(DIRECTORIES):
            source = root / 'local' / directory
            if not source.exists():
                continue
            for path in sorted(source.rglob('*')):
                if path.is_symlink():
                    raise ValueError('checkpoint cannot contain symlinks')
                if path.name in {'review.zip', 'runner.lock'} and directory == 'automation':
                    continue  # Derivable from checked media and pack JSON; avoid duplicate bytes.
                if path.is_file() and not any(part.startswith('.build-') for part in path.parts):
                    name = path.relative_to(root).as_posix()
                    files[name] = path
        database = root / 'local/engine.sqlite3'
        if database.exists():
            with closing(ledger.connect(database)) as db:
                ledger.backup(db, stage / 'engine.sqlite3')
            files['local/engine.sqlite3'] = stage / 'engine.sqlite3'
        if len(files) > MAX_FILES:
            raise ValueError('checkpoint exceeds the file count bound')
        manifest = {name: {'sha256': assets.sha256(path), 'size': path.stat().st_size} for name, path in files.items()}
        unique = {entry['sha256']: entry['size'] for entry in manifest.values()}
        if sum(unique.values()) > MAX_BYTES or sum(entry['size'] for entry in manifest.values()) > MAX_EXPANDED_BYTES:
            raise ValueError('checkpoint exceeds its unique or expanded byte bound')
        temporary_archive = destination.with_name('.' + destination.name + '-' + uuid.uuid4().hex)
        try:
            with tarfile.open(temporary_archive, 'w:gz') as archive:
                payload = json.dumps({'version': 2, 'files': manifest}, sort_keys=True).encode()
                info = tarfile.TarInfo('checkpoint.json'); info.size = len(payload)
                archive.addfile(info, io.BytesIO(payload))
                seen = {}
                for name, path in files.items():
                    checksum = manifest[name]['sha256']
                    if checksum in seen:
                        link = tarfile.TarInfo(name); link.type = tarfile.LNKTYPE; link.linkname = seen[checksum]
                        archive.addfile(link)
                    else:
                        archive.add(path, arcname=name, recursive=False)
                        seen[checksum] = name
            if temporary_archive.stat().st_size > 100 * 1024 * 1024:
                raise ValueError('compressed checkpoint exceeds the 100 MB zero-spend storage policy; no new state artifact may be uploaded')
            temporary_archive.replace(destination)
        finally:
            temporary_archive.unlink(missing_ok=True)
    return {'path': str(destination.relative_to(root)), 'sha256': assets.sha256(destination), 'files': len(files)}


def restore(root, source, replace=False):
    root = Path(root).resolve()
    targets = [root / 'local' / d for d in DIRECTORIES] + [root / 'local/engine.sqlite3']
    if not replace and any(p.exists() for p in targets):
        raise ValueError('restore needs an empty state directory or explicit --replace; close other engine processes first')
    with tempfile.TemporaryDirectory(dir=root, prefix='.restore-') as temporary:
        stage = Path(temporary)
        with tarfile.open(source, 'r:gz') as archive:
            members = archive.getmembers()
            if len(members) > MAX_FILES + 1 or sum(m.size for m in members) > MAX_BYTES + 4000000:
                raise ValueError('checkpoint exceeds extraction bounds')
            names = [m.name for m in members]
            if len(names) != len(set(names)) or 'checkpoint.json' not in names:
                raise ValueError('checkpoint has duplicate entries or no manifest')
            if any(not (m.isfile() or m.islnk()) or (m.name != 'checkpoint.json' and not permitted(m.name)) for m in members):
                raise ValueError('checkpoint contains an unsafe path or nonregular file')
            header = archive.getmember('checkpoint.json')
            if not header.isfile() or header.size > 4000000:
                raise ValueError('checkpoint manifest is invalid or too large')
            manifest = json.load(archive.extractfile('checkpoint.json'))
            if manifest.get('version') not in {1, 2} or set(manifest['files']) != set(names) - {'checkpoint.json'}:
                raise ValueError('checkpoint manifest does not match its files')
            sizes = [entry['size'] for entry in manifest['files'].values()]
            if any(isinstance(n, bool) or not isinstance(n, int) or n < 0 for n in sizes) or sum(sizes) > MAX_EXPANDED_BYTES:
                raise ValueError('checkpoint exceeds its expanded byte bound')
            regular = set()
            for member in members:
                if member.name == 'checkpoint.json':
                    continue
                path = stage / member.name
                path.parent.mkdir(parents=True, exist_ok=True)
                entry = manifest['files'][member.name]
                if member.islnk():
                    if (manifest['version'] != 2 or member.linkname not in regular or not permitted(member.linkname)
                            or manifest['files'][member.linkname] != entry):
                        raise ValueError('checkpoint hardlink is not a verified internal duplicate')
                    # Copy rather than linking restored files: editing one creative
                    # must never change another file with identical original bytes.
                    shutil.copyfile(stage / member.linkname, path)
                else:
                    with archive.extractfile(member) as stream, path.open('wb') as out:
                        shutil.copyfileobj(stream, out)
                    regular.add(member.name)
                if entry['size'] != path.stat().st_size or entry['sha256'] != assets.sha256(path):
                    raise ValueError('checkpoint checksum mismatch')
        database = stage / 'local/engine.sqlite3'
        if database.exists():
            with closing(sqlite3.connect(database)) as db:
                if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                    raise ValueError('checkpoint ledger failed SQLite integrity check')
        # Verification completes before existing state is touched. Keep replaced
        # state as a recovery copy until the operator removes it.
        local = root / 'local'; local.mkdir(exist_ok=True)
        recovery = local / 'backups' / ('before-restore-' + uuid.uuid4().hex)
        if replace:
            recovery.mkdir(parents=True)
            for path in targets + [local / 'engine.sqlite3-wal', local / 'engine.sqlite3-shm']:
                if path.exists():
                    path.rename(recovery / path.name)
        for name in DIRECTORIES | {'engine.sqlite3'}:
            path = stage / 'local' / name
            if path.exists():
                path.rename(local / name)
    return {'restored_files': len(manifest['files']), 'recovery_copy': str(recovery.relative_to(root)) if replace else None}
