"""Pilote autonome 3 Q/R: deux personnages 2D animés, voix FR, 9:16.
Ne publie jamais. La bouche suit l'énergie du son (approximation, pas phonèmes).
"""
import argparse
import asyncio
import json
import math
import subprocess
import wave
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from edge_tts import Communicate

ROOT = Path(__file__).resolve().parent
AVATARS = ROOT / "assets" / "avatars"
LEO_IMAGE = AVATARS / "leo.png"
PROF_IMAGE = AVATARS / "prof.png"
W, H, FPS = 540, 960, 12
BG = (7, 19, 43)
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def run(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, args)], check=True)


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def fit_lines(draw, text, f, width):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if draw.textbbox((0, 0), test, font=f)[2] <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centered_text(draw, text, x, center_y, width, size, color="white", bold=True):
    f = font(size, bold)
    lines = fit_lines(draw, text, f, width)
    step = size + 11
    y = center_y - (len(lines) - 1) * step / 2
    for line in lines:
        draw.text((x, y), line, fill=color, font=f, anchor="mm")
        y += step


def character(draw, cx, cy, leo, speaking, amplitude, t):
    skin = (157, 91, 57) if leo else (128, 75, 53)
    shirt = (28, 120, 219) if leo else (230, 240, 246)
    outline = (28, 44, 67)
    hair = (24, 26, 37) if leo else (178, 188, 197)
    bob = int(math.sin(t * 2.8 + (0 if leo else 1)) * 3) if speaking else 0
    cy += bob
    # Épaules, cou, mains et avant-bras
    draw.rounded_rectangle((cx - 104, cy + 100, cx + 104, cy + 325), radius=70, fill=shirt)
    draw.rounded_rectangle((cx - 25, cy + 68, cx + 25, cy + 142), radius=14, fill=skin)
    gesture = int(18 * math.sin(t * 4.5)) if speaking else 0
    hand_y = cy + 177 - max(gesture, 0)
    draw.line([(cx + 73, cy + 154), (cx + 110, hand_y)], fill=shirt, width=31)
    draw.ellipse((cx + 92, hand_y - 15, cx + 126, hand_y + 19), fill=skin)
    # Cheveux, visage, yeux
    draw.ellipse((cx - 79, cy - 89, cx + 79, cy + 108), fill=skin, outline=outline, width=3)
    draw.pieslice((cx - 84, cy - 104, cx + 84, cy + 20), 180, 360, fill=hair)
    if leo:
        for dx in (-60, -35, -10, 15, 40):
            draw.ellipse((cx + dx - 16, cy - 109, cx + dx + 25, cy - 71), fill=hair)
    else:
        draw.arc((cx - 59, cy + 17, cx + 60, cy + 118), 5, 175, fill=hair, width=15)
        for dx in (-33, 33):
            draw.ellipse((cx + dx - 31, cy - 13, cx + dx + 31, cy + 31), outline=outline, width=5)
        draw.line((cx - 8, cy + 7, cx + 8, cy + 7), fill=outline, width=4)
    for dx in (-32, 32):
        draw.ellipse((cx + dx - 9, cy + 8, cx + dx + 9, cy + 29), fill="white")
        draw.ellipse((cx + dx - 3, cy + 13, cx + dx + 4, cy + 23), fill=outline)
    # Bouche pilotée par l'amplitude: pseudo-lip-sync, sans promesse phonétique
    opening = 3 + int(min(1.0, amplitude * 5.5) * 27) if speaking else 3
    draw.rounded_rectangle((cx - 20, cy + 57, cx + 20, cy + 57 + opening),
                           radius=8, fill=(62, 29, 37))
    if opening > 15:
        draw.line((cx - 12, cy + 60, cx + 12, cy + 60), fill=(246, 236, 225), width=4)


def render_frame(speaker, text, topic, qidx, amplitude, t):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for yy in range(0, H, 55):
        d.line((0, yy, W, yy), fill=(15, 37, 62), width=1)
    for xx in range(0, W, 54):
        d.line((xx, 0, xx, H), fill=(15, 37, 62), width=1)
    d.rounded_rectangle((18, 28, 522, 105), radius=22, fill=(18, 62, 100))
    d.text((270, 68), "LÉO & LE PROF TECH", font=font(26, True), anchor="mm", fill="white")
    d.rounded_rectangle((18, 124, 522, 176), radius=15, fill=(248, 199, 65))
    centered_text(d, f"QUESTION {qidx}/3  •  {topic.upper()}", 270, 151, 476, 19, (14, 33, 55))
    d.rounded_rectangle((16, 195, 524, 641), radius=22, fill=(13, 45, 77))
    # Portraits officiels imposés : jamais de personnages de remplacement.
    for image_path, center_x in ((LEO_IMAGE, 136), (PROF_IMAGE, 399)):
        with Image.open(image_path) as source:
            portrait = source.convert("RGBA")
            portrait.thumbnail((245, 410), Image.Resampling.LANCZOS)
            x = int(center_x - portrait.width / 2)
            y = 223 + (410 - portrait.height)
            im.paste(portrait, (x, y), portrait)
    # NOTE : portraits statiques pour le moment. Une synchronisation réaliste
    # doit préserver les visages; ne pas dessiner de bouche par-dessus.
    d.rounded_rectangle((46, 606, 226, 649), radius=12,
                        fill=(248, 199, 65) if speaker == "Léo" else (44, 86, 114))
    d.rounded_rectangle((310, 606, 494, 649), radius=12,
                        fill=(91, 226, 237) if speaker == "Le Prof" else (44, 86, 114))
    d.text((136, 627), "LÉO", font=font(21, True), anchor="mm", fill=(8, 25, 49) if speaker == "Léo" else "white")
    d.text((399, 627), "LE PROF", font=font(21, True), anchor="mm", fill=(8, 25, 49) if speaker == "Le Prof" else "white")
    d.rounded_rectangle((20, 672, 520, 882), radius=23, fill=(13, 50, 83),
                        outline=(74, 189, 212), width=3)
    centered_text(d, text, 270, 778, 458, 22 if len(text) > 130 else 25)
    d.text((270, 925), "3 QUESTIONS  •  3 RÉPONSES", anchor="mm",
           font=font(17, True), fill=(211, 232, 245))
    return im


async def synthesize(text, voice, audio_path):
    # Pas de voix robotique de secours silencieusement substituée.
    await Communicate(text, voice, rate="+8%").save(str(audio_path))


def audio_levels(wav_path, fps=FPS):
    with wave.open(str(wav_path), "rb") as wf:
        rate = wf.getframerate()
        frames_per_chunk = max(1, round(rate / fps))
        result = []
        while True:
            data = wf.readframes(frames_per_chunk)
            if not data:
                break
            import audioop
            rms = audioop.rms(data, 2) / 32768.0
            result.append(rms)
    return result


async def make_scene(out, scene_id, voice, text, speaker, topic, qidx):
    mp3 = out / f"audio_{scene_id}.mp3"
    wav = out / f"audio_{scene_id}.wav"
    silent = out / f"scene_{scene_id}.mp4"
    await synthesize(text, voice, mp3)
    run("-i", mp3, "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav)
    levels = audio_levels(wav)
    frames_dir = out / f"frames_{scene_id}"
    frames_dir.mkdir()
    for n, amp in enumerate(levels):
        render_frame(speaker, text, topic, qidx, amp, n/FPS).save(frames_dir / f"{n:05d}.jpg", quality=83)
    run("-framerate", str(FPS), "-i", frames_dir / "%05d.jpg",
        "-i", mp3, "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
        "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "128k",
        "-shortest", silent)
    return silent


async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="output_pilot_3")
    p.add_argument("--start", type=int, default=0, help="Index de la première question")
    args = p.parse_args()
    missing = [str(p) for p in (LEO_IMAGE, PROF_IMAGE) if not p.is_file()]
    if missing:
        raise FileNotFoundError("Portraits officiels absents : " + ", ".join(missing) + ". Importer les PNG validés avant tout rendu ; aucun avatar de substitution ne sera généré.")
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    questions = json.loads((ROOT / "questions.json").read_text(encoding="utf8"))
    if len(questions) < 3:
        raise ValueError("Au moins 3 questions sont nécessaires")
    # Trois questions distinctes, ordre stable reproductible.
    selected = [questions[(args.start + i) % len(questions)] for i in range(3)]
    scenes = []
    for i, q in enumerate(selected, 1):
        scenes.append(await make_scene(out, f"{i}_q", "fr-FR-EloiseNeural",
                                       q["question"], "Léo", q["category"], i))
        scenes.append(await make_scene(out, f"{i}_r", "fr-FR-HenriNeural",
                                       q["answer"], "Le Prof", q["category"], i))
    manifest = out / "concat.txt"
    manifest.write_text("".join(f"file '{v.name}'\n" for v in scenes))
    final = out / "leo_prof_3_questions_pilote.mp4"
    run("-f", "concat", "-safe", "0", "-i", manifest,
        "-c", "copy", "-movflags", "+faststart", final)
    (out / "metadata.json").write_text(json.dumps({
        "published": False, "status": "PILOT_REVIEW_REQUIRED",
        "questions": [q["id"] for q in selected],
        "sources": [q["source"] for q in selected],
        "lip_sync": "audio_energy_approximation_not_phoneme_alignment"
    }, ensure_ascii=False, indent=2), encoding="utf8")
    print("PILOTE NON PUBLIÉ:", final)


if __name__ == "__main__":
    asyncio.run(main())
