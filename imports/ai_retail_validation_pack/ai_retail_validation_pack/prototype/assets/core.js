(function(){
  const params = new URLSearchParams(location.search);
  const key = params.get('vertical') || 'garden';
  const cfg = window.VERTICALS[key] || window.VERTICALS.garden;
  document.body.dataset.theme = cfg.theme;
  document.title = cfg.brand + ' — Prototype';

  const $ = (id) => document.getElementById(id);
  $('wordmark').textContent = cfg.brand;
  $('navNote').textContent = cfg.navNote;
  $('eyebrow').textContent = cfg.eyebrow;
  $('headline').textContent = cfg.headline;
  $('subhead').textContent = cfg.subhead;
  $('advisorName').textContent = cfg.advisorName;
  $('proof1').textContent = cfg.proof[0];
  $('proof2').textContent = cfg.proof[1];
  $('proof3').textContent = cfg.proof[2];
  $('trustRow').innerHTML = cfg.trust.map(x=>`<span>${x}</span>`).join('');

  let step = 0;
  let answers = [];
  const conversation = $('conversation');
  const choices = $('choices');

  function addMessage(text, type='bot') {
    const d=document.createElement('div');
    d.className='msg '+type;
    d.textContent=text;
    conversation.appendChild(d);
    conversation.scrollTop=conversation.scrollHeight;
  }

  function ask(){
    const item=cfg.questions[step];
    addMessage(item.q,'bot');
    choices.innerHTML='';
    item.a.forEach(answer=>{
      const b=document.createElement('button');
      b.className='choice';
      b.textContent=answer;
      b.onclick=()=>{
        answers.push({question:item.q,answer});
        addMessage(answer,'user');
        choices.innerHTML='';
        step++;
        setTimeout(()=> step < cfg.questions.length ? ask() : showResult(), 220);
      };
      choices.appendChild(b);
    });
  }

  function showResult(){
    addMessage('I have enough to build a recommendation.','bot');
    const r=cfg.result;
    $('resultTitle').textContent=r.title;
    $('resultIntro').textContent=r.intro;
    $('bundle').innerHTML=r.bundle.map(([k,v])=>`<div class="bundle-row"><span>${k}</span><strong>${v}</strong></div>`).join('');
    $('total').textContent=r.total;
    $('resultNote').textContent=r.note;
    $('primaryAction').textContent=r.action;
    $('primaryAction').onclick=()=>alert('Prototype conversion event: connect this button to /api/leads, /api/cart or /api/quotes.');
    $('resultModal').classList.remove('hidden');
  }

  function restart(){
    step=0; answers=[]; conversation.innerHTML=''; choices.innerHTML='';
    $('resultModal').classList.add('hidden');
    addMessage(`I’ll keep this fast. ${cfg.questions.length} questions, then one clear recommendation.`,'bot');
    setTimeout(ask,180);
  }

  $('closeModal').onclick=()=>$('resultModal').classList.add('hidden');
  $('restart').onclick=restart;
  restart();
})();
