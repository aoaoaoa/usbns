# Article readings

Drop one MP3 per curated feature here, named by its slug. The "Listen to this story" player on each feature finds it automatically; until a file is present the player plays `placeholder.mp3` (the A Common Endeavor letter reading). Delete `placeholder.mp3` and rebuild once every reading is in.

| Feature | File |
| --- | --- |
| The Louis Gregory Bahá'í Institute | `gregory.mp3` |
| New Yorkers create more unified communities | `newyorkers.mp3` |
| Two artists reimagine the role of art | `twoartists.mp3` |
| Association for Bahá'í Studies at 50 | `abs.mp3` |
| Communities engage in a common endeavor | `endeavor.mp3` |
| Sparkling spirits in Indianapolis | `comic.mp3` |

To credit a reader, set `audio_reader="Name"` on the feature in `build/data.py` and rebuild; the player then shows "Read by Name". Mono, 64–96 kbps MP3 keeps a 15-minute reading under 10 MB.
