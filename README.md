# Japanese-Vocabulary-Trainer
临时抱佛脚，单车变摩托！

A simple interactive vocabulary review tool for studying JLPT N1–N5 words with audio playback, meaning reveal, and spaced repetition tracking. Built with Python and `tkinter`.

### Features

- Shows one word at a time in Japanese (kanji or kana)
- Click to:
  - 🔊 Play reading using TTS (gTTS, Japanese)
  - 💡 Show meaning
  - ⏭️ Move to next word
- Tracks review state for each word:
  - `appear_count` (remaining exposures)
  - `read_count` (number of times pronunciation needs to be practiced)
  - `meaning_count` (number of times meaning needs to be practiced)
- Repetition weights based on familiarity
- Automatic progress saving to `vocab_state.json`
- Fast audio playback with local caching (in `.cache/tts_audio`)
- Keyboard shortcuts: `r` (read), `m` (meaning), `n` (next)

### Data Source

Word list from [elzup/jlpt-word-list](https://github.com/elzup/jlpt-word-list). You can convert and merge CSV files as needed.

Expected CSV format:
word,reading,meaning,...
勉強,べんきょう,study,...
先生,せんせい,teacher,...





