# NCLEX Life Agent Team

Claude scheduled tasks that run the NCLEX Life short-form channel end to end.

| Agent | When | Playbook | Does |
|---|---|---|---|
| Daily Studio | every night, ~8:40 pm ET | daily_studio.md | writes 2 original questions, 6-role AI review panel, renders the Shorts, QA, uploads here, schedules tomorrow in Metricool (IG ×2, FB, YT, TikTok), logs, reports |
| Weekly Strategist | Sundays, ~10:40 am ET | weekly_strategist.md | reads Metricool analytics, checks platform changes and best times, updates strategy.md and next week's slate, reports |

Shared memory: `strategy.md` (slots, rotation, weights, hook notes, slate) and `../content_log.csv`.
To change how the team behaves, edit `strategy.md` or a playbook here. No need to touch the
scheduled tasks themselves.

Handled outside this team: comment and DM replies (Muse), pinning first comments (Febin, in-app),
long-form videos and carousels (made on request in chat).
