"""Publication quotidienne d'épisodes inédits validés dans questions.json.
Épisodes possibles : tous les lots complets après le pilote. Un seul Short par date ; aucun doublon.
Le lancement du pilote doit être déjà présent dans les téléversements YouTube.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CHANNEL_ID="UCk-B48dgzUSkcWsQxAQboQw"
FIRST_RELEASE="LEO-PROF-LANCEMENT-2026-11-26"
SCOPES=["https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.readonly"]

def required(name):
    val=os.environ.get(name,"").strip()
    if not val:
        raise RuntimeError(f"Secret manquant : {name}")
    return val

def uploaded_descriptions(youtube,playlist_id):
    token=None
    for _ in range(100):
        page=youtube.playlistItems().list(
            part="snippet", playlistId=playlist_id, maxResults=50,pageToken=token).execute()
        for item in page.get("items",[]):
            sn=item.get("snippet",{})
            yield sn.get("description",""),sn.get("resourceId",{}).get("videoId","")
        token=page.get("nextPageToken")
        if not token:return
    raise RuntimeError("Historique YouTube trop long pour vérifier les doublons")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--start",required=True,type=int)
    p.add_argument("--day",required=True,help="date locale YYYY-MM-DD")
    args=p.parse_args()
    if args.start < 3 or args.start % 3 != 0:
        raise ValueError("Index de lot invalide ou réservé au pilote")
    datetime.date.fromisoformat(args.day)
    key="LEO-PROF-JOUR-"+args.day
    file=Path("output_officiel/Leo_et_le_Prof_Officiel_Voix_Naturelles.mp4")
    metadata=json.loads(Path("output_officiel/metadata.json").read_text(encoding="utf8"))
    questions=json.loads(Path("questions.json").read_text(encoding="utf8"))
    expected=[q["id"] for q in questions[args.start:args.start+3]]
    if len(expected)!=3 or metadata.get("question_ids")!=expected:
        raise RuntimeError("Mauvais lot de questions")
    if not file.exists() or file.stat().st_size<100000:
        raise RuntimeError("Short manquant")
    creds=Credentials(token=None,refresh_token=required("YOUTUBE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=required("YOUTUBE_CLIENT_ID"),
        client_secret=required("YOUTUBE_CLIENT_SECRET"),
        scopes=SCOPES)
    youtube=build("youtube","v3",credentials=creds,cache_discovery=False)
    res=youtube.channels().list(part="id,contentDetails",mine=True).execute()
    matches=[c for c in res.get("items",[]) if c["id"]==CHANNEL_ID]
    if len(matches)!=1:raise RuntimeError("Cette connexion n'est pas celle de Léo & le Prof")
    uploads=matches[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    prior=list(uploaded_descriptions(youtube,uploads))
    if not any(FIRST_RELEASE in desc for desc,_ in prior):
        raise RuntimeError("Premier épisode public non repéré. Aucun Short quotidien envoyé.")
    for desc,vid in prior:
        if key in desc:
            print("Short déjà téléversé pour",args.day,vid)
            return
    selected=questions[args.start:args.start+3]
    headline=selected[0]["question"].rstrip("?")
    title=f"{headline} ? 3 réponses surprenantes ! #Shorts"[:100]
    body={"snippet":{
        "title":title,
        "description":metadata["youtube_description"]+"\n\nEpisode-ID: "+key,
        "categoryId":"27",
        "defaultLanguage":"fr",
        "tags":["Léo et le Prof","sciences","culture générale","découvertes"]},
        "status":{"privacyStatus":"public","selfDeclaredMadeForKids":False}}
    request=youtube.videos().insert(part="snippet,status",body=body,
       media_body=MediaFileUpload(str(file),mimetype="video/mp4",
            chunksize=8*1024*1024,resumable=True))
    result=None
    while result is None:
        _,result=request.next_chunk()
    video_id=result.get("id")
    print("URL nouvel épisode:",("https://www.youtube.com/watch?v="+video_id) if video_id else "absent")
    if not video_id or result.get("status",{}).get("privacyStatus")!="public":
        raise RuntimeError("Publication non confirmée par YouTube")

if __name__=="__main__":
    main()
