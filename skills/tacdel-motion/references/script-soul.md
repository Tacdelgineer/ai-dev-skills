# Script soul: how a tacdel script should sound

The scripts that failed were correct and clear, but they read like an explainer narrated from outside, with
template transitions, uniform sentences and a moral at the end. A script with soul is a small story told by
a person who finds it funny and a little bit moving, to one friend.

## The rules

1. **A character who wants something.** Tac (or Chat, or "you") wants something in the first five seconds.
   Every beat after that changes how close Tac is to getting it. Tac has a feeling in every beat: proud,
   confused, embarrassed, determined, relieved.
2. **Alireza is talking to one friend.** Use contractions, small asides ("I'm not kidding", "honestly",
   "look") and one opinion of his own. Use the first person only for things that are true ("I've watched my
   own agents do this" only if he has). Never invent a result.
3. **One specific detail per beat.** Use something you can picture or hear: the bot that's very proud of a
   calculator nobody asked for, six phones buzzing at once, the leaf sticker on the box. Cut any beat that
   has no detail.
4. **No template phrases.** Banned: "Here's what happens", "Here's the difference", "So what happened?",
   "Let's look inside", "Turns out", "The real X is Y", "In a world", "game-changer", "Let's dive in",
   "It's not about X, it's about Y", "And that's why…". Each of these says "a narrator is talking", not
   a friend.
5. **One gut-punch moment.** The low point should land: the table is full, the steakhouse, the bill. Put a
   `<break time="0.6s" />` before it and let the music drop out. Never more than two breaks.
6. **Vary the rhythm.** After any sentence over 15 words, the next is under 5. Read it aloud and you should
   hear a short one land after a long one: "Nobody asked. He's very proud."
7. **End on a feeling or a callback.** Bring back the opening image, or give one small human beat. If there's
   a practical tip, say it the way a friend would ("tell it twice, it won't mind"), not like a lesson.
   A short question to the viewer about this Short works too. Never tease, promote or advertise another
   episode or video ("next time...", "in my next one...", "follow to see...").
8. **Facts stay exact.** Soul never bends a number or a claim. A vendor number is still said as the
   vendor's, for their system. Plain words: explain jargon or cut it, and use 1–2 numbers at most.
9. **Two hooks, keep one.** Write two openings and keep the one a friend would repeat to someone else.
10. **The read-aloud test.** Read every line in Alireza's voice. If a line sounds like a corporate explainer,
    rewrite it. If it sounds like something he'd say across a dinner table, keep it.

Length: about 110 words (100–120) for ~45 s on eleven_v4 at speed 0.93 (`FINAL_VOICE.md`). Write numbers as words.

## Before and after (Ep 1)

**Before (correct, but flat):** Imagine you hire a hundred AI agents. They never sleep, and they have one job:
build me a website. Here's what happens. All one hundred start on the homepage at once…

**After (same facts, more soul):**
This is Tac. Tac is an AI agent, and Tac just had a big idea: what if there were a hundred of me?
So now there are a hundred Tacs. They never sleep, and they have one job: build a website.
All hundred sprint to the homepage. Half paint it orange. Half paint it blue. Nobody stops.
Twelve wander off to read about what a website even is. And one is building a calculator. Nobody asked.
He's very proud.
And every single thought costs money. When Anthropic ran its own team of research agents, it used about
fifteen times the tokens of a normal chat.
So Tac blows the whistle and puts one Tac in charge.
The job gets cut into pieces. Every team gets one. Somebody checks the work at the end.
And then <break time="0.6s" /> it's quiet.
By the afternoon, there's a website.
A hundred Tacs never needed more Tacs. They needed a plan.

## Hooks that would have been better

- Ep 2: "Same job, two AIs. Dinner for six, Friday night, thirty bucks a head. The first one answers before
  you finish blinking."
- Ep 3: "You told your AI you're vegetarian. You were very clear. An hour later, it books you a steakhouse."
