"""Téléversement privé de contrôle vers la chaîne YouTube officielle.
N'est jamais appelé par le workflow quotidien. Secrets GitHub uniquement.
"""
import argparse
import json
import os
from pathlib import Path

CHANNEL_ID = "UCk-B48dgzUSkcWsQxAQboQw"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]

def required(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Secret GitHub manquant : {name}. Aucune vidéo téléversée.")
    return value

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--metadata", required=True)
    ap.add_argument("--title", default="Léo & le Prof — Pilote privé de validation")
    args = ap.parse_args()
    video_path = Path(args.video)
    if not video_path.is_file() or not video_path.stat().st_size:
        raise FileNotFoundError(f"Vidéo absente : {video_path}")
    metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
    if metadata.get("published") is not False:
        raise ValueError("Le fichier n'est pas marqué comme pilote non publié")
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    creds = Credentials(
        token=None,
        refresh_token=required("YOUTUBE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=required("YOUTUBE_CLIENT_ID"),
        client_secret=required("YOUTUBE_CLIENT_SECRET"),
        scopes=SCOPES,
    )
    youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)
    # Éviter toute erreur de compte si Google a plusieurs chaînes.
    channels = youtube.channels().list(part="id,snippet", mine=True).execute()
    found = [c for c in channels.get("items", []) if c.get("id") == CHANNEL_ID]
    if not found:
        raise RuntimeError("La connexion Google n'autorise pas la chaîne Léo & le Prof. Aucun téléversement effectué.")
    print("Chaîne YouTube vérifiée :", CHANNEL_ID)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": args.title[:100],
                "description": metadata.get("youtube_description", ""),
                "categoryId": "27",
                "defaultLanguage": "fr",
            },
            "status": {
                "privacyStatus": "private",
                "selfDeclaredMadeForKids": False,
                "embeddable": False,
            },
        },
        media_body=MediaFileUpload(str(video_path), mimetype="video/mp4",
                                  chunksize=8 * 1024 * 1024, resumable=True),
    )
    response = None
    while response is None:
        _, response = request.next_chunk()
    video_id = response.get("id")
    if not video_id:
        raise RuntimeError("YouTube n'a pas renvoyé d'identifiant vidéo.")
    print("Téléversement PRIVÉ terminé :", "https://www.youtube.com/watch?v=" + video_id)
    print("Aucune publication publique programmée.")

if __name__ == "__main__":
    main()
