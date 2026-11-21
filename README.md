[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/leopad12121/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/leopad12121/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World in One Day — Saturday 21 November 2026

**Round 2** — rebuilt from the full day's news of 21 November 2026.

A newspaper front page, drawn entirely in code, that sums up Saturday
21 November 2026 in six stories. `main.py` (Python 3.13, standard library
plus Pillow, no network) draws the page at 1024×1024 and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`, or `./entry.png`).
Running it twice produces byte-identical output. Every illustration panel
is made of shapes — no photographs, no external images.

## The six stories

1. **Middle East — Gulf war flares again.** Bahrain said its air defences
   intercepted Iranian aerial attacks on Saturday evening, as attacks on
   tankers in the Strait of Hormuz reached their highest level since the
   war began; the US and Israel are reported to be weighing new strikes
   within days. Sources: Gulf News, Dawn, Al Jazeera, Reuters.
2. **Mexico — FBI most-wanted cartel boss seized.** Mexican forces captured
   Fausto Isidro Meza Flores, "El Chapo Isidro", in Guasave, Sinaloa, on
   Friday night; 11 people died in the cartel backlash. Sources: Reuters,
   Associated Press.
3. **Markets — AI sell-off sinks world markets.** The S&P 500 fell 3.7% and
   the Nasdaq 5.3% on Friday; Nvidia fell about 14% after Reuters reported
   the SEC is examining its accounting. Source: Reuters.
4. **Ukraine — Missiles hit Zelenskyy's hometown, land in Poland.** Russian
   missiles struck Kryvyi Rih on Friday night, killing two and wounding
   60; two Russian missiles and a drone also came down in Poland.
   Sources: Associated Press, Al Jazeera.
5. **Climate — COP31 talks run past deadline.** The UN climate summit in
   Antalya, Turkey, overran its Friday deadline over a draft text that
   drops fossil-fuel language. Sources: One Turn, WW6RAG.
6. **Science — Mosquitoes that beat dengue.** A four-year study of more
   than 5,700 children in Belo Horizonte, Brazil, found Wolbachia-carrying
   mosquitoes cut dengue and chikungunya infections by about 69%.
   Source: Associated Press.

## Run it

```sh
python3 main.py
# or: MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
