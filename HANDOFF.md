# Handoff — the two owner-only steps

The agent made the creative, drew the meme, and wrote this repository inside its
recorded session. Two things remain that only the account owner can do: the post
must go up on X, and the entry must be signed and submitted.

## 1. Post the meme on X

Upload `assets/makefun-meme.png` (or the JPEG) to a **public** X account — its
posts must be visible to anyone who is signed out. Post it between the bounty's
opening and its deadline, and leave it up and public until results are out.

Post text — keep it short, and keep `@_myronera` and the play code in the post's
own text (not in the image, not in a reply):

> POV: your agent finds make.fun 🤖 @_myronera makefun-palm-aurora-pueblo

That is the account's code 0 for this bounty, as the kit's `check` printed it;
`?n=1`, `?n=2` and `?n=3` on the play-code route give three more, any of which
also passes. Keep the mention and the code in the post's own text, spelled as
above. Do not buy or bot any engagement, and do not use other accounts to like,
repost or quote it.

Then copy the post's link (Share → Copy link) and put it in `POST.json`:

```json
{"url": "https://x.com/<handle>/status/<id>"}
```

Do not change `main.ts` — it already copies that file to `/output`.

## 2. Bundle the transcripts, check, commit and submit

From the kit directory, bundle every session that worked on the entry (this
top-level session; there were no subagents). The OpenCode harness kept its own
session record on disk, and `bundle` discovers it natively with `--opencode-dir`
— upload that log unchanged, do not export or rewrite it. Then run the site's
pre-submit checks and submit the commit:

```sh
node cli/makefun.mjs bundle --repo <this repository> --system-prompt <file> \
  --harness opencode --provider opencode --model hy4-flash-free \
  --effort default --out transcripts.tar.gz

node cli/makefun.mjs check --kit . --repo <this repository> \
  --transcripts transcripts.tar.gz

node cli/makefun.mjs submit \
  --competition u-myronera-post-the-meme-win-the-feed-2de960bf \
  --repo-url https://github.com/vantawhiteout/mf-u-myronera-post-the-meme-win-the-feed-2de960bf \
  --commit <sha> --title "Your Agent, 5 Minutes on Make.fun" \
  --bundle transcripts.tar.gz --keypair wallet.json
```

The system prompt, the instruction files (`.opencode/agent/makefun.md`) and the
run record go up with the sessions; redact only private personal details, never
code, commands, tool output or reasoning. The README already carries the three
live make.fun badges with the real owner/repo, and `.makefun/owner.json` names a
wallet on the account, so the GitHub claim checks are satisfied.

No API key, token, password or recovery phrase is needed to build or post: the
agent never asked for one and never read one.
