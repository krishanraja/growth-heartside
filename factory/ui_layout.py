"""Asset-independent layout helpers for the house corpus profile (engine/creative_ui.py).

Every helper draws inside the corpus regions and can record what it drew in a `Layout`, the manifest
`lock.py media` checks. A spec that declares `ui_profile` (or a new spec with no exact legacy lock) uses
this profile; an exact legacy lock without one renders its old geometry, which cannot pass the gate.
"""
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.creative_ui import segments  # noqa: F401  (shared with engine/media.py)
from engine.creative_ui import (CRITICAL, SUBTITLES, HOOK, LOGO, MAX_CHAT_MESSAGES, REVISION, LEGACY, FEED_MARGIN,
                                CAPTION_LINES, CAPTION_WORDS, CAPTION_LINE_HEIGHT, END_HOLD,
                                TIKTOK_PHOTO_BACKGROUND, TIKTOK_PHOTO_TEXT)

CHAT_HEADER = (CRITICAL[0], CRITICAL[1], CRITICAL[2], CRITICAL[1] + 160)
CHAT_TOP = CHAT_HEADER[3] + 14          # the first message line under the header
CHAT_FLOOR = CRITICAL[3]                # the newest message ends above the bottom metadata (corpus 3.5)
CHAT_WIDTH = CRITICAL[2] - CRITICAL[0]  # avatar plus bubble, left of the action rail


class Layout:
    """What a renderer drew: role, box, time span and words. Written beside the media as layout.json."""

    def __init__(self, canvas=(1080, 1920), profile=REVISION):
        self.canvas, self.profile, self.elements, self.duration, self.ending = list(canvas), profile, [], 0.0, None
        self.media_sha256 = None

    def add(self, role, box, start, end, text=None, **extra):
        e = {'role': role, 'box': [round(v, 1) for v in box], 'start': round(start, 3), 'end': round(end, 3)}
        if text:
            e['text'] = text
        e.update(extra)
        self.elements.append(e)
        return e

    def data(self):
        out = {'profile': self.profile, 'canvas': self.canvas, 'duration': round(self.duration, 3), 'elements': self.elements}
        if self.ending:
            out['ending'] = self.ending
        if self.media_sha256:
            out['media_sha256'] = self.media_sha256
        return out

    def save(self, path):
        Path(path).write_text(json.dumps(self.data(), indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
        return path


def end_hold(spec_hold):
    """The product end beat: at least 3 s (Krish's floor endings-land), at most 4 s (no dead outro)."""
    return min(max(float(spec_hold), END_HOLD[0]), END_HOLD[1])


def photo_card(photo, text, font, platform, lines=None):
    """Compose source photos with editable type and visible native controls.

    The caller supplies a clean photo crop; this never generates/repaints it.
    TikTok's empty top/right/bottom regions use ink for its white controls.
    """
    if platform not in ('feed', 'tiktok'):
        raise ValueError('photo card platform must be feed or tiktok')
    vertical = platform == 'tiktok'
    height = 1920 if vertical else 1350
    left, right = (CRITICAL[0], CRITICAL[2]) if vertical else (FEED_MARGIN, 1080 - FEED_MARGIN)
    width = right - left
    bg, fg = (TIKTOK_PHOTO_BACKGROUND, TIKTOK_PHOTO_TEXT) if vertical else (TIKTOK_PHOTO_TEXT, TIKTOK_PHOTO_BACKGROUND)
    canvas = Image.new('RGB', (1080, height), bg)
    draw = ImageDraw.Draw(canvas)
    if lines is None:
        lines, line = [], ''
        for word in text.split():
            trial = (line + ' ' + word).strip()
            if draw.textlength(trial, font=font) > width and line:
                lines.append(line); line = word
            else:
                line = trial
        if line:
            lines.append(line)
    if ' '.join(lines) != ' '.join(text.split()) or len(lines) > 4 or any(draw.textlength(line, font=font) > width for line in lines):
        raise ValueError('photo wording must fit four readable lines without changing words')
    top = HOOK[1] if vertical else FEED_MARGIN
    for i, line in enumerate(lines):
        draw.text(((left + right) / 2 - draw.textlength(line, font=font) / 2, top + i * 64), line, font=font, fill=fg)
    photo_top = top + len(lines) * 64 + 36
    area = (left, photo_top, right, CRITICAL[3]) if vertical else (FEED_MARGIN, photo_top, 1080 - FEED_MARGIN, 1350 - FEED_MARGIN)
    fitted = ImageOps.contain(photo, (area[2] - area[0], area[3] - area[1]), Image.Resampling.LANCZOS)
    canvas.paste(fitted, (round((area[0] + area[2] - fitted.width) / 2), area[1]))
    return canvas


def enabled(spec, locked=None, fingerprint=None):
    profile = spec.get('ui_profile')
    if profile is not None and profile != REVISION and profile not in LEGACY:
        raise ValueError('unknown ui_profile; use ' + REVISION)
    if profile:
        return True
    # An exact legacy lock with no profile renders its old geometry, which the gate holds.
    # Never reinterpret a known master or a matching legacy slot variant silently.
    return not (locked and locked.get('status') == 'locked'
                and (spec.get('id') == locked.get('id')
                     or fingerprint == locked.get('fingerprint')))


def caption_lines(draw, text, font, width):
    """One line, or the best two-line split at a phrase end; raises when it needs more."""
    words = text.split()
    if draw.textlength(text, font=font) <= width:
        return [text]
    choices = []
    for cut in range(1, len(words)):
        pair = [' '.join(words[:cut]), ' '.join(words[cut:])]
        widths = [draw.textlength(line, font=font) for line in pair]
        if max(widths) <= width and (len(words) <= 2 or len(words) - cut > 1):
            phrase_end = words[cut - 1].endswith(('.', '?', '!', ',', ';', ':'))
            choices.append(((0 if phrase_end else 1, abs(widths[0] - widths[1])), pair))
    if not choices:
        raise ValueError('split the caption beat: wording exceeds two readable lines')
    return min(choices, key=lambda choice: choice[0])[1]


def caption(image, text, font, y=None, layout=None, start=0.0, end=0.0):
    if not text:
        return image
    left, top, right, bottom = SUBTITLES
    top = top if y is None else y
    draw = ImageDraw.Draw(image, 'RGBA')
    width = right - left - 48
    lines = caption_lines(draw, text, font, width)
    height = len(lines) * CAPTION_LINE_HEIGHT + 32
    if len(lines) > CAPTION_LINES or not CRITICAL[1] <= top < top + height <= CRITICAL[3]:
        raise ValueError('split the caption beat: at most two readable lines inside the tested content region')
    # Opaque background gives stable text contrast even over the busiest frame.
    draw.rounded_rectangle((left, top, right - 1, top + height - 1), 20, fill=(20, 18, 15, 255))
    for index, line in enumerate(lines):
        if draw.textlength(line, font=font) > right - left - 48:
            raise ValueError('caption word exceeds the working region; rewrite, do not shrink')
        draw.text(((left + right - draw.textlength(line, font=font)) / 2,
                   top + 10 + index * CAPTION_LINE_HEIGHT), line, font=font, fill='white')
    if layout is not None:
        layout.add('subtitle', (left, top, right, top + height), start, end, text, lines=len(lines),
                   px=getattr(font, 'size', None))
    return image


def caption_y(y, lines=2):
    """A spec's cap_y, kept inside the critical box (subtitles may move to protect a face)."""
    height = lines * CAPTION_LINE_HEIGHT + 32
    if y is None:
        return SUBTITLES[1]
    return min(max(int(y), CRITICAL[1]), CRITICAL[3] - height)


def chat_blocks(blocks, top=CHAT_TOP, bottom=CHAT_FLOOR, gap=18):
    """A chat builds as a real one does (Krish, 10 Nov): newest at the bottom, earlier messages stacked
    above it, the oldest sliding up under the header and cut off by it, as in WhatsApp. No cap."""
    if blocks and blocks[-1].height > bottom - top:
        raise ValueError('chat message is too tall; split it into another beat')
    positioned, y = [], bottom
    for block in reversed(blocks):
        y -= block.height
        if y + block.height <= top:
            break
        positioned.append((block, y))
        y -= gap
    return list(reversed(positioned))


def recent_blocks(blocks, top=CHAT_TOP, bottom=CRITICAL[3], gap=22):
    """Newest payoff must fit; never silently disappear below the native UI."""
    visible, room = [], bottom - top
    for block in reversed(blocks[-MAX_CHAT_MESSAGES:]):
        if block.height + gap > room:
            if not visible:
                raise ValueError('chat message is too tall; split it into another beat')
            break
        visible.append(block)
        room -= block.height + gap
    y = top + room // 2
    positioned = []
    for block in reversed(visible):
        positioned.append((block, y))
        y += block.height + gap
    return positioned


def chat_screen(blocks, title, avatars, title_font, small_font, paper, layout=None, start=0.0, end=0.0, texts=None):
    image = Image.new('RGB', (1080, 1920), paper)
    draw = ImageDraw.Draw(image)
    left, top, right, bottom = CHAT_HEADER
    draw.rounded_rectangle((left, top, right, bottom), 24, fill=(71, 61, 52))
    if draw.textlength(title, font=title_font) > right - left - 40:
        raise ValueError('shorten the chat title to fit the content region')
    draw.text(((left + right - draw.textlength(title, font=title_font)) / 2, top + 16), title, font=title_font, fill=paper)
    for i, avatar in enumerate(avatars):
        avatar = avatar.resize((58, 58))
        image.paste(avatar, (int((left + right) / 2 - len(avatars) * 30 + i * 60), top + 64), avatar)
    label = 'Fictional dog chat'
    draw.text(((left + right - draw.textlength(label, font=small_font)) / 2, top + 120), label, font=small_font, fill=paper)
    if layout is not None:
        layout.add('title', CHAT_HEADER, start, end, title)
    for index, (block, y) in enumerate(chat_blocks(blocks)):
        if block.width > CHAT_WIDTH:
            raise ValueError('chat block crosses the action-rail working boundary')
        if y < CHAT_TOP:   # scrolled up under the header: show only what is still below it
            block = block.crop((0, CHAT_TOP - y, block.width, block.height)); y = CHAT_TOP
        image.paste(block, (left, y), block)
        if layout is not None:
            box = block.getbbox() or (0, 0, 1, 1)
            layout.add('chat', (left + box[0], y + box[1], left + box[2], y + box[3]), start, end)
    # No pretend input field, notifications, platform controls or engagement counts.
    return image
