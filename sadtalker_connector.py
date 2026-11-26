"""Connecteur expérimental vers le Space public SadTalker.

Ne réalise aucune publication YouTube. Chaque avatar nécessite son image et
sa piste audio. Les quotas ZeroGPU peuvent empêcher une génération gratuite.
"""
import argparse
import json
import os
from pathlib import Path

SPACE = "henrybit/SadTalker-Demo"

def client():
    from gradio_client import Client
    token = os.environ.get("HF_TOKEN") or None
    return Client(SPACE, token=token)

def check():
    c = client()
    api = c.view_api(return_format="dict")
    print(json.dumps({"space": SPACE, "api": api}, ensure_ascii=False, default=str, indent=2))

def generate(image, audio, output):
    from gradio_client import handle_file
    c = client()
    # Named endpoint can change when the Space owner updates the application.
    result = c.predict(
        handle_file(str(Path(image).resolve())),
        handle_file(str(Path(audio).resolve())),
        "crop", False, 0, 1.0,
        api_name="/generate",
    )
    # Le Space renvoie un objet Gradio Video : {"video": "/tmp/...mp4", "subtitles": ...}.
    # Selon les versions de gradio_client, le résultat peut être enveloppé dans une liste.
    if isinstance(result, (list, tuple)):
        result = result[0] if result else None
    if isinstance(result, dict):
        result = result.get("video")
    if isinstance(result, dict):
        result = result.get("path")
    if not isinstance(result, str) or not Path(result).is_file():
        raise RuntimeError(f"Résultat vidéo introuvable ou incompatible : {repr(result)[:300]}")
    import shutil
    dest = Path(output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(result, dest)
    print(f"Animation générée : {dest}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    p.add_argument("--image")
    p.add_argument("--audio")
    p.add_argument("--output", default="output_sadtalker/avatar.mp4")
    a=p.parse_args()
    if a.check:
        check()
    elif a.image and a.audio:
        generate(a.image, a.audio, a.output)
    else:
        p.error("Utiliser --check ou fournir --image et --audio")
