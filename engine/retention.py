"""Bound hot media storage; preserve all ledger/evidence metadata.

The default checkpoint is a rolling seven-day production workspace, not a
permanent media archive. Saved creator lists and arbitrary local files are never
touched. Keep long-term publication masters in licensed private storage separately.
"""
import datetime as dt
import json
from pathlib import Path
import re
import shutil

from . import assets


def prune(root, today, days=7):
    cutoff = dt.date.fromisoformat(today) - dt.timedelta(days=days - 1)
    removed = []
    runs = Path(root) / 'local/automation/runs'
    if runs.exists():
        for directory in runs.iterdir():
            if directory.is_dir() and re.fullmatch(r'\d{4}-\d{2}-\d{2}', directory.name):
                if dt.date.fromisoformat(directory.name) < cutoff:
                    shutil.rmtree(directory); removed.append(str(directory.relative_to(root)))
    media = Path(root) / 'local/media'
    if media.exists():
        for creative in media.iterdir():
            match = re.fullmatch(r'(?:IG|FB|TT|PIN)_[A-Z]+_(?:REEL|STORY|PIN)_C\d+_H\d+_V\d+_(\d{8})', creative.name)
            if creative.is_dir() and not creative.is_symlink() and match:
                date = dt.datetime.strptime(match[1], '%Y%m%d').date()
                if date < cutoff:
                    shutil.rmtree(creative); removed.append(str(creative.relative_to(root)))
    return {'hot_media_days': days, 'removed_paths': removed, 'ledger_metadata_deleted': False}
