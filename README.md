# news-image-20261123-v1

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/haidildariell/news-image-20261123-v1/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/haidildariell/news-image-20261123-v1/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-image broadsheet summing up the world news of Monday 23 November 2026 — 37 stories across 7 regions, 15 of them illustrated. Leads: Democrats clinch 258 House seats, their biggest majority since 1992; FBI Top-10 fugitive 'Chapo Isidro' captured in Sinaloa; Liverpool rout 10-man Manchester United 4–0. All stories were verified against live reporting on the morning of 23 November 2026 (WIB); most were first reported overnight Sunday into Monday in Asia–Pacific time. Stories from 21–22 November that were not part of this day's news (COP31 no-deal, Russia's 186-drone Kyiv raid, Cikande fire toll, Verstappen's Las Vegas win, Wembanyama's 50 points, India 720/9 declared) are named in the DATE CHECK box as left out. A world map with numbered pins, a UTC timeline, a stat strip and a certainty legend complete the page.

## Run it

```sh
python3 render.py        # rebuild entry.png (needs Pillow)
python3 main.py          # copy entry.png to /output/entry.png
```

`render.py` draws the 1024×1024 PNG with Pillow at build time: masthead, date headline, red deck line, six-number stat strip, region bar, UTC timeline, three illustrated lead stories, twelve illustrated smaller stories, a numbered world map, an ALSO list of 22 more stories, a DATE CHECK box, a certainty legend and a sources footer. `main.py` (standard library only) copies the shipped `entry.png` to `/output/entry.png`, so both runs write identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=haidildariell&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
