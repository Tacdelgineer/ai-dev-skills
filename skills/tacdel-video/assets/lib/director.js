'use strict';
/* =====================================================================
   DIRECTOR MODE — record by hand, with the camera on the keyboard.

   Usage: load after riso-core.js, then call installDirector() once the rooms exist:

     installDirector({
       rooms:   () => ['street', 'lab', 'vault'],   // order for 1-9, 0 and for , .
       current: () => 'lab',                         // the room on screen, or null
       goRoom:  id => goToRoom(id, 700),             // fly the camera to a room
       pan:     (dx, dy) => panBy(dx, dy),           // screen pixels; the page divides by zoom
       zoom:    f => zoomBy(f),                      // multiply the zoom by f
       rate:    r => { RATE = r },                   // world speed: 1, or .25 while Shift is held
       extra:   [['B', 'the whole building', () => building()]],
       legend:  document.getElementById('legend'),   // optional: filled with the key list
     });

   Keys: 1-9 and 0 jump to the first ten rooms, , and . step through all of them, arrows or
   WASD pan, + and - zoom, hold Shift for slow motion and a finer pan, H hides every element
   with class "ui" (the page's CSS: body.clean .ui{display:none}), F toggles fullscreen,
   P saves the canvas as a PNG. `extra` adds project keys (a single character each).

   Every key only moves the camera, the clock's speed or the UI. None can change a number, so
   a hand-recorded take shows exactly what an automatic render would.
   ===================================================================== */
function installDirector(o){
  const PAN=120,FINE=28,ZOOM=1.2;
  const rooms=()=>(o.rooms&&o.rooms())||[];
  const keys=[
    ['1 - 9, 0','the first ten rooms'],
    [', .','the room before / after'],
    ['← ↑ ↓ →','pan (also W A S D)'],
    ['+  -','zoom in / out'],
    ['SHIFT (hold)','slow motion, and a fine pan'],
    ...(o.extra||[]).map(([k,what])=>[k,what]),
    ['H','hide everything for a clean take'],
    ['F','fullscreen'],
    ['P','save this frame as a png'],
  ];
  if(o.legend)o.legend.innerHTML=keys.map(([k,w])=>`<b>${k}</b><span>${w}</span>`).join('');

  const typing=e=>{const t=e.target;return t&&(t.isContentEditable||/^(TEXTAREA|SELECT)$/.test(t.tagName)||
    (t.tagName==='INPUT'&&!/^(range|button|checkbox)$/.test(t.type)))};
  const setClean=on=>document.body.classList.toggle('clean',on);

  addEventListener('keydown',e=>{
    if(e.key==='Shift'){o.rate&&o.rate(.25);return}
    if(e.metaKey||e.ctrlKey||e.altKey||typing(e))return;
    const k=e.key,lk=k.toLowerCase(),list=rooms(),step=e.shiftKey?FINE:PAN;
    const done=()=>{e.preventDefault();e.stopPropagation()};
    const digit='1234567890'.indexOf(k);
    if(digit>=0&&k!==' '){if(digit<list.length){o.goRoom(list[digit]);done()}return}
    if(k===','||k==='.'){
      if(!list.length)return;
      const here=o.current?list.indexOf(o.current()):-1;
      const i=((here<0?0:here+(k==='.'?1:-1))+list.length)%list.length;
      o.goRoom(list[i]);done();return;
    }
    if(lk==='arrowleft'||lk==='a'){o.pan(-step,0);done();return}
    if(lk==='arrowright'||lk==='d'){o.pan(step,0);done();return}
    if(lk==='arrowup'||lk==='w'){o.pan(0,-step);done();return}
    if(lk==='arrowdown'||lk==='s'){o.pan(0,step);done();return}
    if(k==='+'||k==='='){o.zoom(ZOOM);done();return}
    if(k==='-'||k==='_'){o.zoom(1/ZOOM);done();return}
    if(lk==='h'){setClean(!document.body.classList.contains('clean'));done();return}
    if(lk==='f'){
      if(document.fullscreenElement)document.exitFullscreen();
      else if(document.documentElement.requestFullscreen)document.documentElement.requestFullscreen();
      done();return;
    }
    if(lk==='p'){
      const cv=document.querySelector('canvas');if(!cv)return;
      cv.toBlob(b=>{const a=document.createElement('a');a.href=URL.createObjectURL(b);
        a.download=(document.title||'frame').replace(/[^\w.-]+/g,'_')+'.png';a.click()});
      done();return;
    }
    for(const [key,,fn] of o.extra||[])if(fn&&lk===String(key).toLowerCase()){fn();done();return}
  });
  addEventListener('keyup',e=>{if(e.key==='Shift')o.rate&&o.rate(1)});
  addEventListener('blur',()=>{o.rate&&o.rate(1)});
  return keys;
}
