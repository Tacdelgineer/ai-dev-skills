/* 00 · Cold open. Payoff first (2 s lead before the first word), then the fake, then the real log beside it. */
const K = { looks: cue('This page looks like'), made: cue('Every number on it'), read: cue('The agent read it'), wrote: cue('Here is what it wrote') };
const SHEET = { x: 560, y: 150, w: 800, h: 700 };
const sheetShot = (lt, t, o = {}) => {
  PC.piece(PC.rect(SHEET.x, SHEET.y, SHEET.w, SHEET.h, 6), PC.C.cream);
  PC.text(D.fake.title, SHEET.x + 40, SHEET.y + 80, 34, PC.C.ink, 'left', 900);
  D.fake.body.split('\n').forEach((l, i) => PC.text(l, SHEET.x + 40, SHEET.y + 180 + i * 56, 30, PC.C.ink, 'left', 600, FONT.mono));
  if (o.stamp) PC.stamp('PLANTED', SHEET.x + SHEET.w * .62, SHEET.y + SHEET.h * .78, -.12, (t - o.stamp) / .35, 80);
  fakeLabel(960, SHEET.y + SHEET.h + 70);                                             // outside the fake, the whole time
};
// the payoff, before the voice starts: the real call on the fake page
shot(0, 'crt', 'payoff: the call', (lt) => {
  CR.statusBar(`${D.call.agent} · REAL CALL`, 'place_paper_bet');
  CR.tx(`${D.call.side}  $${D.call.stake}`, 320, 150, 56, CR.C.gh, { wt: 700, align: 'center' });
  if (lt > .8) CR.tx('on a page that was made up', 320, 230, 22, CR.C.g, { align: 'center' });
});
shot(K.looks, 'paper', 'the fake sheet', (lt, t) => sheetShot(lt, t, { stamp: K.made }));
shot(K.read, 'riso', 'what it wrote', (lt) => {
  R.mono(`${D.call.agent} · ITS OWN WORDS`, 960, 300, 34, R.C.dim, 'center', 800);
  R.mono(`"${D.call.quote}"`, 960, 520, 44, R.C.white, 'center', 800);
  fakeLabel(960, 760);                                                                // the quote repeats the fake numbers
});
// no still over ~6 s: push in on the stamp (tools/stills.py counts a window as a cut)
win(K.made + .4, K.read, 'punch', [], { k: 1.18, cx: 960, cy: 620 });
// the real thing whenever the voice mentions it: the run's own footage beside the sheet, then a push-in
win(K.wrote, K.wrote + 2.5, 'split', [{ src: D.clip, title: 'THE REAL RUN', from: 0 }], { title: 'ITS REAL LOG' });
win(K.wrote + 2.5, DUR, 'punch', [], { k: 1.25 });
sfx(0, 'thunk', .5); sfx(K.made, 'thunk', .6); sfx(K.read, 'whoosh', .3); sfx(K.wrote, 'swish', .4);
