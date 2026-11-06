"""Asset-independent layout helpers for the social UI house profile.

Existing locked masters use their legacy renderer until a new spec explicitly
opts into this profile. New concepts and variants use it by default.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.creative_ui import CRITICAL, SUBTITLES, MAX_CHAT_MESSAGES, REVISION


def enabled(spec, locked=None, fingerprint=None):
    profile = spec.get('ui_profile')
    if profile is not None and profile != REVISION:
        raise ValueError('unknown ui_profile; use ' + REVISION)
    if profile:
        return True
    return not (locked and locked.get('status') == 'locked'
                and spec.get('id') == locked.get('id')
                and fingerprint == locked.get('fingerprint'))


def caption(image, text, font, y=None):
    if not text:
        return image
    left, top, right, bottom = SUBTITLES
    top = top if y is None else y
    draw = ImageDraw.Draw(image, 'RGBA')
    width = right - left - 48
    # A two-line caption needs only one split. Avoid the legacy combinatorial
    # multi-line wrapper on long wording: fail promptly, then split the beat.
    words = text.split()
    if draw.textlength(text, font=font) <= width:
        lines = [text]
    else:
        choices = []
        for cut in range(1, len(words)):
            pair = [' '.join(words[:cut]), ' '.join(words[cut:])]
            widths = [draw.textlength(line, font=font) for line in pair]
            if max(widths) <= width and (len(words) <= 2 or len(words) - cut > 1):
                phrase_end = words[cut - 1].endswith(('.', '?', '!', ',', ';', ':'))
                choices.append(((0 if phrase_end else 1, abs(widths[0] - widths[1])), pair))
        if not choices:
            raise ValueError('split the caption beat: wording exceeds two readable lines')
        lines = min(choices, key=lambda choice: choice[0])[1]
    height = len(lines) * 64 + 32
    if len(lines) > 2 or not CRITICAL[1] <= top < top + height <= CRITICAL[3]:
        raise ValueError('split the caption beat: at most two readable lines inside the tested content region')
    # Opaque background gives stable text contrast even over the busiest frame.
    draw.rounded_rectangle((left, top, right - 1, top + height - 1), 20, fill=(20, 18, 15, 255))
    for index, line in enumerate(lines):
        if draw.textlength(line, font=font) > right - left - 48:
            raise ValueError('caption word exceeds the working region; rewrite, do not shrink')
        draw.text(((left + right - draw.textlength(line, font=font)) / 2,
                   top + 10 + index * 64), line, font=font, fill='white')
    return image


def recent_blocks(blocks, top=510, bottom=1152, gap=22):
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


def chat_screen(blocks, title, avatars, title_font, small_font, paper):
    image = Image.new('RGB', (1080, 1920), paper)
    draw = ImageDraw.Draw(image)
    left, top, right, _ = CRITICAL
    draw.rounded_rectangle((left, top, right, 480), 24, fill=(71, 61, 52))
    if draw.textlength(title, font=title_font) > right - left - 40:
        raise ValueError('shorten the chat title to fit the content region')
    draw.text(((left + right - draw.textlength(title, font=title_font)) / 2, 304), title, font=title_font, fill=paper)
    for i, avatar in enumerate(avatars):
        avatar = avatar.resize((58, 58))
        image.paste(avatar, (int((left + right) / 2 - len(avatars) * 30 + i * 60), 374), avatar)
    label = 'Fictional dog chat'
    draw.text(((left + right - draw.textlength(label, font=small_font)) / 2, 440), label, font=small_font, fill=paper)
    for block, y in recent_blocks(blocks):
        if block.width > right - left:
            raise ValueError('chat block crosses the action-rail working boundary')
        image.paste(block, (left, y), block)
    # No pretend input field, notifications, platform controls or engagement counts.
    return image
