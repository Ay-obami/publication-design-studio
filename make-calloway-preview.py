from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
root=Path('/home/ayobami/Documents/publication-design-studio-buyer-upgrade/process-assets/calloway')
imgs=[Image.open(root/'rendered'/f'source-page-{n}.png').convert('RGB') for n in (1,2,4)]
target_h=1180
scaled=[]
for im in imgs:
    w=round(im.width*target_h/im.height)
    scaled.append(im.resize((w,target_h),Image.Resampling.LANCZOS))
margin=60; gap=38
W=sum(i.width for i in scaled)+gap*2+margin*2
H=target_h+margin*2
canvas=Image.new('RGB',(W,H),(233,231,226))
draw=ImageDraw.Draw(canvas)
x=margin
for im in scaled:
    shadow=Image.new('RGBA',(im.width+24,im.height+24),(0,0,0,0))
    ImageDraw.Draw(shadow).rectangle((12,12,im.width+12,im.height+12),fill=(0,0,0,38))
    canvas.paste(shadow.convert('RGB'),(x-12,margin-12))
    canvas.paste(im,(x,margin))
    x+=im.width+gap
canvas.save(root/'raw-source-preview.webp','WEBP',quality=86,method=6)
print(root/'raw-source-preview.webp',canvas.size)
