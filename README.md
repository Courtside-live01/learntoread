# Hoot's Reading Island

A talking, picture-based reading adventure for a 5-year-old. It is a single HTML page that works in any browser, on phones, tablets and computers.

The child travels across 11 islands, from the five vowels all the way to reading whole sentences. Each island has picture cards to learn from, then five quick games. Finishing an island earns a gold star and an animal sticker.

| # | Island | What it teaches |
|---|---|---|
| 1 | Vowel Valley | a e i o u and their short sounds |
| 2 | Alphabet Beach | Letters and their picture friends ("B is for ball") |
| 3 | Two-Letter Town | up, go, hi, me |
| 4 | Cat Farm | Short a words: cat, hat, van |
| 5 | Hen House | Short e and i words: hen, bed, pig |
| 6 | Sunny Pond | Short o and u words: dog, sun, bus |
| 7 | Tricky Treehouse | Sight words: the, I, you, my, see |
| 8 | Frog Forest | Consonant blends: frog, star, drum |
| 9 | Ship Shore | Letter teams: sh, ch, ck, ee, oo, ng |
| 10 | Five-Letter Castle | horse, train, zebra, pizza |
| 11 | Sentence Summit | Short sentences: "The dog can run." |

Games: which vowel, first sound, balloon pop, find the letter, find the picture, feed the hungry monster, build the word, missing letter, memory match, word balloons, sentence to picture and sentence builder.

Red tiles are always vowels and blue tiles are consonants. Wide tiles are letter teams. After two wrong tries the right answer glows, so a child never gets stuck.

## Play it

Open `reading-adventure.html` in a browser and tap **Let's read!** (browsers only allow sound after a tap). Keep the `voices/` folder next to the HTML file so the extra teacher voices can load.

## Voices

Every word, letter and instruction is a recorded clip in six natural female teacher voices (Microsoft neural voices via [edge-tts](https://github.com/rany2/edge-tts)): Ava (default, built into the page), Emma, Jenny, Sonia, Libby and Natasha. The five extra voices live in `voices/*.js` and load only when chosen.

## Files

| File | What it is |
|---|---|
| `reading-adventure.html` | The built game (open this) |
| `voices/*.js` | Extra voice packs, loaded on demand |
| `template.html` | Page source: layout, styles and game code |
| `content.py` | Islands, words, pictures, sentences and spoken phrases |
| `build.py` | Records the clips and builds the page |
| `v1/` | The first 5-island version, kept for reference |

## Rebuild

Needs Python 3, `edge-tts` (`pip install edge-tts`) and `ffmpeg`.

```bash
python build.py
```

The build records any clips not already in `audio/`, which is a cache and is not committed. It trims and loudness-normalises each clip, then writes `reading-adventure.html` and `voices/*.js`. To change words or add an island, edit `content.py` and rebuild.
