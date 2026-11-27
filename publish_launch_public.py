"""Publie une seule fois le Short de lancement approuvé sans modifier la vidéo privée existante.
Utilise le consentement OAuth YouTube upload déjà accordé.
"""
import json
import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CHANNEL_ID = "UCk-B48dgzUSkcWsQxAQboQw"
RELEASE_KEY = "LEO-PROF-LANCEMENT-2026-11-26"
TITLE = "Le Wi-Fi, les mots de passe et le DNS : 3 questions utiles ! 🤯 #Shorts"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.readonly"]

def required(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Secret manquant: {name}")
    return value

def main():
    video = Path("output_officiel/Leo_et_le_Prof_Officiel_Voix_Naturelles.mp4")
    metadata = json.loads(Path("output_officiel/metadata.json").read_text(encoding="utf8"))
    assert metadata.get("question_ids") == ["q001","q002","q003"], "Lot de questions inattendu"
    if not video.is_file() or video.stat().st_size < 100000:
        raise RuntimeError("Vidéo manquante ou trop petite")
    credentials = Credentials(
        token=None, refresh_token=required("YOUTUBE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=required("YOUTUBE_CLIENT_ID"),
        client_secret=required("YOUTUBE_CLIENT_SECRET"), scopes=SCOPES,
    )
    youtube = build("youtube","v3",credentials=credentials,cache_discovery=False)
    result = youtube.channels().list(part="id,contentDetails",mine=True).execute()
    matches = [c for c in result.get("items",[]) if c["id"]==CHANNEL_ID]
    if len(matches) != 1: raise RuntimeError("Mauvaise chaîne Google: publication annulée")
    uploads = matches[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    # Prévenir une répétition si le job est relancé : parcourir les 200 derniers téléversements.
    token = None
    for _ in range(4):
        page = youtube.playlistItems().list(
            part="snippet",playlistId=uploads,maxResults=50,pageToken=token).execute()
        for item in page.get("items",[]):
            if RELEASE_KEY in item.get("snippet",{}).get("description",""):
                vid = item["snippet"]["resourceId"]["videoId"]
                print("Publication déjà réalisée; aucun doublon:",vid)
                return
        token = page.get("nextPageToken")
        if not token: break
    body = {
        "snippet": {
            "title": TITLE,
            "description": metadata["youtube_description"] + "\n\nRéférence de publication : "+RELEASE_KEY,
            "categoryId":"27",
            "defaultLanguage":"fr",
            "tags":["Léo et le Prof","culture générale","technologie","sciences","questions réponses"],
        },
        "status": {
            "privacyStatus":"public",
            "selfDeclaredMadeForKids":False,
        },
    }
    request = youtube.videos().insert(
        part="snippet,status",body=body,
        media_body=MediaFileUpload(str(video),mimetype="video/mp4",
                                   chunksize=8*1024*1024,resumable=True))
    res=None
    while res is None:
        _,res=request.next_chunk()
    vid=res.get("id")
    if not vid: raise RuntimeError("Téléversement sans identifiant YouTube")
    print("VIDÉO TÉLÉVERSÉE:", "https://www.youtube.com/watch?v="+vid)
    print("STATUT REÇU:",res.get("status",{}).get("privacyStatus"))
    if res.get("status",{}).get("privacyStatus")!="public":
        raise RuntimeError("YouTube n'a pas confirmé la visibilité publique")

if __name__=="__main__":
    main()
