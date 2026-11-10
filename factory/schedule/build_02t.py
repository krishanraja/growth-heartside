"""Build 02t (10 Nov): photo posts as videos with licensed Epidemic music built in.

Krish, 10 Nov: "try having them all be posted/postable with music - even the stills. ideally you do that by finding
music in epidemic, but if the payoff of the humour is actually a specific song, we add it to my manual phone posting
board". So every photo post, the seven already in 02r and the eight new ones (F52 to F59), goes out as an 8 s video
with its Epidemic track in it. Codex posts these rows on all three platforms; nothing is added in the app.
Usage: python3 factory/schedule/build_02t.py 02r.csv shas.json out.csv
"""
import csv, json, sys

TRACKS = {  # post: (title, artist, epidemic id)
    'F30-pepper': ('Sneaky Business', 'J.R. Productions', '8e1d93c8-9023-4371-9492-9ba9b562330e'),
    'F31': ('Christmas Magic', 'Megan Wofford', '5128d3e7-4855-4d7c-bc80-b327dde76c49'),
    'F32': ('Ghost in the Attic', 'The Fly Guy Five', '6af1f2a2-984f-4073-a6f8-06bac73dace9'),
    'F33': ('Sneaking Around', 'Guto Lucena', 'c1b99978-a8f0-41cf-a0f2-8a25dfc6317a'),
    'F35': ('Mr Attitude', 'Stationary Sign', '833c4195-d826-4462-8398-8b98c3e2bc09'),
    'F36': ('In Disguise', 'The Fly Guy Five', '20470259-69bc-444e-bc8e-01066aed76ca'),
    'F37': ('Tiny Trot', 'Speedy The Spider', '5e2b4a5e-c7ad-4192-b83e-d1dc906e5d48'),
    'F53': ('One Step Away', 'Dian Shuai', '2dfb0d5d-7d3c-43cb-8216-e76cec2f9b6b'),
    'F52': ('Moving Up', 'Origo', '72ead9c2-60c5-4e9f-9f5d-bbdb4aeaaca3'),
    'F54': ('Success Story', 'Lukas Got Lucky', '44ba240a-836b-4b49-a019-97e1ba62ddb9'),
    'F55': ('All I Want for Christmas Is an Analog Synth', 'pär', '2110b4f5-5dfa-4197-b5f6-9939655611e8'),
    'F56': ('Mabel (Instrumental Version)', 'Clara Mendes', '481ce8c1-fad2-4f2d-9fb6-c123914a853a'),
    'F57': ('Härlig Är Jorden (Organ Version)', 'Kurt Lyndon', '78ed1bfc-11b8-3a90-a11f-bf294494c1c7'),
    'F58': ('The Blue Tiger', 'Guto Lucena', '5079b22e-9a59-4ad6-b530-933d44b82529'),
    'F59': ("I Can't See", 'Lennon Hutton', '1f45db8f-506d-4f62-a026-4e25c2be1994'),
}
SRC = {'F52': 'P2', 'F53': 'P1', 'F54': 'P3', 'F55': 'P4', 'F56': 'P5', 'F57': 'P6', 'F58': 'P7', 'F59': 'P11'}
NEW = {  # post: (date, time, slug, caption first line, hashtags)
    'F52': ('2026-11-18', '8:00', 'reports-to-the-cat', 'Effective immediately, the cat runs this department. He has been asked to support the transition 💀', '#labrador #catsanddogs #dogsof{p} #corporatelife'),
    'F53': ('2026-11-18', '12:30', 'mostly-a-floor-dog', 'The rule is no dogs on the sofa. He has read the rule very carefully.', '#labrador #dogrules #dogsof{p} #sofadog'),
    'F58': ('2026-11-19', '8:00', 'cheese-witness', '2 AM. Fridge open. Witness present 💀', '#beagle #midnightsnack #dogsof{p} #cheese'),
    'F54': ('2026-11-19', '12:30', 'portion-escalated', 'He was told it is the same amount as yesterday. He has requested the minutes.', '#beagle #dinnertime #dogsof{p} #hungrydog'),
    'F59': ('2026-11-20', '8:00', 'vacuum-not-plugged-in', 'Bravest dog in the house, unless the vacuum is in the room. It does not need to be on.', '#bernesemountaindog #scaredydog #dogsof{p} #vacuum'),
    'F56': ('2026-11-23', '12:30', 'guest-room-review', 'Guests arrive Wednesday. He has already checked in.', '#goldenretriever #guestroom #dogsof{p} #thanksgiving'),
    'F57': ('2026-11-26', '10:00', 'saying-grace', 'Happy Thanksgiving. He was thankful for about four seconds.', '#beagle #thanksgiving #dogsof{p} #turkey'),
    'F55': ('2026-11-28', '12:30', 'christmas-photo-take-41', 'Forty-one takes. He has made his position clear.', '#beagle #christmasphoto #dogsof{p} #matchingpajamas'),
}
TAIL = 'Gifts from your dog. Painted lovingly in your style of choice using our next-generation AI artists.'
PLAT = [('tiktok', 0, 'TT', 'tiktok'), ('instagram', 5, 'IG', 'instagram'), ('facebook', 10, 'FB', None)]


def plus(t, m):
    h, mi = map(int, t.split(':')); mi += m
    return f'{h + mi // 60}:{mi % 60:02d}'


def note(pid, sha, size):
    t, a, i = TRACKS[pid]
    return (f'BAKED MUSIC: the licensed Epidemic Sound track "{t}" by {a} (recording {i}) is built into the video. '
            'Post the video as it is on every platform, with no sound added in the app and the original audio at 100. '
            'Never post this row through the phone list; Codex posts it. '
            f'Media: sha256 {sha}, {size} bytes. Approved stays Krish\'s to mark.')


def main(src, shas, out):
    sh = json.load(open(shas))
    rows = list(csv.reader(open(src, encoding='utf-8')))
    head, body = rows[0], rows[1:]
    i = {k: n for n, k in enumerate(head)}
    new = []
    for r in body:  # the seven existing photo posts, same slots, video media
        pid = r[i['post_id']]
        if pid not in TRACKS:
            continue
        r = list(r)
        base = r[i['media_files']].rsplit('_slide1.jpg', 1)[0]
        r[i['media_files']], r[i['cover']] = base + '_music_reel.mp4', base + '_music_cover.jpg'
        r[i['format']] = 'REEL'
        r[i['creative_id']] = r[i['creative_id']].replace('_POST_', '_REEL_').replace('_V1_', '_V2_')
        r[i['lock_fingerprint']] = sh[pid][0][:16]
        if r[i['platform']] == 'facebook':
            cid = r[i['creative_id']]
            old = r[i['link']]
            link = old.split('&utm_content=')[0].replace('organic_social', 'organic_video') + '&utm_content=' + cid
            r[i['link']] = link
            r[i['caption']] = r[i['caption']].replace(old, link)
        r[i['notes']] = note(pid, *sh[pid])
        r[i['approved']] = ''
        new.append(r)
    n = 170
    for pid, (d, t, slug, line, tags) in NEW.items():
        n += 1
        for plat, off, code, tagp in PLAT:
            cid = f'{code}_ENT_REEL_C{n}_H01_V1_{d.replace("-", "")}'
            row = [''] * len(head)
            hh, mm = plus(t, off).split(':')
            row[i['slot']] = f'{d}_{int(hh):02d}:{mm}_{plat}'
            row[i['date_ET']], row[i['time_ET']], row[i['platform']] = d, plus(t, off), plat
            row[i['post_id']], row[i['format']] = pid, 'REEL'
            row[i['media_files']] = f'heartside_{pid}_{slug}_music_reel.mp4'
            row[i['cover']] = f'heartside_{pid}_{slug}_music_cover.jpg'
            if plat == 'facebook':
                link = ('https://heartside.io?utm_source=facebook&utm_medium=organic_video&utm_campaign=hs_growth_202611'
                        f'&utm_content={cid}')
                row[i['caption']], row[i['link']] = f'{line}\n\n{TAIL}\n{link}', link
            else:
                row[i['caption']] = f'{line}\n\n{TAIL} Link in bio.\n\n{tags.format(p=tagp)}'
                row[i['link']] = 'link in bio'
            row[i['creative_id']] = cid
            row[i['lock_fingerprint']] = sh[pid][0][:16]
            row[i['notes']] = note(pid, *sh[pid])
            new.append(row)
    new.sort(key=lambda r: (r[i['date_ET']], int(r[i['time_ET']].split(':')[0]) * 60 + int(r[i['time_ET']].split(':')[1])))
    w = csv.writer(open(out, 'w', encoding='utf-8', newline=''))
    w.writerow(head)
    w.writerows(new)
    print(len(new), 'rows')


if __name__ == '__main__':
    main(*sys.argv[1:4])
