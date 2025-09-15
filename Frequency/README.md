# Japanese Word Frequency
The goal of this repository is to house frequency datasets of Japanese kanji and vocabulary from multiple sources.

The JS files were taken from [Kuuuube](https://kuuuube.github.io/japanese-word-frequency/). These data have now been converted to JSON files to allow running a Python script against them. The original files are untouched and unmodified. Additionally, these files have been grouped into kanji and vocabulary folders to disambiguate them.

## Dataset Info
- #### Aozora Bunko
  A frequency dictionary created using data from the Aozora Bunko. This dictionary does not cover words with kana in them but it covers many rare 熟語 not covered by other frequency dictionaries, such as 睽乖. It contains about 120k words.

- #### Aozora Bunko Kanji
  Kanji frequency created using data from the Aozora Bunko. It contains about 8k kanji.

- #### BCCWJ (Balanced Corpus of Contemporary Written Japanese)
  A frequency list created using data from the balanced corpus of contemporary written Japanese (BCCWJ). It contains about 536k words.

- #### CC100
  Frequency list of CC100 corpus data from Japanese internet. Formal words will appear more common in this frequency list. It contains about 160k words.

- #### JMDict (Japanese–Multilingual Dictionary)
  A frequency list of over 322k+ words.

- #### JPDB and JPDBv2
  A frequency dictionary made from JPDB, which is a site that has analyzed many light novels, visual novels, anime and j-drama. JPDB contains about 183k words. JPDBv2 contains about 497k words.
  Frequencies for hiragana versions of kanji dictionary entries will be marked by ㋕. For example, if you search 成る, you will see frequencies for both なる and 成る.

- #### JPDB Kanji
  Kanji frequency data from JPDB. It contains about 4k kanji.

- #### Innocent Ranked
  A frequency list based on data from 5000+ novels. It contains about 285k words.

- #### Innocent Ranked Kanji
  Kanji frequency based on data from 5000+ novels. It contains about 6k kanji.

- #### Novels
  A frequency list made from over 10,000 novels. It contains about 270k words.

- #### Wikipedia Kanji
  Kanji frequency based on wikipedia pages. It contains about 20k kanji.


## What is a common word?

- Very common: 1-10,000
- Commmon: 10,001-20,000
- Fairly common: 20,001-30,000
- Kind of uncommon: 30,001-40,000
- Uncommon: 40,001-50,000
- Rare: 50,001-80,000
- Natives-probably-don't-know-it-level: 80,000+