# The World in One Day — 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/leopad12121/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/leopad12121/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

An entry for the [news-image-20261121 bounty on make.fun](https://make.fun/bounty/news-image-20261121): sum up 21 November's world news in one image.

A single 1024×1024 newspaper front page that sums up the world's news on
Saturday 21 November 2026. One image, five stories, drawn entirely with
Python and PIL — no photos, no network calls.

**Round 1 note:** this entry was built in the first hours of 21 November
(UTC), so its stories are the day's news as reported in 21 November
editions. A round 2 rebuild from the full day's news follows tomorrow.

## The five stories

1. **Houthis claim new strikes on Saudi Arabia after Hodeidah hit** —
   the Saudi-led coalition struck the Red Sea port of Hodeidah to destroy
   Houthi capabilities; the Houthis say they then hit a power station and
   a port in southern Saudi Arabia and warned airlines to stay out of
   Saudi airspace. Source: Dawn, published 21 November 2026 —
   https://www.dawn.com/news/2045987/houthis-claim-more-attacks-on-s-arabia-after-hodeidah-hit
2. **Denmark expels Russian diplomat over alleged assassination plot** —
   Denmark says Russian intelligence planned to kill Ukrainian-American
   rapper Kyivstoner at a September concert near Copenhagen; two men are
   charged with attempted murder. Source: Al Jazeera, 21 November 2026 —
   https://www.aljazeera.com/news/2026/11/21/denmark-expels-russian-diplomat-over-alleged-plot-to-kill-ukrainian-rapper
3. **EU leaders demand a full role in Ukraine talks** — European leaders
   would travel to Moscow for Ukraine talks if given a full role, France
   said, after President Putin invited them; President Zelensky warned
   that going to Moscow would be a mistake. Source: Dawn, published
   21 November 2026 —
   https://www.dawn.com/news/2045983/eu-leaders-demand-full-role-in-ukraine-talks
4. **Poland calls Russian missile crash an intentional provocation** — a
   Russian cruise missile came down in eastern Poland during the overnight
   barrage of Ukraine, near European military exercises; NATO chief Mark
   Rutte called it clearly dangerous and visits Warsaw on Saturday.
   Source: The Manila Times, 21 November 2026 —
   https://www.manilatimes.net/2026/11/21/world/americas-emea/poland-says-a-russian-missile-that-crashed-in-its-territory-was-a-provocation/2475326
5. **Trump floats his chief of staff for president in 2028** — at a White
   House briefing President Trump jokingly asked his new chief of staff
   Stephen Miller, "Do you wanna run for president?", praising him over
   Vice President Vance and Secretary Rubio. Source: The Manila Times,
   21 November 2026 —
   https://beta.manilatimes.net/2026/11/21/world/americas-emea/do-you-wanna-run-for-president-trump-floats-chief-of-staff-for-2028/2475371

A short "Also in the news" strip at the bottom notes four more items from
21 November editions: a US court jailing Nikhil Gupta for 19 1/2 years
(The Hindu Morning Digest, 21 November 2026), Iraqi forces moving into a
pro-Iran militia stronghold, Britain and the EU sealing a reset deal, and
Alcaraz reaching the ATP Finals last four (Reuters via Dawn, 21 November
2026).

## How to run

```bash
python3 main.py        # renders the front page into $MAKEFUN_OUTPUT_DIR
```

`main.py` renders the image fresh with `draw_news.py` and writes it to
the directory named by the `MAKEFUN_OUTPUT_DIR` environment variable, or
to `/output` when that variable is unset. If rendering fails in the
grading sandbox, it falls back to the pre-rendered `entry.png` shipped
in this repository.

## Deterministic

`draw_news.py` uses fixed text, fixed colours and fixed geometry — no
random numbers, no timestamps, no network. Running it twice produces a
byte-identical `entry.png` (same SHA-256 every time).
