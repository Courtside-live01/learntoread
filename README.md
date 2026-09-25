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

Every word, letter and instruction is a recorded clip in eleven natural teacher voices (Microsoft neural voices via [edge-tts](https://github.com/rany2/edge-tts)).

- Female: Ava (default, built into the page), Emma, Jenny (American), Sonia, Libby (British), Natasha (Australian)
- Male: Andrew, Brian (American), Ryan, Thomas (British), William (Australian)

The extra voices live in `voices/*.js` and load only when chosen.

## Sound Garden (phonics)

Real letter sounds ("sss", "mmm", "buh"), not letter names, in the chosen teacher's voice, plus a step-by-step path to reading:

1. **Letter sounds**: 5 lessons in the usual teaching order (s a t p i n / m d g o c k / e u r h b f / l j v w y z / x qu sh ch th). "This is s. s says sss... sun!"
2. **Blend two sounds**: 5 lessons (one per vowel). sss + a slide together into "sa".
3. **Sound out words**: 5 lessons. c... a... t... ca... t... cat.
4. **Read by myself**: 5 lessons of mixed words, with "Sound it out" as help.

The **Sound board** plays every letter sound (a to z, plus qu, sh, ch, th) with a picture word, and "Play all" runs through the alphabet.

The voices cannot say a sound on its own, so `phonics/slice.py` cuts each sound out of the teacher's own recording of a word: the hiss before the vowel in "sun", the hum in "mud", the burst plus a short "uh" in "bug", the "ks" at the end of "box". Where the consonant ends is found from the energy in different frequency bands; hiss sounds are then filtered to pure hiss and hums to pure hum. Blends ("sa") are cut from a word ("sat") just before the final consonant. Short vowels are cut the same way from apple, egg, it, octopus and up.

## Sound World (open-world 3D)

A free-roaming island (first button on the 3D menu) with 29 letter friends: the vowels live in red houses in Vowel Village in the middle, the consonants (plus qu, sh, ch, th) stand on blue statues around the island. A floating arrow points to the nearest letter not yet found. Walking up to a letter opens its card:

1. **Listen**: "This is b. b says buh... buh... ball!" (vowels add "This letter is a vowel").
2. **Say the sound** into the mic; the child hears their own voice next to the teacher's.
3. **Say the word** ("ball"); speech recognition checks it (with the same forgiving checker as Talk Time), coaching up to three tries.

Found letters turn gold, get a star, and fill the letter tray at the top; progress is saved. Without a microphone or speech recognition, a grown-up checks with thumbs up.

## Word Island 3D

A low-poly 3D island (three.js, loaded from cdnjs only when opened) where a blocky buddy walks, runs and jumps down a path of reading gates: a floating joystick on the left of the screen, a JUMP button on the right, arrow keys/WASD and space on a computer.

- **Letter Land**: walk into the letter the teacher asks for; "b... buh... ball".
- **Word Builder**: spell a word sound by sound (the next letter is asked for by its sound).
- **Sentence Trail**: the teacher reads a sentence with a gap; walk into the missing word.

Adapted from a separate Word Island prototype: it now uses the chosen teacher voice and real letter sounds instead of the device's speech voice, the app's own letters, words, pictures and sentences (lowercase, vowels red), saves stars to the app's progress, keeps its touch handling and render loop inside its own screen (stopped when closed), and places the signs beside the path so the answer blocks stay in view on a phone.

## Talk Time (speaking practice)

400 speaking lessons with the microphone: 100 each for 2, 3, 4 and 5-letter words. Each lesson practises 3 words (1 new, 2 review, so every word comes back spaced out). English has only about 35 two-letter words a young child uses, so the 2-letter lessons repeat those words in new mixes; the 3, 4 and 5-letter levels each use 100 different words.

For each word the teacher says it, then says it slowly; the child taps the big mic and says it. The mic input is cleaned up for a small, soft voice (browser noise suppression, echo cancellation and auto gain, then rumble and hiss filters, a consonant-clarity boost, compression and extra gain). The child hears their own recording next to the teacher's ("This is you... and this is me"). Where the browser has speech recognition (Chrome, Safari), it checks the word: exact or a homophone is a pass, one sound off is "so close", and the tile for the sound that was off is highlighted with a slow model. After three tries the lesson moves on kindly. Without speech recognition, or with it switched off in the grown-ups panel, a grown-up checks with thumbs up.

Recordings stay on the device and are never saved or uploaded. Speech checking uses the browser's own speech service (Google in Chrome, Apple in Safari). The microphone needs the normal web page (https://learntoread-one.vercel.app); it is not available inside the Claude app.

## Picture Pairs and stickers

Picture Pairs is a matching game with 9 levels (6, 8, 10, 12, 16, 18, 20, 22 and 24 cards). Each pair is a picture and its written word, so matching means reading.

Each island awards an animal sticker. Tapping a sticker plays a real field recording of that animal, then the teacher says its name.

### Animal sound credits

Real recordings from Wikimedia Commons, trimmed to a short clip and level-matched (no other processing):

- Horse: [Wiehern.ogg](https://commons.wikimedia.org/wiki/File:Wiehern.ogg) by Hü., Public domain
- Dolphin: [161691 felixblume dolphin-screaming-underwater-in-caribbean-sea-mexico.wav](https://commons.wikimedia.org/wiki/File:161691_felixblume_dolphin-screaming-underwater-in-caribbean-sea-mexico.wav) by Felix Blume, CC0
- Dog: [Barking of a dog.ogg](https://commons.wikimedia.org/wiki/File:Barking_of_a_dog.ogg) by Amada44, CC BY-SA 3.0
- Cow: [Single Cow Moo.ogg](https://commons.wikimedia.org/wiki/File:Single_Cow_Moo.ogg) by MichaeltheFox8621, CC BY-SA 4.0
- Rooster: [Medium rooster crowing.ogg](https://commons.wikimedia.org/wiki/File:Medium_rooster_crowing.ogg) by alys, Public domain
- Duck: [Anas platyrhynchos - Mallard - XC62258.ogg](https://commons.wikimedia.org/wiki/File:Anas_platyrhynchos_-_Mallard_-_XC62258.ogg) by Jonathon Jongsma, CC BY-SA 3.0
- Whale: [Humpbackwhale2.ogg](https://commons.wikimedia.org/wiki/File:Humpbackwhale2.ogg) by Spyrogumas, CC0
- Lion: [Lion raring-sound1TamilNadu178.ogg](https://commons.wikimedia.org/wiki/File:Lion_raring-sound1TamilNadu178.ogg) by த*உழவன், Public domain
- Eagle: [Bald Eagle Yellowstone National Park.ogg](https://commons.wikimedia.org/wiki/File:Bald_Eagle_Yellowstone_National_Park.ogg) by National Park Service, Public domain
- Monkey: [Howler monkey.ogg](https://commons.wikimedia.org/wiki/File:Howler_monkey.ogg) by David O'Hara, CC BY 3.0
- Frog: [Banded Bull Frog Call.ogg](https://commons.wikimedia.org/wiki/File:Banded_Bull_Frog_Call.ogg) by Inspector, CC BY-SA 3.0

## Files

| File | What it is |
|---|---|
| `reading-adventure.html` | The built game (open this) |
| `voices/*.js` | Extra voice packs, loaded on demand |
| `voices/*.talk.js` | Talk Time words (normal and slow) for each voice |
| `template.html` | Page source: layout, styles and game code |
| `content.py` | Islands, words, pictures, sentences and spoken phrases |
| `build.py` | Records the clips and builds the page |
| `phonics/slice.py` | Cuts letter sounds and blends from each voice's words |
| `animals/` | Trimmed animal clips, their credits, and `trim.py` |
| `v1/` | The first 5-island version, kept for reference |

## Rebuild

Needs Python 3, `edge-tts` (`pip install edge-tts`) and `ffmpeg`.

```bash
python build.py
```

The build records any clips not already in `audio/`, which is a cache and is not committed. It trims and loudness-normalises each clip, then writes `reading-adventure.html` and `voices/*.js`. To change words or add an island, edit `content.py` and rebuild.
