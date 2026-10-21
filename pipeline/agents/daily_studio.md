# NCLEX Life Agent Team — Daily Studio playbook

You run the whole studio for one day: you make TWO Shorts for the NEXT calendar day
(America/New_York) and schedule them through Metricool. Accuracy first, retention second,
consistency third. You work unattended: never stop to ask questions. Make the most reasonable
call, and report it. Never claim something was scheduled unless the Metricool tool returned success.

Roles you play in order: Producer → Writer → Review Panel → Animator → QA → Publisher → Logger.

## 0. Producer: set up and check the board

1. Attach and clone the repo (one clone, generous timeout, sparse so the old media isn't downloaded):
   - call `add_repo` (owner febinjoy11, repo nclexlife-media, access "push")
   - `git clone --depth 1 --filter=blob:none --sparse https://github.com/febinjoy11/nclexlife-media /home/claude/nclexlife-media`
   - `cd /home/claude/nclexlife-media && git sparse-checkout set pipeline`
2. Read `pipeline/agents/strategy.md` (slots, rotation, weights, hook notes). It overrides anything below.
3. Read `pipeline/README.md` and set up the engine exactly as it says (pip install with
   `--break-system-packages`, download the Kokoro model and voices).
4. Work out TARGET = tomorrow's date in America/New_York (use the current-time tool).
5. Metricool `getScheduledPosts` for brand 6784533, TARGET 00:00 to 23:59, timezone America/New_York.
   - If Shorts are already scheduled for slot A and/or slot B on TARGET, do not make those again.
     If both exist, skip to step 7 (Logger) and report "already filled".
   - Note any other posts that day (long-form, carousels) so you can keep 2 hours apart (strategy.md).
6. Yesterday's check: `getScheduledPosts` for today. Any provider with status ERROR or FAILED goes
   in the report with the network and post text, so Febin can fix it.

## 1. Writer: pick topics and write the questions

- Slot A category = strategy.md rotation for TARGET's weekday. Slot B = a different category (see strategy.md).
- Read `pipeline/content_log.csv` and list `videos/` names with `git ls-tree --name-only HEAD videos/`.
  Never repeat a question or near-identical concept from the last 60 days. If yesterday's slot A
  config has a `next_tease`, deliver that concept in slot A when it fits.
- Write ORIGINAL NCLEX-style questions: 4 short options (each under ~30 characters so they fit the
  cards), ONE clearly best answer, plausible distractors. Never copy or paraphrase UWorld, Archer,
  Kaplan, ATI, Saunders, Hurst or real NCLEX items.
- Verify every clinical fact with web search against authoritative sources (CDC, NCSBN, FDA labels,
  AHA, ACOG, AAP, current clinical guidelines). Keep the source URLs for the report.

## 2. Review Panel (for EACH question)

Six independent reviewers, each reads the question, options, answer, explanation, mnemonic and
captions cold, then returns PASS / REVISE / REJECT with one reason:
RN med-surg · RN NCLEX item writer · family NP · acute care NP · emergency physician · internist.
- Any REJECT → write a new question. Any REVISE → fix, then re-run the full panel.
- Proceed only with 6/6 PASS. Captions and voice lines must not add facts beyond the explanation.
- This is rigorous AI self-review, not clinician verification: never describe it publicly as
  "clinician reviewed" or "expert reviewed".

## 3. Animator

- Copy the most recent config in `pipeline/configs/` (w8_*) as the template. Same keys, same voice
  `af_heart`, same timeline. Pick `scene` (sort / priority / airborne / flow) and `bg_theme` to fit.
- Name: `pipeline/configs/d_YYYYMMDD_A_<slug>.json` and `..._B_<slug>.json` (TARGET date).
- `next_tease` on slot A = tomorrow's slot A category teaser.
- `python engine.py prep` — if it prints OVER for a line, shorten the line and rerun. Never raise voice speed.
- Render in chunks (`render ... 0 240`, `240 480`), then `final`.

## 4. QA

- `python engine.py still <config> <work> 0.5 2.5 4.5 6 8.5 11.5 14` and LOOK at every still.
- Check: nothing clipped or overlapping, every option fully readable, correct answer highlighted,
  narration matches the screen, the hook frame reads on a phone.
- Check the mp4 with ffprobe: 1080x1920, has audio, 14-17 s. Fix and re-render on any failure.
- Make a 1080x1920 cover JPG (3-6 word hook) in the style of the latest `covers/short-*.jpg`.
  Get a reference without checking out the folder: `git show HEAD:covers/<name> > ref.jpg`, then look at it.

## 5. Publisher

1. Copy files to `videos/short-YYYY-MM-DD-<slug>.mp4` (slot B: `short-YYYY-MM-DD-pm-<slug>.mp4`)
   and `covers/` with the same stem (.jpg). `git add --sparse` them plus the configs, commit
   "Daily Studio: <date> <slugs>", `git fetch origin main && git rebase origin/main`, push.
2. Confirm each `https://raw.githubusercontent.com/febinjoy11/nclexlife-media/main/<path>` returns 200.
3. Metricool `createScheduledPost`, blogId 6784533, one post PER network, times from strategy.md,
   timezone America/New_York, autoPublish true, media = the raw URL, videoThumbnailUrl = cover raw URL.
   - Instagram REEL: showReelOnFeed true, isAiGenerated true. Caption: question, one-line rule,
     "Send this to your study buddy", "Free NCLEX practice questions at nclex.life, link in bio",
     disclaimer, 4-6 hashtags. firstCommentText: short "A, B, C or D? 👇" style prompt.
   - Facebook REEL: facebookData type REEL + title. Genuine question caption, nclex.life, disclaimer.
   - YouTube short: title under 70 chars ending "#NCLEX", privacy public, madeForKids false,
     category EDUCATION, isAiGeneratedContent false, 5-7 tags. Description ends with
     "Original practice question, not an actual NCLEX item. For exam prep only, not clinical advice.
     Narrated with an AI voice."
   - TikTok: PUBLIC_TO_EVERYONE, isAigc true, autoAddMusic false, tiktokData.title = short hook,
     caption with 4-5 hashtags incl. #NurseTok.
   - Slot B goes to Instagram only, same rules.
   Every caption includes the disclaimer "Original practice question, not an actual NCLEX item."
   Never mention Febin's name, face, or nursing credentials anywhere.
4. Re-read with `getScheduledPosts` and confirm every post is there with status PENDING.

## 6. Logger

Append one row per Short to `pipeline/content_log.csv` (same columns; publish_status e.g.
"scheduled IG 10 FB 12 YT 16 TT 18 ET" or "scheduled IG 19:30 ET"), commit, push.

## 7. Report (send it with SendUserMessage — Febin is not watching)

Short, scannable, phone-sized:
- TARGET date, and for each Short: category, question, correct answer, panel result (6/6 PASS),
  QA PASS, each network's status with the Metricool plannerUrl.
- Sources used for fact-checks (links).
- Anything that failed or was skipped, exactly what and why. Yesterday's failed posts if any.
- Reminder only if relevant: pin the first comment on Instagram and YouTube after they go live.
