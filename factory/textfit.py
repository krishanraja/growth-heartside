"""Text fitting with no font files or assets, so the lock tests can run anywhere."""
import itertools, re

EMOJI_RE = re.compile('([\U0001F300-\U0001FAFF\u2600-\u27bf\u2615])')


def runs(text):
    return [p for p in EMOJI_RE.split(text) if p]


def text_width(d, text, font, size):
    w = 0
    for p in runs(text):
        if EMOJI_RE.fullmatch(p):
            w += size + 6
        else:
            w += d.textlength(p, font=font)
    return w


def wrap_rich(d, text, font, size, maxw):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if text_width(d, t, font, size) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def balanced_wrap(d, text, font, maxw, size=46):
    """Wrap to the fewest lines that fit, with line widths as even as possible, and never one
    word alone on the last line (Krish, 2 Nov: a lone "too" on its own line "looks shitty")."""
    words = text.split(' '); n = len(words)
    width = lambda s: text_width(d, s, font, size)
    if width(text) <= maxw:
        return [text]
    for k in range(2, min(n, 7) + 1):
        best = None
        for cuts in itertools.combinations(range(1, n), k - 1):
            b = (0,) + cuts + (n,)
            if n > 2 and b[-1] - b[-2] == 1:
                continue
            lines = [' '.join(words[b[i]:b[i + 1]]) for i in range(k)]
            ws = [width(l) for l in lines]
            if max(ws) > maxw:
                continue
            score = max(ws) - min(ws)
            if best is None or score < best[0]:
                best = (score, lines)
        if best:
            return best[1]
    return wrap_rich(d, text, font, size, maxw)


def lone_word(lines):
    return len(lines) > 1 and len(lines[-1].split()) == 1 and len(' '.join(lines).split()) > 2


