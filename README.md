# League of Legends Matchup Guide

## About the project

This is a desktop application for League of Legends players to record and consult matchup notes. The tool allows you to quickly search for an enemy champion and view essential information such as difficulty level, recommended runes, summoner spells, starting items, and specific notes on what to do or avoid during the laning phase. The goal is to provide a fast reference during champion select or the loading screen.

## How to record your notes

All data displayed by the application is stored and read locally from the `matchups.json` file, located in the project's root folder.

To edit or add your own notes:

1. Open the `matchups.json` file.
2. Search for the enemy champion's name.
3. Fill in or modify the text values inside the quotation marks for the desired keys (`"difficulty"`, `"runes"`, `"notes"`, `"todo"`, `"nottodo"`).
4. Save the file. The changes will be applied immediately the next time you open the app or consult the champion.

**Recommended editing tools:**
If you do not use a code editor (such as VS Code or Notepad++) and want to avoid syntax errors (like accidentally deleting a comma or bracket, which will prevent the file from being read), you can use online JSON validators and editors. Simply copy the content of your file, paste it into the website, make your edits, and paste it back into your file:

## Trivia

Initially, this project was conceived and built exclusively for *Riven mains* to document their top lane matchups. However, as development progressed and the code was refined, the project's scope was expanded so that the structure could be used by any player, covering all champions and roles in the game.
