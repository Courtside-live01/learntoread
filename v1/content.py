# Lesson content shared by build.py (audio) and the HTML (data).
VOWELS = {
  "a": {"word": "apple", "pic": "🍎", "src": "apple"},
  "e": {"word": "egg", "pic": "🥚", "src": "egg"},
  "i": {"word": "insect", "pic": "🐞", "src": "it"},
  "o": {"word": "octopus", "pic": "🐙", "src": "octopus"},
  "u": {"word": "umbrella", "pic": "☂️", "src": "up"},
}
FIRST_VOWEL = [("apple","🍎"),("ant","🐜"),("egg","🥚"),("elephant","🐘"),("insect","🐞"),
  ("iguana","🦎"),("octopus","🐙"),("otter","🦦"),("umbrella","☂️"),("up","⬆️")]
L2 = [("up","🎈⬆️"),("go","🟢"),("no","🙅"),("hi","👋"),("me","🙋"),("we","👫"),("ox","🐂"),("in","🐱📦")]
L3 = [("cat","🐱"),("dog","🐶"),("pig","🐷"),("hen","🐔"),("sun","☀️"),("bus","🚌"),("bed","🛏️"),("cup","🥤"),
  ("fox","🦊"),("bat","🦇"),("hat","🎩"),("box","📦"),("bug","🐛"),("web","🕸️"),("pen","🖊️"),("van","🚐")]
L4 = [("fish","🐟"),("frog","🐸"),("duck","🦆"),("milk","🥛"),("bell","🔔"),("drum","🥁"),("lamp","💡"),("sock","🧦"),
  ("crab","🦀"),("ship","🚢"),("nest","🪺"),("star","⭐"),("moon","🌙"),("tree","🌳"),("ring","💍"),("king","🤴")]
L5 = [("truck","🚚"),("snake","🐍"),("horse","🐴"),("sheep","🐑"),("train","🚂"),("house","🏠"),("mouse","🐭"),
  ("plant","🪴"),("bread","🍞"),("chair","🪑"),("clock","⏰"),("crown","👑"),("heart","❤️"),("pizza","🍕"),
  ("robot","🤖"),("tiger","🐯"),("zebra","🦓"),("whale","🐳"),("lemon","🍋")]

PHRASES = {
  "welcome": "Hello, super reader! I'm your teacher, and this is Hoot the owl. Let's go on a reading adventure! Tap the first island to start.",
  "intro1": "Welcome to Vowel Valley! These five letters are the vowels: A, E, I, O, U. Every word needs a vowel!",
  "intro2": "Welcome to Two Letter Town! Let's put two letters together to make little words.",
  "intro3": "Welcome to Three Letter Farm! Three letters make words like cat and dog.",
  "intro4": "Welcome to Four Letter Forest! You are getting so good at reading!",
  "intro5": "Welcome to Five Letter Castle! This is the biggest challenge. I know you can do it!",
  "learn": "Tap the picture to hear the word. Tap a letter to hear its name.",
  "learnv": "Tap the big letter to hear its sound.",
  "ready": "Great learning! Now let's play a game!",
  "whichvowel": "Which vowel says",
  "firstvowel": "What sound does this word start with? Tap the vowel.",
  "pop": "Pop the vowel balloons! Find A, E, I, O, and U.",
  "findpic": "Read the word. Then tap the matching picture!",
  "build": "Build the word! Tap the letters in the right order.",
  "missing": "Uh oh! A letter fell off. Which letter is missing?",
  "praise1": "Great job!", "praise2": "Wow, you are a super reader!", "praise3": "Yes! That's right!",
  "praise4": "Amazing!", "praise5": "High five!", "praise6": "Brilliant reading!",
  "retry1": "Oops, try again!", "retry2": "Almost! Have another go!", "retry3": "Hmm, look again and try.",
  "star": "You did it! You earned a gold star!",
  "alldone": "Hooray! You finished the whole reading adventure! You are a reading champion!",
  "locked": "That island is still locked. Finish the one before it first!",
  "popdone": "You popped all the vowels!",
  "helpread": "Let's read it together.",
}
VOICES = [  # key, edge-tts voice, teacher name, accent
  ("ava", "en-US-AvaNeural", "Miss Ava", "American"),
  ("emma", "en-US-EmmaNeural", "Miss Emma", "American"),
  ("jenny", "en-US-JennyNeural", "Miss Jenny", "American"),
  ("sonia", "en-GB-SoniaNeural", "Miss Sonia", "British"),
  ("libby", "en-GB-LibbyNeural", "Miss Libby", "British"),
  ("natasha", "en-AU-NatashaNeural", "Miss Natasha", "Australian"),
]
for v, d in VOWELS.items():
    PHRASES[f"vsays_{v}"] = f"The letter {v.upper()} says"
