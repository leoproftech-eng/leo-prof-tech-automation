"""Studio v2: voix françaises plus naturelles et montage vertical dynamique.
Prototype de qualité améliorée. Ne publie jamais sur YouTube.
"""
import asyncio, json, subprocess, argparse, textwrap
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from edge_tts import Communicate
import shutil

BASE=Path(__file__).parent
W,H=720,1280
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def ff(*args):
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*map(str,args)],check=True)

def font(n,bold=False): return ImageFont.truetype(BOLD if bold else FONT,n)

def wrap(d,t,f,width):
    groups=[];current=''
    for word in t.split():
        trial=(current+' '+word).strip()
        if d.textbbox((0,0),trial,font=f)[2]<=width:current=trial
        else:
            if current:groups.append(current)
            current=word
    if current:groups.append(current)
    return groups

def frame(name,sentence,category,num,dest):
    im=Image.new('RGB',(W,H),(7,20,47));d=ImageDraw.Draw(im)
    for y in range(H):
        c=int(29*y/H)
        d.line((0,y,W,y),fill=(7,21+c,49+c))
    for x in range(40,720,80):d.line((x,0,x,H),fill=(16,51,85),width=1)
    for y in range(70,H,100):d.line((0,y,720,y),fill=(16,51,85),width=1)
    accent='#FFCD43' if name=='Léo' else '#4BE2EF'
    d.rounded_rectangle((38,45,682,132),radius=25,fill='#0D3861',outline='#2987B1',width=3)
    d.text((360,91),'LÉO & LE PROF TECH',font=font(33,True),anchor='mm',fill='white')
    d.rounded_rectangle((42,165,678,235),radius=21,fill=accent)
    d.text((360,200),category.upper()+'  •  ÉPISODE '+str(num),font=font(23,True),anchor='mm',fill='#07162F')
    # Illustration-avatar flat 2D simple et cohérente; assets illustrés à remplacer par avatars officiels
    cx,cy=360,470
    skin='#A75F39' if name=='Léo' else '#8F4E32'
    shirt='#1976D2' if name=='Léo' else '#EAF6FE'
    d.ellipse((cx-185,cy+80,cx+185,cy+460),fill=shirt)
    d.rounded_rectangle((cx-50,cy+75,cx+50,cy+215),radius=20,fill=skin)
    d.ellipse((cx-145,cy-135,cx+145,cy+190),fill=skin,outline='#442A29',width=6)
    hair='#171523' if name=='Léo' else '#A6ADB6'
    d.pieslice((cx-151,cy-169,cx+151,cy-5),180,360,fill=hair)
    if name=='Léo':
        for xp in range(cx-120,cx+130,39):d.ellipse((xp-24,cy-172,xp+35,cy-106),fill=hair)
    else:
        d.arc((cx-96,cy-10,cx+100,cy+180),3,177,fill='#D3D9E1',width=19)
        for xp in (cx-70,cx+72):d.ellipse((xp-49,cy-23,xp+49,cy+47),outline='#13233B',width=9)
        d.line((cx-22,cy+9,cx+22,cy+9),fill='#13233B',width=8)
    for xp in (cx-64,cx+64):
        d.ellipse((xp-20,cy+8,xp+21,cy+52),fill='white')
        d.ellipse((xp-3,cy+18,xp+11,cy+37),fill='#15243A')
    d.arc((cx-54,cy+59,cx+54,cy+117),0,180,fill='white',width=9)
    d.rounded_rectangle((70,800,650,873),radius=18,fill=accent)
    d.text((360,837),name.upper(),font=font(42,True),anchor='mm',fill='#06162B')
    d.rounded_rectangle((49,898,671,1165),radius=25,fill='#0D3155',outline='#367EA4',width=3)
    fs=font(32 if len(sentence)<110 else 27,True)
    words=wrap(d,sentence,fs,550)
    if len(words)>7:raise ValueError('Réponse trop longue pour la mise en page: '+str(len(words))+' lignes')
    step=44 if len(sentence)<110 else 41
    y=1020-(len(words)-1)*step/2
    for line in words:d.text((360,y),line,font=fs,anchor='mm',fill='white');y+=step
    d.text((360,1212),'UNE QUESTION  •  UNE RÉPONSE  •  UNE DÉCOUVERTE',font=font(17,True),anchor='mm',fill='#D0E9FA')
    im.save(dest)

async def audio(text,voice,path):
    try:
        await Communicate(text,voice,rate='+4%').save(str(path))
    except Exception as exc:
        # Mode dégradé : une coupure du service TTS ne doit pas casser le pilote.
        espeak=shutil.which('espeak-ng')
        if not espeak:
            raise RuntimeError('TTS indisponible et moteur de secours absent') from exc
        wav=path.with_suffix('.wav')
        subprocess.run([espeak,'-v','fr','-s','150','-w',str(wav),text],check=True)
        ff('-i',wav,'-codec:a','libmp3lame','-qscale:a','3',path)
        print('Voix de secours utilisée :',exc)

async def main():
    ap=argparse.ArgumentParser();ap.add_argument('--id',default='auto');ap.add_argument('--output',default='output');args=ap.parse_args()
    data=json.loads((BASE/'questions.json').read_text())
    idx=datetime.now().date().toordinal()%len(data)
    q=next((v for v in data if v['id']==args.id),data[idx]) if args.id!='auto' else data[idx]
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    scenes=[('Léo',q['question'],'fr-FR-EloiseNeural'),('Le Prof',q['answer'],'fr-FR-HenriNeural')]
    videos=[]
    for i,(name,speech,voice) in enumerate(scenes):
        still=out/f'frame_{i}.png';sound=out/f'audio_{i}.mp3';clip=out/f'clip_{i}.mp4'
        frame(name,speech,q['category'],q['id'][1:],still)
        await audio(speech,voice,sound)
        # Légère animation de zoom et sous-titres intégrés dans la composition.
        ff('-loop','1','-framerate','25','-i',still,'-i',sound,
           '-vf','zoompan=z=min(zoom+0.0003\\,1.05):d=1:s=720x1280:fps=25',
           '-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p',
           '-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',clip)
        videos.append(clip)
    manifest=out/'concat.txt';manifest.write_text(''.join("file '"+p.name+"'\\n" for p in videos))
    video=out/(q['id']+'_studio_v2.mp4')
    ff('-f','concat','-safe','0','-i',manifest,'-c','copy','-movflags','+faststart',video)
    (out/'metadata.json').write_text(json.dumps({'title':q['question']+' | Léo & le Prof Tech #Shorts','source':q['source'],'status':'NOT_PUBLISHED'},ensure_ascii=False,indent=2))
    print('Généré:',video)
if __name__=='__main__': asyncio.run(main())
