"""Build 02r from 02q (10 Nov): the one Sheet Codex posts Sprint 120 rows from.

Changes from 02q, on Krish's board answers of 10 Nov:
- F38 and F41 point to the real-dog remakes ("post-F38-real", "post-F41-real": Yes), filed through the library lane.
- F30 is dropped ("decision-F30-real-dog": Yes) and replaced by F30-pepper in the same slots.
- F39 and F45 are left out: Krish asked for real-dog remakes ("Remake all five") and they are not ready.
Usage: python3 factory/schedule/build_02r.py 02q.csv out.csv [pepper_slide_sha256 pepper_bytes]
"""
import csv, sys

REAL = {
    'F38': ('heartside_F38_4am-routine-real_reel.mp4', 'heartside_F38_4am-routine-real_cover.jpg',
            '57189319e0ba5f8a4f17fc016523a6b30ff48385458adb10515cd2879337b38f', 20281013),
    'F41': ('heartside_F41_christmas-shopping-real_reel.mp4', 'heartside_F41_christmas-shopping-real_cover.jpg',
            '9e0daf79586f81a4dfb9bae2decf4a6acc509aecb9185fb2135d7b59889838ba', 14904521),
}
PEPPER_CAPTION = ("The pie was alone for five minutes. Pepper weighs six pounds and cannot reach the table. "
                  "The investigation continues.\n\nGifts from your dog. Painted lovingly in your style of choice "
                  "using our next-generation AI artists.")


def main(src, out, pepper_sha=None, pepper_bytes=None):
    rows = list(csv.reader(open(src, encoding='utf-8')))
    head, body = rows[0], rows[1:]
    i = {k: n for n, k in enumerate(head)}
    new = []
    for r in body:
        pid = r[i['post_id']]
        if pid in ('F39', 'F45'):
            continue
        r = list(r)
        if pid in REAL:
            reel, cover, sha, size = REAL[pid]
            r[i['media_files']], r[i['cover']], r[i['lock_fingerprint']] = reel, cover, sha[:16]
            r[i['notes']] = (r[i['notes']] + f" MEDIA (10 Nov): the real-dog remake Krish approved on his board, reel "
                             f"sha256 {sha}, {size} bytes; same beats, labels, timing and song as before.")
        if pid == 'F30':
            if not pepper_sha:
                continue
            plat = r[i['platform']]
            r[i['post_id']] = 'F30-pepper'
            r[i['media_files']] = r[i['cover']] = 'heartside_F30-pepper_pie-statement_slide1.jpg'
            cid = r[i['creative_id']].replace('C130', 'C160')
            r[i['creative_id']], r[i['lock_fingerprint']] = cid, pepper_sha[:16]
            if plat == 'facebook':
                link = ('https://heartside.io?utm_source=facebook&utm_medium=organic_social&utm_campaign=hs_growth_202611'
                        f'&utm_content={cid}')
                r[i['link']], r[i['caption']] = link, PEPPER_CAPTION + '\n' + link
            else:
                tags = '#thanksgiving #beagle #chihuahua ' + ('#dogsoftiktok' if plat == 'tiktok' else '#dogsofinstagram')
                r[i['link']], r[i['caption']] = 'link in bio', PEPPER_CAPTION.replace(
                    'AI artists.', 'AI artists. Link in bio.') + '\n\n' + tags
            r[i['notes']] = ("NO SONG: a single photo post, no sound to add. Replaces F30 (Krish's board Yes, 10 Nov). Judged 8 (three takes); posts only if Krish types yes on this row. "
                             f"Line on the photo: He has already given a statement. He says it was Pepper. Media: sha256 "
                             f"{pepper_sha}, {pepper_bytes} bytes. Approved stays Krish's to mark.")
        r[i['approved']] = ''
        new.append(r)
    w = csv.writer(open(out, 'w', encoding='utf-8', newline=''))
    w.writerow(head)
    w.writerows(new)
    print(len(new), 'rows')


if __name__ == '__main__':
    main(*sys.argv[1:3], *(sys.argv[3:5] if len(sys.argv) > 4 else []))
