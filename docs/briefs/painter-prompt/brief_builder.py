"""Short directed painting brief built from what Heartside's chat actually sends (v2).

Prototype for a proposal to heartside (its painter prompt is heartside's to change).
Input is only what production knows: the photo, breed, pronoun, the chat's chip ids or typed
answers (home, spot, together), the buyer's toy and accessory, the chosen tone, style and product.

v2 (control test, 29 Oct): with no stated pose and camera the model returns the photo's pose and
one safe "dog by the feet, looking at you" layout, so tone barely showed. Now every tone owns the
staging, the pose and the camera, every style owns its composition, and the pose is always explicit.

Usage: python3 brief_builder.py case.json   (prints the prompt)
"""
import json
import sys

PRON = {"she": ("she", "her", "her"), "he": ("he", "him", "his"), "they": ("they", "them", "their")}
VERB = {"she": ("is", "loves"), "he": ("is", "loves"), "they": ("are", "love")}

STYLE = {  # medium, how it behaves, the composition it owns
    "painterly": ("hand-painted oil painting",
                  "loaded-brush oil, visible directional strokes and impasto, fur built from painted shapes, never "
                  "hairs; the face, eyes and nose brushed as boldly as the background",
                  "a classic painted portrait composition"),
    "cinematic": ("cinematic film still, shot fresh for this scene, not an edit of the photo",
                  "a real 35mm film look, natural proportions, gentle grain, restrained color, the face in focus",
                  "a candid film-still framing with real depth"),
    "comic": ("comic-book illustration",
              "confident black ink contours, flat bold color, halftone dots in the shadows; the face drawn in ink and "
              "flat color like everything else",
              "one dynamic comic panel: a tilted angle, strong foreground and background separation"),
    "screenprint": ("vintage screenprint poster",
                    "four flat inks only on cream paper, bold cut silhouettes, slight misregistration and paper grain; "
                    "the dog itself reduced to flat ink shapes, no fur strands, shading only as halftone dots",
                    "a bold, near-symmetrical poster with a simple graphic backdrop"),
    "collage": ("cut-paper collage",
                "real layered cut paper, visible fibres, soft shadows between layers; the dog itself built from 20 to 30 "
                "hand-cut paper pieces, each one flat colour with scissor-cut or torn edges, no brushwork or fur "
                "strands anywhere",
                "flat layered planes and simplified background shapes"),
    "ink": ("fine pen-and-ink drawing",
            "brown ink line on cream paper, precise contours and cross-hatching, only a light pale wash; "
            "the face drawn in the same line",
            "a vignette on white paper, the setting only lightly suggested and fading out"),
}

# where the scene happens, from the chat
SETTING = {
    "spot": {"feet": "at {pos} person's feet (only their socked feet and ankles show)",
             "bed": "on {pos} person's side of the bed",
             "couch": "on the couch beside {pos} person (only their knee or hand at the edge)",
             "anywhere": "right beside {pos} person (only their hand at the edge)"},
    "together": {"walk": "on the morning walk outdoors", "coffee": "at morning coffee, a plain mug nearby",
                 "movie": "on movie night, lit by the glow of an unseen screen", "naps": "at nap time",
                 "car": "in the car, the window behind {obj}"},
}

# warm: caught mid-moment, from the chat's activity
WARM_ACTION = {"walk": "trotting along mid-stride, ears bouncing", "coffee": "sitting up hopefully, eyes on the mug",
               "movie": "sprawled across the couch, one eye on the screen", "naps": "just waking, mid-stretch",
               "car": "head out of the window, ears flying", "door": "at the door mid-wag",
               "toy": "trotting in with the toy held high", "spin": "caught mid-spin",
               "cool": "pretending not to watch, one eye open"}

# hilarious: a visual joke built on the stated thing (scale or importance), never the dog's anatomy
# Ruling (Krish, 2026-10-29): Hilarious may use theatrical staging (a cushion, a spotlight, the buyer's own
# couch cushions piled high); it never invents the dog's toys, food, clothes, habits or places.
FUNNY = {"walk": "leading the morning walk at the very front like a parade marshal, chest out, the path stretching behind",
         "coffee": "the coffee mug set before {obj} on the table like an offering on an altar, guarded with narrowed eyes",
         "movie": "perched at the very top of the couch back like a stern film critic in a balcony box, narrowed eyes "
                  "fixed on the unseen screen, one ear cocked in disapproval",
         "naps": "sprawled diagonally across the entire bed, {pos} person's feet squeezed off the edge",
         "car": "in the front seat, chin up, ears streaming, like a celebrity in a motorcade",
         "couch": "the couch cushions piled into a towering throne with {obj} seated on top",
         "bed": "sprawled diagonally across the entire bed, {pos} person's feet squeezed off the edge",
         "feet": "sitting squarely on {pos} person's feet, pinning them down like a paperweight",
         "door": "nose pressed to the front door, on high alert, as if guarding a bank vault",
         "spin": "caught mid-spin like a figure skater, utterly serious",
         "cool": "pretending to ignore everyone with absurd dignity, nose in the air"}


def facts(c):
    t, s, h = c.get("together"), c.get("spot"), c.get("home")
    where = []
    for key, val in (("together", t), ("spot", s)):
        if val:
            where.append(SETTING[key].get(val, "%s, in the owner's words: \"%s\"" % (
                "doing what {sub} {loves} most with {pos} person" if key == "together" else "in {pos} favourite spot", val)))
    extras = []
    if c.get("toy"):
        extras.append("{pos} %s" % c["toy"])
    if c.get("accessory"):
        extras.append("a plain %s with no pattern" % c["accessory"])
    return t, s, h, where, extras


def staging(c):
    t, s, h, where, extras = facts(c)
    tone = c["tone"]
    place = ", ".join(where) or "at home"
    toy = c.get("toy")
    with_toy = (", {pos} %s hugged close" % toy) if toy else ""
    worn = (", wearing a plain %s with no pattern" % c["accessory"]) if c.get("accessory") else ""
    if tone == "sentimental":
        return ("Pose: asleep or resting, eyes closed, curled up close %s%s%s, utterly safe and content. "
                "Camera: close and low at {pos} eye level, intimate. Light: soft, low window light; calm, muted "
                "palette. Mood: quiet and tender." % (place, with_toy, worn))
    if tone == "warm":
        act = WARM_ACTION.get(t) or WARM_ACTION.get(h) or "trotting toward the viewer, mid-step"
        with_t = (", with {pos} %s" % toy) if toy else ""
        return ("Pose: caught mid-moment, %s, %s%s%s, head turned three-quarters with bright eyes and a small "
                "knowing smile. Camera: candid, slightly above, as if snapped by {pos} person. Light: clear, bright "
                "daylight; lively natural color. Mood: warm and happy, both eyes open." % (act, place, with_t, worn))
    joke = (("{pos} %s presented on a velvet cushion under a spotlight like a crown jewel, {obj} guarding it "
             "with narrowed eyes" % toy) if toy else None) or FUNNY.get(t) or FUNNY.get(s) or FUNNY.get(h)
    if not joke and t:
        joke = "this, in the owner's words: \"%s\", turned into one grand, absurd scene" % t
    joke = joke or "posed like a grand, solemn oil portrait of a statesman, nose in the air"
    return ("The joke, readable from across the room: %s, %s%s. Expression: utterly serious, narrowed eyes. "
            "Camera: worm's-eye view from the floor, wide-angle, the frame tilted. Light: bright, punchy, theatrical, "
            "a spotlight feel. Mood: funny at a glance, affectionate, never mocking." % (joke, place, worn))


FORMAT = {
    "portrait": ("vertical 2:3", "Framing: from a little further back, open space above {pos} head, and the "
                                 "lower-right quarter left plain for a small note."),
    "mug": ("wide 3:2 mug wrap", "Framing: one clear focal dog in the left half, the right third left plain for a "
                                 "small note, nothing important at the far edges where the handle sits."),
    "blanket": ("square all-over blanket print", "Layout: five or six different poses of {obj} from this scene, edge "
                                                 "to edge, large enough to read across a room, no panel, border or "
                                                 "words, motifs may run off the edges."),
}


def build(c):
    p = c.get("pronoun", "they")
    sub, obj, pos = PRON[p]
    is_, loves = VERB[p]
    medium, medium_detail, composition = STYLE[c["style"]]
    shape, framing = FORMAT[c["format"]]
    breed = c.get("breed") or "dog"
    avoid = ["faces", "text, letters or logos", "patterns on clothing", "food, snacks or drinks",
             "visible screens", "other animals", "any object not named here"]
    if c.get("together") == "coffee":
        avoid[3] = "food or snacks"
    if c["style"] == "comic":
        avoid.insert(0, "speech bubbles, sound effects or lettering")
    if c.get("no_toy"):
        avoid.insert(0, "toys")
    text = " ".join([
        "Create a new %s, %s, of the dog in this photo." % (medium, shape),
        "Keep exactly who %s %s: this %s's face shape, ears, eyes, muzzle, coat colours and markings. Change "
        "everything else; never reuse the photo's pose, angle, light or background." % (sub, is_, breed),
        staging(c),
        "Composition: %s. %s" % (composition, framing),
        "Medium: %s." % medium_detail,
        "Avoid: %s." % ", ".join(avoid),
    ])
    return text.format(sub=sub, obj=obj, pos=pos, loves=loves)


if __name__ == "__main__":
    print(build(json.load(open(sys.argv[1]))))
