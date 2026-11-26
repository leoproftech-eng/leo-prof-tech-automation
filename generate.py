"""Générateur de Shorts hors abonnement : Pillow + eSpeak + FFmpeg."""
import argparse, json, shutil, subprocess
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent
W,H=720,1280

def command(*args):
    subprocess.run([str(x) for x in args], check=True, stdout=subprocess.DEVNULL)

def ft(size,bold=False):
    suffix='-Bold' if bold else ''
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+suffix+'.ttf',size)

def lines(draw,text,font,maxwidth):
    out=[]; line=''
    for word in text.split():
        t=(line+' '+word).strip()
        if draw.textbbox((0,0),t,font=font)[2]<=maxwidth:line=t
        else:
            if line:out.append(line)
            line=word
    if line:out.append(line)
    return out

def avatar(im,who):
    d=ImageDraw.Draw(im)
    skin=(162,86,50) if who=='Léo' else (127,70,41)
    dark=(30,25,31); grey=(165,174,186)
    jacket=(32,119,219) if who=='Léo' else (240,245,253)
    d.ellipse((144,470,576,875),fill=jacket,outline=(30,74,116),width=10)
    d.rounded_rectangle((322,425,401,545),radius=20,fill=skin)
    d.ellipse((212,222,508,552),fill=skin,outline=(66,43,37),width=6)
    d.ellipse((208,209,517,365),fill=dark if who=='Léo' else grey)
    if who=='Léo':
        for x in range(225,495,44):d.ellipse((x-24,194,x+40,281),fill=dark)
    else:
        d.arc((258,406,466,536),0,170,fill=grey,width=23)
        for x in (280,404):d.ellipse((x-41,357,x+40,429),outline=(20,37,57),width=8)
        d.line((321,387,362,387),fill=(20,37,57),width=8)
    for x in (292,425):
        d.ellipse((x-21,353,x+21,394),fill='white')
        d.ellipse((x-5,362,x+9,381),fill=(15,27,37))
    d.arc((303,404,425,488),0,170,fill=(252,240,226),width=10)

def still(person,speech,path):
    im=Image.new('RGB',(W,H),(8,33,73));d=ImageDraw.Draw(im)
    for x in range(0,W,68):d.line((x,0,x-190,H),fill=(19,61,103),width=2)
    d.rounded_rectangle((24,24,696,1250),radius=32,outline=(49,146,201),width=3)
    d.rounded_rectangle((52,56,668,139),radius=22,fill=(13,74,122))
    d.text((W//2,99),'LÉO & LE PROF',font=ft(36,True),anchor='mm',fill='white')
    d.rounded_rectangle((75,163,645,697),radius=34,fill=(234,242,250))
    avatar(im,person);d=ImageDraw.Draw(im)
    badge=(252,185,37) if person=='Léo' else (66,203,241)
    d.rounded_rectangle((73,734,647,818),radius=25,fill=badge)
    d.text((W//2,777),person.upper()+' PARLE',font=ft(42,True),anchor='mm',fill=(8,31,62))
    d.rounded_rectangle((55,846,665,1160),radius=28,fill=(14,54,92))
    f=ft(35 if len(speech)<110 else 30,True)
    seg=lines(d,speech,f,530)
    lh=49 if len(speech)<110 else 44
    y=1000-len(seg)*lh//2
    for line in seg:d.text((W//2,y),line,font=f,anchor='mt',fill='white');y+=lh
    d.text((W//2,1200),'UNE QUESTION · UNE RÉPONSE · UNE DÉCOUVERTE',font=ft(17,True),anchor='mm',fill=(173,219,251))
    im.save(path)

def main():
    p=argparse.ArgumentParser();p.add_argument('--id',default='q001');p.add_argument('--output',default='output');a=p.parse_args()
    questions=json.loads((ROOT/'questions.json').read_text(encoding='utf-8'))
    selected_id=(questions[datetime.now(ZoneInfo('America/Toronto')).date().toordinal()%len(questions)]['id'] if a.id=='auto' else a.id)
    q=next((q for q in questions if q['id']==selected_id),None)
    if q is None:raise SystemExit('Question inconnue: '+a.id)
    out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
    espeak=shutil.which('espeak-ng') or shutil.which('espeak')
    if not espeak:raise SystemExit('eSpeak manquant')
    rendered=[]
    for n,(who,speech,voice,speed) in enumerate([('Léo',q['question'],'fr+f3','162'),('Le Prof',q['answer'],'fr+m3','148')]):
        stillfile=out/f'scene{n}.png';audio=out/f'scene{n}.wav';video=out/f'scene{n}.mp4'
        still(who,speech,stillfile)
        command(espeak,'-v',voice,'-s',speed,'-w',audio,speech)
        command('ffmpeg','-y','-loglevel','error','-loop','1','-framerate','24','-i',stillfile,'-i',audio,'-c:v','libx264','-preset','ultrafast','-tune','stillimage','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','44100','-shortest',video)
        rendered.append(video)
    manifest=out/'segments.txt'
    manifest.write_text(''.join("file '"+f.name+"'\n" for f in rendered),encoding='utf-8')
    result=out/(q['id']+'_Leo_et_le_Prof.mp4')
    command('ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',manifest,'-c','copy','-movflags','+faststart',result)
    metadata={'title':q['question']+' | Léo & le Prof #Shorts','description':q['answer']+'\nSource : '+q['source']+'\n#LeoEtLeProf #Shorts','status':'pilot_not_published'}
    (out/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Vidéo générée :',result)

if __name__=='__main__':main()
