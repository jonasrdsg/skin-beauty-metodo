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
PRIVJS='''  /* Aviso de privacidade */
  var dlg=$('#privacidade');
  function openPriv(e){ e.preventDefault(); if(!dlg) return; if(dlg.showModal) dlg.showModal(); else dlg.setAttribute('open',''); }
  ['#open-priv','#open-priv-2'].forEach(function(q){ var a=$(q); if(a) a.addEventListener('click',openPriv); });
  var cp=$('#close-priv'); if(cp) cp.addEventListener('click',function(){ dlg.close ? dlg.close() : dlg.removeAttribute('open'); });
  if(dlg) dlg.addEventListener('click',function(e){ if(e.target===dlg && dlg.close) dlg.close(); });
'''
for k,v in [('__DIALOG__',DIALOG),('__FORMJS__',PRIVJS),('/*__FORM_CSS__*/',FORM_CSS),('/*__DIALOG_CSS__*/',DIALOG_CSS)]:
    assert k in s,k; s=s.replace(k,v)
# ---- página de inscrição (gerada a partir do index) ----
si=s.replace('<title>Skin Beauty Método | Curso presencial de clareamento íntimo com Ana Paula Estética</title>','<title>Seu interesse na formação | Skin Beauty Método</title>')
si=si.replace('<meta name="description"','<meta name="robots" content="noindex">\n<meta name="description"',1)
i=si.rindex('</style>'); si=si[:i]+open('insc.css',encoding='utf8').read()+si[i:]
a=si.index('<main id="topo">'); z=si.index('</main>')+7; si=si[:a]+open('insc_main.html',encoding='utf8').read()+si[z:]
si=re.sub(r'\n<div class="sticky" id="sticky">.*?</div>\n','\n',si,flags=re.S)
si=re.sub(r'(<ul class="nav__links" id="links">.*?</ul>)',lambda m:m.group(1).replace('href="#','href="index.html#'),si,flags=re.S)
si=si.replace('<a class="brand" href="#topo"','<a class="brand" href="index.html"')
si=si.replace('<a class="btn" href="inscricao.html"><span>Quero garantir minha vaga</span>','<a class="btn" href="index.html"><span>Voltar à página</span>')
sa=si.index('var IMGS='); sz=si.rindex('</script>')
si=si[:sa]+'''(function(){
  var d=document; d.documentElement.classList.add('js');
  var $=function(s){return d.querySelector(s)};
  function track(ev){ try{ (window.dataLayer=window.dataLayer||[]).push({event:ev}); }catch(e){} }
  var head=$('#head'), prog=$('#prog'), tick=0;
  function onScroll(){ tick=0; var y=window.scrollY; if(head) head.classList.toggle('is-stuck', y>40);
    if(prog) prog.style.setProperty('--p', Math.min(1,y/Math.max(1,d.documentElement.scrollHeight-innerHeight)).toFixed(4)); }
  addEventListener('scroll',function(){ if(!tick) tick=requestAnimationFrame(onScroll); },{passive:true}); onScroll();
'''+PRIVJS+open('insc.js',encoding='utf8').read()+'})();\n'+si[sz:]
e=lambda p,m:'data:'+m+';base64,'+base64.b64encode(open(p,'rb').read()).decode()
fav=Image.open('assets/diamond.png').convert('RGBA'); c=Image.new('RGBA',(96,96),(132,82,64,255)); c.alpha_composite(fav.resize((72,43)),(12,27)); bio=io.BytesIO(); c.save(bio,'PNG')
def fill(s):
  s=s.replace('__DIAMOND_FAV__','data:image/png;base64,'+base64.b64encode(bio.getvalue()).decode())
  s=s.replace('__DIAMOND__',e('assets/diamond.png','image/png')).replace('__AP_LOGO__',e('assets/ap-logo.png','image/png'))
  s=s.replace('__ANA_MAIN__',e('assets/ana-hero-main.webp','image/webp'))
  s=s.replace('__AP_LOGO_BIG__',e('assets/ap-logo-big.png','image/png'))
  s=s.replace('__ANA_DOCENTE__',e('assets/ana-docente.jpg','image/jpeg')).replace('__SB_LOGO__',e('assets/sb-logo.png','image/png'))
  s=s.replace('__HERO_BOKEH__',e('assets/hero-bokeh.jpg','image/jpeg'))
  s=s.replace('__ANA_TURMA__',e('assets/ana-turma.jpg','image/jpeg'))
  s=s.replace('__ANA_VEST__',e('assets/ana-vest.webp','image/webp')).replace('__ANA_BLAZER__',e('assets/ana-blazer.jpg','image/jpeg')).replace('__ANA_HERO__',e('assets/ana-hero.webp','image/webp'))
  s=s.replace('__ANA_BRANCO__',e('assets/ana-branco.jpg','image/jpeg')).replace('__DIA_PATTERN_W__',e('assets/diamond-pattern-w.svg','image/svg+xml')).replace('__DIA_PATTERN__',e('assets/diamond-pattern.svg','image/svg+xml'))
  assert not re.findall(r'__[A-Z_]{3,}__',s), re.findall(r'__[A-Z_]{3,}__',s)[:5]
  return s
s=fill(s); si=fill(si)
open('inscricao.html','w',encoding='utf8').write(si)
open('index.html','w',encoding='utf8').write(s); print(len(s)//1024,'KB')
