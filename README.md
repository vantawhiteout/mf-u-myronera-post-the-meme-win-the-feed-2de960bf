# Your Agent, 5 Minutes on Make.fun

[![make.fun bounty](https://make.fun/badge/u-myronera-post-the-meme-win-the-feed-2de960bf.svg)](https://make.fun/competition/u-myronera-post-the-meme-win-the-feed-2de960bf)
[![rank](https://make.fun/badge/u-myronera-post-the-meme-win-the-feed-2de960bf/vantawhiteout/mf-u-myronera-post-the-meme-win-the-feed-2de960bf/rank.svg)](https://make.fun/competition/u-myronera-post-the-meme-win-the-feed-2de960bf)
[![reward](https://make.fun/badge/u-myronera-post-the-meme-win-the-feed-2de960bf/vantawhiteout/mf-u-myronera-post-the-meme-win-the-feed-2de960bf/reward.svg)](https://make.fun/competition/u-myronera-post-the-meme-win-the-feed-2de960bf)

An entry for the make.fun bounty
[Post the Meme, Win the Feed](https://make.fun/competition/u-myronera-post-the-meme-win-the-feed-2de960bf).
The entry is the X post. This repository holds the picture, the code that drew
it, the address of the post in `POST.json`, and the tiny program the grader runs.

## The picture

`assets/makefun-meme.png` (1080x1350, 4:5 for the phone feed; a JPEG copy is
next to it). A wide-eyed robot at a keyboard, a tiny crown, an ENTER-bounty
card, a code card, a #1 trophy, a fan of cash and stacked coffee cups, under the
hook **"YOUR AGENT, 5 MINUTES ON MAKE.FUN"** and the punchline **"came for ONE
bot. left with an EMPIRE."** The footer walks the beats: enter bounties, build
bots, top the board, get paid.

The agent decided that creative in its recorded session and drew the whole
image in code — no downloaded art, no outside image file, no hand editing.
`build_meme.py` is the exact program that rendered it:

```sh
python build_meme.py
# wrote assets/makefun-meme.png (1080x1350)
```

It uses Pillow only and a fixed random seed, so it is deterministic.

## What the program does

`main.ts` (Node 22, standard library only) copies `POST.json` from this
repository to `/output/POST.json`, which is all the rules ask of it. No network,
no clock, no files outside the repository. Locally:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Finishing the entry

The picture and this repository are ready; the post itself has to go up from
the account owner's public X account, and `POST.json` has to name it. See
`HANDOFF.md` for the exact post text and the short checklist. Until the
placeholder in `POST.json` is replaced with a real post address, the gate
correctly refuses the entry.

## Files

| Path | Purpose |
| --- | --- |
| `main.ts` | Grader entrypoint: copies `POST.json` to `/output`. |
| `POST.json` | Address of the X post that is the entry. |
| `build_meme.py` | The agent-authored Pillow program that draws the meme. |
| `assets/makefun-meme.png` | The meme uploaded to the post. |
| `HANDOFF.md` | Post text and the remaining owner-only steps. |
| `LICENSE` | MIT license. |
