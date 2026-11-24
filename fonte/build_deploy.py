import re,shutil,os
src=open('build2.py').read()
ns={}; exec(src[:src.index("e=lambda p,m:")],ns); s=ns['s']; si=ns['si']
A='assets/'; D='deploy/assets/'; os.makedirs(D,exist_ok=True)
files={'__DIAMOND__':'diamond.png','__AP_LOGO__':'ap-logo.png','__ANA_MAIN__':'ana-hero-main.webp','__AP_LOGO_BIG__':'ap-logo-big.png',
 '__ANA_DOCENTE__':'ana-docente.jpg','__SB_LOGO__':'sb-logo.png','__HERO_BOKEH__':'hero-bokeh.jpg','__ANA_TURMA__':'ana-turma.jpg',
 '__ANA_BLAZER__':'ana-blazer.jpg','__ANA_VEST__':'ana-vest.webp','__ANA_HERO__':'ana-hero.webp',
 '__ANA_BRANCO__':'ana-branco.jpg','__DIA_PATTERN_W__':'diamond-pattern-w.svg','__DIA_PATTERN__':'diamond-pattern.svg'}
og='''<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:url" content="https://skin-beauty-metodo.stayai.space/">
<meta property="og:title" content="Skin Beauty Método | Curso presencial de clareamento íntimo">
<meta property="og:description" content="Formação presencial para profissionais habilitadas: raciocínio clínico e tratamentos personalizados de manchas íntimas. 30 e 31 de janeiro de 2027, Savassi, BH. Apenas 5 vagas.">
<meta property="og:image" content="https://skin-beauty-metodo.stayai.space/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">'''
def fix(s,preload=True):
    s=s.replace('__DIAMOND_FAV__','assets/favicon.png')
    for k,f in files.items():
        if k in s: shutil.copy(A+f,D+f); s=s.replace(k,'assets/'+f)
    s=re.sub(r'data-img="(ANA_[A-Z]+)" src="data:image/gif;base64,[^"]+"',lambda m:'src="assets/'+files['__'+m.group(1)+'__']+'" loading="lazy"',s)
    s=re.sub(r"var IMGS=\{[^}]*\};\ndocument\.querySelectorAll\('img\[data-img\]'\)[^\n]*\n","",s)
    tag=og+('\n<link rel="preload" as="image" href="assets/ana-hero-main.webp">' if preload else '')
    s=s.replace('<link rel="preconnect" href="https://fonts.googleapis.com">',tag+'\n<link rel="preconnect" href="https://fonts.googleapis.com">',1)
    assert 'data:image/jpeg' not in s and 'data:image/webp' not in s and 'IMGS' not in s
    assert not re.findall(r'__[A-Z_]{3,}__',s), re.findall(r'__[A-Z_]{3,}__',s)[:5]
    return s
s=fix(s); si=fix(si,False).replace('<meta property="og:url" content="https://skin-beauty-metodo.stayai.space/">','<meta property="og:url" content="https://skin-beauty-metodo.stayai.space/inscricao.html">')
import glob
for f in glob.glob(A+'res-*'): shutil.copy(f,D)
open('deploy/index.html','w',encoding='utf8').write(s); open('deploy/inscricao.html','w',encoding='utf8').write(si)
print(len(s)//1024,'KB /',len(si)//1024,'KB')
