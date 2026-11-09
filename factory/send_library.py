"""Send finished posts to Heartside's social library on Drive, through the home-computer lane.

Krish, 2026-11-03: "You also can queue stuff for the home computer to upload in the right place",
then "Why don't you duplicate that Python script for Heartside then? We're going to need to do a lot
more of this type of stuff moving forward." He chose to add Heartside to content-engine's library lane
(krishanraja/content-engine, scripts/post-pack/send.py): each file goes to the engine's private
library, and his always-on machine writes it into Heartside/05_Social-Library/Posts/<post id>/ within
about ten minutes, where Codex posts what he approves.

    python3 factory/send_library.py LIBRARY_DIR [--dry-run] [--only F01,F02]

LIBRARY_DIR holds the media and manifest.json: [{"post", "file", "bytes", "sha256"}, ...], as the
library build writes it. Every file is checked against its manifest sha256 and size before anything is
sent; one mismatch and nothing is sent. Paths follow the lane's Heartside rule: Posts/<post id>/<file>,
the id like F01 or F06-frenchie (content-engine config/library-paths.cases.json). A file the library
already holds is skipped. Sending never posts anything: Codex posts only rows Krish approved (in the Sheet, or in chat recorded in notes).

The engine key is ENGINE_OPERATOR_TOKEN, else MINDMAKE_ENGINE_TOKEN, else Windows Credential Manager
`Mindmake/engine-operator-token` (the home computers' store, as content-watcher reads it); never printed; the address is ENGINE_BASE_URL, else the
engine's own.
"""
import argparse, hashlib, json, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path
from urllib.parse import urlsplit

BASE = os.environ.get('ENGINE_BASE_URL', 'https://content-engine-flame-nu.vercel.app').rstrip('/')
LIBRARY = 'heartside'
POST_ID = re.compile(r'[A-Z][0-9]{2,3}(?:-[a-z0-9]+)*')
NAME = re.compile(r'[A-Za-z0-9][A-Za-z0-9._ ()-]{0,98}')
KINDS = {'review-reel': 'a candidate for Krish to review: never posted', 'review-cover': 'a candidate cover for review: never posted',
         'paid-reel': 'a paid cut (mp4), run only under docs/PAID-BOOSTS.md', 'paid-cover': 'the paid cut\'s cover',
         'reel': 'the reel (mp4)', 'cover': 'the cover, used as the thumbnail', 'slide': 'a carousel slide, in order'}
WAITS = (2, 4, 8, None)


def _windows_credential(target):
    """The home computers keep the engine key in Windows Credential Manager (content-watcher secrets.py)."""
    if sys.platform != 'win32':
        return None
    import ctypes
    from ctypes import wintypes

    class CREDENTIAL(ctypes.Structure):
        _fields_ = [('Flags', wintypes.DWORD), ('Type', wintypes.DWORD), ('TargetName', wintypes.LPWSTR),
                    ('Comment', wintypes.LPWSTR), ('LastWritten', wintypes.FILETIME),
                    ('CredentialBlobSize', wintypes.DWORD), ('CredentialBlob', ctypes.POINTER(ctypes.c_ubyte)),
                    ('Persist', wintypes.DWORD), ('AttributeCount', wintypes.DWORD), ('Attributes', ctypes.c_void_p),
                    ('TargetAlias', wintypes.LPWSTR), ('UserName', wintypes.LPWSTR)]
    advapi32 = ctypes.WinDLL('advapi32', use_last_error=True)
    pointer = ctypes.POINTER(CREDENTIAL)()
    if not advapi32.CredReadW(target, 1, 0, ctypes.byref(pointer)):
        return None
    try:
        blob = ctypes.string_at(pointer.contents.CredentialBlob, pointer.contents.CredentialBlobSize)
    finally:
        advapi32.CredFree(pointer)
    for enc in ('utf-16-le', 'utf-8'):
        try:
            value = blob.decode(enc).strip('\x00').strip()
        except UnicodeDecodeError:
            continue
        if value and value.isprintable():
            return value
    return None


def engine_key():
    return (os.environ.get('ENGINE_OPERATOR_TOKEN') or os.environ.get('MINDMAKE_ENGINE_TOKEN')
            or _windows_credential('Mindmake/engine-operator-token'))


class SendError(Exception):
    pass


def digests(path):
    sha, md5 = hashlib.sha256(), hashlib.md5()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            sha.update(chunk); md5.update(chunk)
    return sha.hexdigest(), md5.hexdigest()


def purpose(post, name):
    kind = next((words for key, words in KINDS.items() if f'_{key}' in name), 'a file of the post')
    return f'Heartside post {post}: {kind}. Codex posts it only when Krish has approved its row.'


def plan(folder, only=None):
    """[(library path, Path, sha256, md5, bytes, purpose)], every file checked first."""
    folder = Path(folder)
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    planned, problems = [], []
    for item in manifest:
        post, name = item['post'], item['file']
        if only and post not in only:
            continue
        if not POST_ID.fullmatch(post) or not NAME.fullmatch(name) or name.endswith(('.', ' ')):
            problems.append(f'{post}/{name}: not a Heartside library path (Posts/<post id>/<file>)'); continue
        path = folder / name
        if not path.is_file():
            problems.append(f'{name}: missing'); continue
        sha, md5 = digests(path)
        size = path.stat().st_size
        if sha != item['sha256'] or size != item['bytes']:
            problems.append(f'{name}: differs from its manifest (sha256 or size)'); continue
        planned.append((f'Posts/{post}/{name}', path, sha, md5, size, purpose(post, name)))
    if problems:
        raise SendError('nothing was sent, because:\n  ' + '\n  '.join(problems))
    if not planned:
        raise SendError('nothing to send')
    return planned


class Engine:
    def __init__(self):
        self.token = engine_key()
        if not self.token:
            raise SendError('no engine key: set ENGINE_OPERATOR_TOKEN, or store it in Windows Credential Manager as Mindmake/engine-operator-token')

    def post(self, route, body):
        data = json.dumps({**body, 'library': LIBRARY, 'client': 'claude_code'}).encode()
        for wait in WAITS:
            req = urllib.request.Request(BASE + route, data=data, method='POST',
                                         headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'})
            try:
                with urllib.request.urlopen(req, timeout=120) as res:
                    return res.status, json.loads(res.read() or b'{}')
            except urllib.error.HTTPError as err:
                if err.code < 500 or wait is None:
                    try:
                        return err.code, json.loads(err.read() or b'{}')
                    except json.JSONDecodeError:
                        return err.code, {}
            except urllib.error.URLError as err:
                if wait is None:
                    raise SendError(f'the engine could not be reached ({err.reason})')
            time.sleep(wait)

    def put(self, url, path, headers, size):
        parts = urlsplit(url)
        if parts.scheme != 'https' or parts.username or parts.password or not parts.path.startswith('/storage/v1/object/upload/sign/'):
            raise SendError('the engine gave an upload address that is not its signed storage upload: nothing was put')
        for wait in WAITS:
            with open(path, 'rb') as fh:
                req = urllib.request.Request(url, data=fh, method='PUT', headers={**headers, 'Content-Length': str(size)})
                try:
                    with urllib.request.urlopen(req, timeout=600) as res:
                        return res.status
                except urllib.error.HTTPError as err:
                    if err.code < 500 or wait is None:
                        return err.code
                except urllib.error.URLError as err:
                    if wait is None:
                        raise SendError(f'the upload could not reach storage ({err.reason})')
            time.sleep(wait)


def refusal(status, body):
    error = body.get('error') if isinstance(body, dict) else None
    code = error.get('code') if isinstance(error, dict) else error
    reason = error.get('reason') if isinstance(error, dict) else None
    return f'the engine answered {status} ({code or "no code"}{", " + reason if reason else ""})'


def send(planned, engine, out=print):
    done = {'sent': 0, 'already': 0}
    for target, path, sha, md5, size, why in planned:
        status, answer = engine.post('/api/library/upload-url', {'path': target, 'sha256': sha, 'md5': md5, 'bytes': size, 'purpose': why})
        if not (200 <= status < 300 and answer.get('ok') is True):
            raise SendError(f'{target}: {refusal(status, answer)}. Stopped; the files above went in.')
        if answer.get('already_there'):
            done['already'] += 1; out(f'already there  {target}'); continue
        upload = answer.get('upload')
        if upload:
            put = engine.put(upload['url'], path, upload.get('headers') or {}, size)
            if not (200 <= put < 300 or put == 409):
                raise SendError(f'{target}: the upload was refused ({put}). Stopped; the files above went in.')
        status, confirmed = engine.post('/api/library/confirm', {'path': target, 'sha256': sha})
        if not (200 <= status < 300 and confirmed.get('ok') is True):
            raise SendError(f'{target}: {refusal(status, confirmed)}. Stopped; the files above went in.')
        done['sent'] += 1; out(f'sent           {target}  ({size // 1024} KB)')
    return done


def main():
    ap = argparse.ArgumentParser(description='Send finished posts to Heartside/05_Social-Library through the home-computer lane.')
    ap.add_argument('folder', help='the library folder: media plus manifest.json')
    ap.add_argument('--only', help='comma-separated post ids, e.g. F01,F02')
    ap.add_argument('--dry-run', action='store_true', help='check and list, send nothing')
    a = ap.parse_args()
    try:
        planned = plan(a.folder, set(a.only.split(',')) if a.only else None)
        if a.dry_run:
            for target, *_rest, why in planned:
                print(f'{target}\n    {why}')
            print(f'{len(planned)} files checked; nothing was sent.')
            return
        done = send(planned, Engine())
    except SendError as err:
        sys.exit(f'send_library: {err}')
    print(f"Sent {done['sent']}, already there {done['already']}. Krish's always-on machine writes them into "
          'Heartside/05_Social-Library/Posts within about ten minutes.')


if __name__ == '__main__':
    main()
