"""Check a listing of Heartside's Drive against config/drive-map.json.

Krish, 2026-11-09: "Make sure the drive is completely up to date and not able to be corrupted or sprawled, and that
everything is automatically managed in Google Drive without you having to say so." No runner here holds Drive
credentials, so a session with the Drive connector lists the folders (docs/DRIVE-MAP.md, "Auditing") and this
checks the listing deterministically. Errors break the map and fail the audit; warnings are drift Krish should see.

A listing is a JSON array of Drive items as the connector returns them: id, title, mimeType, parentId.
"""
import re

FOLDER = 'application/vnd.google-apps.folder'


def audit(drive_map, listing):
    folders = drive_map['folders']
    by_id = {i['id']: i for i in listing}
    children = {}
    for item in listing:
        children.setdefault(item.get('parentId'), []).append(item)
    post_ids = {i['id'] for i in children.get(next(k for k, v in folders.items() if v['rule'] == 'posts'), []) if i['mimeType'] == FOLDER}
    sessions_root = next(k for k, v in folders.items() if v['rule'] == 'sessions')
    session_ids = {i['id'] for i in children.get(sessions_root, []) if i['id'] not in folders}
    posts_path = next(v['path'] for v in folders.values() if v['rule'] == 'posts')
    problems = []

    def err(where, what):
        problems.append(f'ERROR {where}: {what}')

    def warn(where, what):
        problems.append(f'WARN  {where}: {what}')

    for item in listing:
        parent, title, is_folder = item.get('parentId'), item['title'], item['mimeType'] == FOLDER
        rule = folders.get(parent, {}).get('rule')
        base = folders.get(parent, {}).get('path') or (posts_path + '/' + by_id[parent]['title'] if parent in post_ids else
                (folders[sessions_root]['path'] + '/' + by_id[parent]['title'] if parent in session_ids else str(parent)))
        where = base + '/' + title
        if item['id'] in folders and folders[item['id']]['path'].rsplit('/', 1)[-1] != title:
            warn(folders[item['id']]['path'], f'the folder is now named "{title}"; update config/drive-map.json and docs/DRIVE-MAP.md')
        if rule == 'schedule':
            if not any(re.search(p, title) for p in drive_map['schedule_files']):
                err(where, 'not a file the map allows in 03b_Social-Schedule (README, posting strategy, 02 Schedule Sheets, weekly placement review, Posts)')
        elif rule == 'posts':
            if not is_folder:
                err(where, 'a loose file in Posts/; media goes in Posts/<post id>/')
            elif not re.search(drive_map['post_id'], title):
                err(where, 'a Posts folder must be named by its post id, like F28 or F06-frenchie')
        elif parent in post_ids:
            folder = by_id[parent]['title']
            m = re.search(drive_map['post_file'], title)
            if is_folder:
                err(where, 'no subfolders inside a post folder')
            elif not m:
                err(where, 'not heartside_<id>_<slug>_<reel|cover|slide1-5>.<mp4|jpg>; sources and drafts go in a 03a session folder')
            elif m['id'] != folder:
                err(where, f'filed under {folder} but named for {m["id"]}')
            elif drive_map['kind_ext'][re.sub(r'\d', '', m['kind'])] != m['ext']:
                err(where, f'a {m["kind"]} must be .{drive_map["kind_ext"][re.sub(r"[0-9]", "", m["kind"])]}')
            elif re.search(r'(^|-)(v\d+|final|copy|new)(-|$)', m['slug']):
                warn(where, 'a versioned slug; a changed version keeps its name and is sent again')
        elif rule == 'sessions':
            if not is_folder:
                err(where, 'a loose file at the top of 03a; it belongs inside a dated session folder')
            elif item['id'] not in folders and not re.search(drive_map['session_folder'], title):
                err(where, 'a 03a folder must be YYYY-MM-DD_<Engine|Codex|Claude>-<Topic>')
            elif item['id'] not in folders and not title.startswith('Failed - ') and not re.search(drive_map['new_session_folder'], title):
                warn(where, 'a new session folder names its maker: YYYY-MM-DD_<Engine|Codex|Claude>-<Topic>')
    for sid in session_ids:
        kids = children.get(sid)
        if kids is not None and not any(re.search(drive_map['session_readme'], k['title']) for k in kids):
            err(folders[sessions_root]['path'] + '/' + by_id[sid]['title'], 'no START-HERE.md at its top')
    for pid in post_ids:
        slugs = {m['slug'] for k in children.get(pid, []) if (m := re.search(drive_map['post_file'], k['title']))}
        if len(slugs) > 1:
            warn(posts_path + '/' + by_id[pid]['title'], f'{len(slugs)} slugs in one post ({", ".join(sorted(slugs))}); every file of a post shares one slug')
    elsewhere = drive_map.get('elsewhere', {})

    def under_heartside(item):
        seen = set()
        while item and item['id'] not in seen:
            if item['id'] in folders or item.get('parentId') in folders or item['id'] in elsewhere or item.get('parentId') in elsewhere:
                return True
            seen.add(item['id'])
            item = by_id.get(item.get('parentId'))
        return False

    for item in listing:
        if not under_heartside(item) and re.search(drive_map['heartside_names'], item['title']):
            err(item['title'], f'a Heartside file outside the Heartside folder (parent {item.get("parentId")}); move it to the folder the map names')
    return problems
