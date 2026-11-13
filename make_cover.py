from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
R=Path(__file__).resolve().parents[1]
W,H=1600,900
im=Image.new('RGB',(W,H),'#071322')
d=ImageDraw.Draw(im)
for y in range(H):
 t=y/H
 c=(int(7+3*t),int(19+11*t),int(34+16*t))
 d.line((0,y,W,y),fill=c)
for x in range(0,W,57):d.line((x,0,x,H),fill='#0d2337',width=1)
for y in range(0,H,57):d.line((0,y,W,y),fill='#0d2337',width=1)
d.ellipse((-120,-250,590,460),fill='#0b2636')
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fontbold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def f(s,b=False):return ImageFont.truetype(fontbold if b else font,s)
# Screenshot panel with soft shadow
src=Image.open(R/'screenshots/01_executive_linkedin.jpg').convert('RGB')
crop=src.crop((168,2,1600,1150))
crop.thumbnail((880,710),Image.Resampling.LANCZOS)
panel=Image.new('RGB',(905,745),'#102537');pd=ImageDraw.Draw(panel);pd.rounded_rectangle((0,0,904,744),radius=20,fill='#102537',outline='#285064',width=2)
panel.paste(crop,((905-crop.width)//2,(745-crop.height)//2))
mask=Image.new('L',panel.size,0);md=ImageDraw.Draw(mask);md.rounded_rectangle((0,0,904,744),radius=20,fill=255)
shadow=Image.new('RGBA',(960,800),(0,0,0,0));sd=ImageDraw.Draw(shadow);sd.rounded_rectangle((12,15,920,759),radius=25,fill='#000000aa');shadow=shadow.filter(ImageFilter.GaussianBlur(18))
im.paste(shadow,(665,70),shadow)
im.paste(panel,(672,75),mask)
d=ImageDraw.Draw(im)
d.rounded_rectangle((64,73,451,109),radius=18,fill='#123a3b',outline='#22645d',width=1)
d.ellipse((81,86,91,96),fill='#64f2bf')
d.text((103,82),'INTERACTIVE ANALYTICS PORTFOLIO',font=f(15,True),fill='#8efad3')
d.text((64,148),'FINSIGHT',font=f(71,True),fill='#f0f8ff')
d.text((545,153),'.',font=f(70,True),fill='#64f2bf')
d.text((66,255),'FINTECH PRODUCT',font=f(42,True),fill='#d9eafd')
d.text((66,318),'INTELLIGENCE',font=f(42,True),fill='#d9eafd')
d.rounded_rectangle((66,401,305,409),radius=3,fill='#64f2bf')
d.text((66,438),'Growth  •  Activation',font=f(25),fill='#9bc6d8')
d.text((66,477),'Retention  •  Experiments',font=f(25),fill='#9bc6d8')
d.text((66,516),'Predictive Analytics',font=f(25),fill='#9bc6d8')
for x,label in [(66,'07 DASHBOARD PAGES'),(273,'05 GLOBAL FILTERS'),(489,'100% SYNTHETIC')]:
 if x>540:continue
 d.rounded_rectangle((x,608,x+198,664),radius=9,fill='#123145',outline='#24566b')
 d.text((x+13,628),label,font=f(13,True),fill='#a0f0d9')
d.text((65,744),'HTML  /  PLOTLY  /  EXCEL  /  PYTHON  /  ML',font=f(15,True),fill='#88a9ba')
d.text((65,817),'SANJIBAN DAS  |  BUSINESS INTELLIGENCE & PRODUCT ANALYTICS',font=f(14,True),fill='#d9ecf4')
im.save(R/'screenshots/00_linkedin_project_cover.jpg',quality=92,subsampling=0)
print('saved cover',R/'screenshots/00_linkedin_project_cover.jpg')
