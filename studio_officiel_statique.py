"""Short officiel : portraits fixes + voix naturelles distinctes, 3 questions.
Aucun repli sur une voix robotique. Aucun téléversement YouTube.
Prérequis : assets/avatars/leo.png et assets/avatars/prof.png.
"""
import argparse
import asyncio
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from edge_tts import Communicate

ROOT = Path(__file__).resolve().parent
AVATARS = ROOT / "assets" / "avatars"
W, H = 720, 1280
CHANNEL_URL = "https://www.youtube.com/channel/UCk-B48dgzUSkcWsQxAQboQw"
SUBSCRIBE_URL = CHANNEL_URL + "?sub_confirmation=1"
SUBSCRIBE_MESSAGE = ("Chaque jour, une nouvelle découverte pour mieux comprendre le monde ! "
                     "Abonne-toi à Léo & le Prof pour apprendre quelque chose d'utile chaque jour.")
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def cmd(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str,args)],check=True)

def ft(n,bold=True):
    return ImageFont.truetype(BOLD if bold else REG,n)

def wrap(draw,text,font,maxw):
    lines=[]; line=""
    for word in text.split():
        candidate=(line+" "+word).strip()
        if draw.textbbox((0,0),candidate,font=font)[2] <= maxw: line=candidate
        else:
            if line: lines.append(line)
            line=word
    if line: lines.append(line)
    return lines

def image_cover(source,w,h):
    ratio=max(w/source.width,h/source.height)
    scaled=source.resize((round(source.width*ratio),round(source.height*ratio)),Image.Resampling.LANCZOS)
    x=(scaled.width-w)//2;y=max(0,int((scaled.height-h)*0.33))
    return scaled.crop((x,y,x+w,y+h))

def panel(image,source,x,y,active,accent):
    d=ImageDraw.Draw(image)
    if active:
        glow=Image.new("RGBA",(334,560))
        g=ImageDraw.Draw(glow)
        g.rounded_rectangle((12,12,322,548),radius=30,fill=(*accent,90))
        glow=glow.filter(ImageFilter.GaussianBlur(14))
        image.paste(glow,(x-18,y-18),glow)
    d.rounded_rectangle((x-5,y-5,x+303,y+529),radius=24,fill=accent if active else (54,96,127))
    cover=image_cover(source,298,524)
    mask=Image.new("L",(298,524));m=ImageDraw.Draw(mask)
    m.rounded_rectangle((0,0,297,523),radius=20,fill=255)
    image.paste(cover,(x,y),mask)

def render(leo,prof,speaker,text,num,path):
    image=Image.new("RGB",(W,H),(7,21,47));d=ImageDraw.Draw(image)
    for y in range(H):
        t=y/H;d.line((0,y,W,y),fill=(7,int(24+20*t),int(48+32*t)))
    for x in range(0,W,72):d.line((x,0,x,H),fill=(17,48,73))
    for y in range(0,H,85):d.line((0,y,W,y),fill=(17,48,73))
    d.rounded_rectangle((34,30,686,132),radius=24,fill=(12,53,90),outline=(58,125,175),width=2)
    d.text((360,81),"LÉO  &  LE PROF",anchor="mm",font=ft(35),fill="white")
    d.rounded_rectangle((34,154,686,226),radius=20,fill=(16,56,88))
    d.text((360,190),"3 QUESTIONS  •  3 RÉPONSES",anchor="mm",font=ft(25),fill=(235,244,252))
    panel(image,leo,47,279,speaker=="Léo",(255,203,72))
    panel(image,prof,375,279,speaker=="Le Prof",(70,225,233))
    d=ImageDraw.Draw(image)
    for name,cx,active,accent in [("LÉO",196,speaker=="Léo",(255,203,72)),("LE PROF",524,speaker=="Le Prof",(70,225,233))]:
        d.rounded_rectangle((cx-130,730,cx+130,789),radius=15,fill=accent if active else (32,73,105))
        d.text((cx,759),name,anchor="mm",font=ft(24),fill=(9,28,52) if active else "white")
    accent=(255,203,72) if speaker=="Léo" else (70,225,233)
    d.rounded_rectangle((33,836,687,1157),radius=25,fill=(12,49,81),outline=accent,width=4)
    if num == 4:
        d.rounded_rectangle((66,860,320,910),radius=14,fill=(215,56,62))
        d.text((193,884),"S'ABONNER",anchor="mm",font=ft(24),fill="white")
        d.text((659,884),"À DEMAIN !",anchor="rm",font=ft(18),fill=(193,229,239))
    else:
        d.rounded_rectangle((66,860,312,910),radius=14,fill=accent)
        d.text((189,884),f"QUESTION {num} / 3",anchor="mm",font=ft(23),fill=(7,27,50))
        d.text((659,884),"QUESTION" if speaker=="Léo" else "RÉPONSE",anchor="rm",font=ft(18),fill=(193,229,239))
    if num == 4:
        # Le texte dans une vidéo YouTube n'est pas cliquable.
        # On conserve le message parlé complet, mais l'écran final reste lisible.
        d.text((360,978),"UNE DÉCOUVERTE CHAQUE JOUR !",
               anchor="mm",font=ft(29),fill="white")
        d.text((360,1034),"Abonne-toi à Léo & le Prof",
               anchor="mm",font=ft(28),fill=(255,227,152))
        d.rounded_rectangle((89,1082,631,1138),radius=16,fill=(23,85,127))
        d.text((360,1110),"OUVRE NOTRE PROFIL POUR T'ABONNER",
               anchor="mm",font=ft(19),fill="white")
    else:
        size=37 if len(text)<57 else 29 if len(text)>125 else 33
        lines=wrap(d,text,ft(size),570)
        step=size+14;y=1030-(len(lines)-1)*step/2
        for line in lines:
            d.text((360,int(y)),line,anchor="mm",font=ft(size),fill="white");y+=step
    for n in range(3):
        d.rounded_rectangle((267+n*65,1192,315+n*65,1203),radius=5,fill=(255,203,72) if n<num else (61,97,121))
    d.text((360,1244),"SCIENCES  •  DÉCOUVERTES  •  CULTURE",anchor="mm",font=ft(18),fill=(197,220,235))
    image.save(path)

async def speak(text,voice,path,rate):
    # Échec visible si le TTS est inaccessible : jamais de mauvaise voix de secours.
    await Communicate(text,voice,rate=rate).save(str(path))

async def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="output_officiel")
    p.add_argument("--start",type=int,default=0)
    p.add_argument("--leo-voice",default="fr-FR-EloiseNeural")
    p.add_argument("--prof-voice",default="fr-FR-HenriNeural")
    args=p.parse_args()
    for name in ("leo.png","prof.png"):
        if not (AVATARS/name).is_file():
            raise FileNotFoundError(f"Portrait officiel manquant : {AVATARS/name}. Aucun personnage alternatif ne sera utilisé.")
    leo=Image.open(AVATARS/"leo.png").convert("RGB")
    prof=Image.open(AVATARS/"prof.png").convert("RGB")
    data=json.loads((ROOT/"questions.json").read_text(encoding="utf-8"))
    if len(data)<3: raise ValueError("Au moins 3 questions sont nécessaires")
    selected=[data[(args.start+i)%len(data)] for i in range(3)]
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    videos=[]
    for i,q in enumerate(selected,1):
        for marker,speaker,text,voice,rate in (
            ("q","Léo",q["question"],args.leo_voice,"+4%"),
            ("r","Le Prof",q["answer"],args.prof_voice,"-5%")):
            stem=f"{i}_{marker}"
            frame=out/(stem+".png");sound=out/(stem+".mp3");video=out/(stem+".mp4")
            render(leo,prof,speaker,text,i,frame)
            await speak(text,voice,sound,rate)
            cmd("-loop","1","-framerate","25","-i",frame,"-i",sound,
                "-c:v","libx264","-preset","veryfast","-pix_fmt","yuv420p",
                "-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",video)
            videos.append(video)
    # Invitation finale prononcée par le Prof ; même avatar officiel.
    cta_frame=out/"4_abonnement.png"
    cta_audio=out/"4_abonnement.mp3"
    cta_video=out/"4_abonnement.mp4"
    render(leo,prof,"Le Prof",SUBSCRIBE_MESSAGE,4,cta_frame)
    await speak(SUBSCRIBE_MESSAGE,args.prof_voice,cta_audio,"-5%")
    cmd("-loop","1","-framerate","25","-i",cta_frame,"-i",cta_audio,
        "-c:v","libx264","-preset","veryfast","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",cta_video)
    videos.append(cta_video)
    listing=out/"concat.txt"
    listing.write_text("".join(f"file '{v.name}'\n" for v in videos))
    final=out/"Leo_et_le_Prof_Officiel_Voix_Naturelles.mp4"
    cmd("-f","concat","-safe","0","-i",listing,"-c","copy","-movflags","+faststart",final)
    description=("🔎 Trois questions, trois réponses : découvrons le monde avec Léo & le Prof !\n\n"
                 "Abonne-toi pour une découverte chaque jour : " + SUBSCRIBE_URL + "\n"
                 "Ouvre notre profil YouTube et utilise le bouton S'abonner.\n\n"
                 "Sources des réponses :\n" +
                 "\n".join(q["source"] for q in selected) +
                 "\n\n#LeoEtLeProf #Sciences #CultureGenerale #Shorts")
    metadata={"published":False,"voice_engine":"edge-tts",
              "leo_voice":args.leo_voice,"prof_voice":args.prof_voice,
              "question_ids":[q["id"] for q in selected],
              "subscribe_message":SUBSCRIBE_MESSAGE,
              "subscribe_url":SUBSCRIBE_URL,
              "channel_url":CHANNEL_URL,
              "youtube_description":description,
              "requires_approval":True}
    (out/"metadata.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"youtube_description.txt").write_text(description,encoding="utf-8")
    print("Fichier de validation :",final)

if __name__=="__main__":
    asyncio.run(main())
