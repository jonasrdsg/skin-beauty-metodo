import base64,io,re
from PIL import Image
o=open('src.html',encoding='utf8').read()
def cut(a,b,inc=False,src=o,last=False):
    i=src.index(a); j=(src.rindex(b) if last else src.index(b,i)); return src[i:j+(len(b) if inc else 0)]
FORM=cut('<div class="form rv"','\n  </div>\n</section>\n</main>')
faqsec=cut('<section class="faq"','</section>')
FAQ=faqsec[faqsec.index('<details open>'):faqsec.rindex('</details>')+10]
DIALOG=cut('<!-- Aviso de privacidade: TEXTO-BASE','</dialog>',True)
js=o[o.index('<script>'):]
FORMJS=js[js.index('  /* Aviso de privacidade */'):js.rindex('})();')]
FORM_CSS=cut('.form{background:var(--paper)','@media(max-width:900px){.apply__grid')
DIALOG_CSS=cut('dialog{border:0','.dlg .btn{margin-top:24px}',True)
s=open('src2.html',encoding='utf8').read()
s=re.sub(r'(\d)\.(\d)00\b',r'\1.\2',s)  # normaliza decimais dos ícones
for k,v in [('__FORM__',FORM),('__FAQ__',FAQ),('__DIALOG__',DIALOG),('__FORMJS__',FORMJS),('/*__FORM_CSS__*/',FORM_CSS),('/*__DIALOG_CSS__*/',DIALOG_CSS)]:
    assert k in s,k; s=s.replace(k,v)
e=lambda p,m:'data:'+m+';base64,'+base64.b64encode(open(p,'rb').read()).decode()
fav=Image.open('assets/diamond.png').convert('RGBA'); c=Image.new('RGBA',(96,96),(132,82,64,255)); c.alpha_composite(fav.resize((72,43)),(12,27)); bio=io.BytesIO(); c.save(bio,'PNG')
s=s.replace('__DIAMOND_FAV__','data:image/png;base64,'+base64.b64encode(bio.getvalue()).decode())
s=s.replace('__DIAMOND__',e('assets/diamond.png','image/png')).replace('__AP_LOGO__',e('assets/ap-logo.png','image/png'))
s=s.replace('__ANA_MAIN__',e('assets/ana-hero-main.webp','image/webp'))
s=s.replace('__AP_LOGO_BIG__',e('assets/ap-logo-big.png','image/png'))
s=s.replace('__ANA_DOCENTE__',e('assets/ana-docente.jpg','image/jpeg')).replace('__SB_LOGO__',e('assets/sb-logo.png','image/png'))
s=s.replace('__HERO_BOKEH__',e('assets/hero-bokeh.jpg','image/jpeg'))
s=s.replace('__ANA_TURMA__',e('assets/ana-turma.jpg','image/jpeg'))
s=s.replace('__ANA_VEST__',e('assets/ana-vest.webp','image/webp')).replace('__ANA_BLAZER__',e('assets/ana-blazer.jpg','image/jpeg')).replace('__ANA_HERO__',e('assets/ana-hero.webp','image/webp'))
assert not re.findall(r'__[A-Z_]{3,}__',s), re.findall(r'__[A-Z_]{3,}__',s)[:5]
open('index.html','w',encoding='utf8').write(s); print(len(s)//1024,'KB')
