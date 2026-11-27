"""Rendre publique UNIQUEMENT une vidéo pilote identifiée explicitement.
À déclencher manuellement après avoir accordé le scope OAuth youtube.force-ssl.
Ne téléverse jamais un deuxième MP4 et ne parcourt pas la chaîne pour publier en masse.
"""
import argparse
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

EXPECTED_CHANNEL = "UCk-B48dgzUSkcWsQxAQboQw"
EXPECTED_TITLE = "Léo & le Prof — Pilote privé de validation"
EDIT_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"

def secret(name):
    val = os.environ.get(name, "").strip()
    if not val:
        raise RuntimeError(f"Secret GitHub requis : {name}")
    return val

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-id", required=True,
                        help="Identifiant EXACT de la vidéo privée déjà vérifiée")
    args = parser.parse_args()
    if len(args.video_id) != 11 or not all(c.isalnum() or c in "-_" for c in args.video_id):
        raise ValueError("ID vidéo YouTube non valide")
    creds = Credentials(
        token=None, refresh_token=secret("YOUTUBE_REFRESH_TOKEN_EDIT"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=secret("YOUTUBE_CLIENT_ID"),
        client_secret=secret("YOUTUBE_CLIENT_SECRET"),
        scopes=[EDIT_SCOPE],
    )
    youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)
    res = youtube.videos().list(part="snippet,status", id=args.video_id).execute()
    items = res.get("items", [])
    if len(items) != 1:
        raise RuntimeError("La vidéo n'a pas été trouvée avec les droits actuels")
    video = items[0]
    snippet, status = video["snippet"], video["status"]
    if snippet.get("channelId") != EXPECTED_CHANNEL:
        raise RuntimeError("La vidéo ne correspond pas à la chaîne officielle")
    if snippet.get("title") != EXPECTED_TITLE:
        raise RuntimeError("Titre inattendu : arrêt pour éviter toute publication erronée")
    if status.get("privacyStatus") == "public":
        print("Déjà publique :", args.video_id)
        return
    if status.get("privacyStatus") != "private":
        raise RuntimeError("La vidéo n'est pas privée. Mise à jour annulée.")
    body = {
        "id": args.video_id,
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": status.get("selfDeclaredMadeForKids", False),
        },
    }
    result = youtube.videos().update(part="status", body=body).execute()
    if result.get("status", {}).get("privacyStatus") != "public":
        raise RuntimeError("YouTube n'a pas confirmé la mise en public")
    print("VIDÉO PUBLIQUE CONFIRMÉE :", "https://www.youtube.com/watch?v="+args.video_id)

if __name__ == "__main__":
    main()
