  /* Formulário de interesse */
  var form=$('#form'), err=$('#err'), started=false, whats=$('#whats'), sel=$('#formacao'), block=$('#block'), go=$('#go');
  form.addEventListener('focusin',function(){ if(!started){ started=true; track('interesse_inicio'); } });
  sel.addEventListener('change',function(){ var no=sel.value==='Outra'; block.classList.toggle('on',no); go.disabled=no; });
  whats.addEventListener('input',function(){
    var v=whats.value.replace(/\D/g,'').slice(0,11), o='';
    if(v.length>0) o='('+v.slice(0,2);
    if(v.length>=3) o+=') '+v.slice(2, v.length>10?7:6);
    if(v.length>=7) o+='-'+v.slice(v.length>10?7:6);
    whats.value=o;
  });
  function fail(msg,el){ err.textContent=msg; err.classList.add('on'); if(el&&el.focus) el.focus(); }
  form.addEventListener('submit',function(e){
    e.preventDefault(); err.classList.remove('on');
    var f=form.elements;
    if(f.nome.value.trim().split(/\s+/).length<2) return fail('Informe seu nome completo.',f.nome);
    if(whats.value.replace(/\D/g,'').length<10) return fail('Informe um WhatsApp válido, com DDD.',whats);
    if(f.cidade.value.trim().length<3) return fail('Informe sua cidade e estado.',f.cidade);
    if(!f.formacao.value) return fail('Selecione sua formação profissional.',f.formacao);
    if(f.formacao.value==='Outra') return fail('Esta formação é exclusiva para as formações listadas.',f.formacao);
    if(!f.experiencia.value) return fail('Selecione seu tempo de atuação na área.',f.experiencia);
    if(!f.disponibilidade.value) return fail('Informe sua disponibilidade para os dias 30 e 31 de janeiro de 2027.');
    if(!f.consentimento.checked) return fail('Para continuar, autorize o uso dos dados conforme o aviso de privacidade.',f.consentimento);
    var data={}; new FormData(form).forEach(function(v,k){ data[k]=v; });
    data.enviado_em=new Date().toISOString(); data.pagina=location.href;
    var url='https://wa.me/'+CONFIG.whatsapp+'?text='+encodeURIComponent(CONFIG.mensagem);
    var win=window.open(url,'_blank'); try{ if(win) win.opener=null; }catch(_){}
    var save=CONFIG.webhook ? fetch(CONFIG.webhook,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data),keepalive:true}).catch(function(){}) : Promise.resolve();
    track('interesse_envio');
    save.then(function(){
      form.style.display='none';
      var done=$('#done'); done.classList.add('on'); $('#wa-again').href=url; done.focus();
      if(!win) location.href=url;
    });
  });
