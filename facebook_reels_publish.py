"""Publication automatique des mêmes MP4 sur la Page Facebook Léo & le Prof.

Secrets GitHub uniquement : META_PAGE_ID et META_PAGE_ACCESS_TOKEN.
Ne fonctionne PAS tant que l'accès Page n'est pas autorisé dans Meta.
API officielle Facebook Page Reels : START -> rupload -> FINISH.
"""
import argparse
import json
import os
from pathlib import Path
import requests

GRAPH_VERSION = "v27.0"
GRAPH = f"https://graph.facebook.com/{GRAPH_VERSION}"
UPLOAD_BASE = f"https://rupload.facebook.com/video-upload/{GRAPH_VERSION}/"
VIDEO_PATH = Path("output_officiel/Leo_et_le_Prof_Officiel_Voix_Naturelles.mp4")
META_PATH = Path("output_officiel/metadata.json")

def required(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Secret requis : {name}. Aucun Reel Facebook publié.")
    return value

def api(method, url, token, **kwargs):
    kwargs.setdefault("timeout", 90)
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"{'OAuth' if url.startswith(UPLOAD_BASE) else 'Bearer'} {token}"
    response = requests.request(method, url, headers=headers, **kwargs)
    try:
        payload = response.json()
    except ValueError:
        raise RuntimeError(f"Réponse Meta non JSON (HTTP {response.status_code})") from None
    if not response.ok or (isinstance(payload, dict) and payload.get("error")):
        error = payload.get("error", {}) if isinstance(payload, dict) else {}
        raise RuntimeError(f"Erreur Meta (HTTP {response.status_code}): {error.get('message', 'inconnue')}")
    return payload

def already_published(page_id, token, marker):
    """Ne pas envoyer de doublon lorsqu'un identifiant d'épisode existe déjà dans les descriptions.

    Si la lecture échoue, bloquer l'envoi par sécurité, ne PAS présumer qu'il manque.
    """
    next_url = f"{GRAPH}/{page_id}/video_reels"
    params = {"fields": "id,description", "limit": 50}
    for _ in range(100):
        result = api("GET", next_url, token, params=params)
        for entry in result.get("data", []):
            if marker in entry.get("description", ""):
                print("Reel déjà présent sur la Page :", entry.get("id"))
                return True
        next_url = result.get("paging", {}).get("next")
        if not next_url:
            return False
        # Ne pas intégrer un access_token dans les journaux.
        params = None
    # Trop d'historique pour confirmer l'absence ; on suspend pour éviter les doublons.
    raise RuntimeError("Historique Meta trop long pour garantir l'absence de doublons")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", required=True, help="YYYY-MM-DD date locale du Short")
    parser.add_argument("--start", type=int, required=True, help="index des 3 questions")
    args = parser.parse_args()
    import datetime
    datetime.date.fromisoformat(args.day)
    page_id = required("META_PAGE_ID")
    if not page_id.isdecimal():
        raise RuntimeError("META_PAGE_ID doit être l'identifiant numérique de la Page")
    token = required("META_PAGE_ACCESS_TOKEN")
    metadata = json.loads(META_PATH.read_text(encoding="utf8"))
    catalog = json.loads(Path("questions.json").read_text(encoding="utf8"))
    expected = [q["id"] for q in catalog[args.start:args.start + 3]]
    if len(expected) != 3 or metadata.get("question_ids") != expected:
        raise RuntimeError("Le MP4 ne correspond pas au lot des 3 questions du jour")
    if not VIDEO_PATH.is_file() or VIDEO_PATH.stat().st_size < 100000:
        raise RuntimeError("Vidéo MP4 absente ou invalide")

    page = api("GET", f"{GRAPH}/{page_id}", token, params={"fields":"id,name"})
    if str(page.get("id")) != page_id or page.get("name") != "Léo & le Prof":
        raise RuntimeError("La connexion Meta n'est pas celle de la Page officielle Léo & le Prof")
    marker = f"LEO-PROF-JOUR-{args.day}"
    if already_published(page_id, token, marker):
        return

    # 1. Initialiser l'upload sur la Page
    started = api("POST", f"{GRAPH}/{page_id}/video_reels", token,
                  data={"upload_phase": "start"})
    video_id = str(started.get("video_id", ""))
    if not video_id.isdecimal():
        raise RuntimeError("Meta n'a pas renvoyé un identifiant vidéo utilisable")
    # 2. Transférer les octets MP4. La réponse de rupload est traitée strictement.
    with VIDEO_PATH.open("rb") as f:
        uploaded = api("POST", f"{UPLOAD_BASE}{video_id}", token,
                       headers={"offset": "0", "file_size": str(VIDEO_PATH.stat().st_size),
                                "Content-Type": "application/octet-stream"},
                       data=f, timeout=240)
    if uploaded.get("success") is not True:
        raise RuntimeError("Meta n'a pas confirmé le transfert vidéo")

    # 3. Finaliser en Reel public ; description indexée par jour pour éviter les doublons.
    caption = ("🌍🔬 Léo & le Prof : 3 questions, 3 réponses et une découverte !\n"
               "Abonne-toi pour apprendre quelque chose chaque jour.\n"
               "Notre chaîne YouTube : " + metadata["channel_url"] +
               f"\n\n#LeoEtLeProf #Sciences #CultureGenerale\n{marker}")
    result = api("POST", f"{GRAPH}/{page_id}/video_reels", token, data={
        "upload_phase": "finish", "video_id": video_id,
        "video_state": "PUBLISHED", "description": caption,
        "title": "Léo & le Prof | 3 questions, 3 réponses"
    })
    if result.get("success") is not True:
        raise RuntimeError("Meta n'a pas confirmé la finalisation du Reel")
    print("Reel Facebook accepté, identifiant :", video_id)
    print("Important : vérifier la publication et les éventuels traitements vidéo dans Meta Business Suite")

if __name__ == "__main__":
    main()
