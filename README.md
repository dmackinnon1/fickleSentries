# fickleSentries
Scripts and interface for a set of logic puzzles similar to those of Raymond Smullyan. 

## Overview

The "Fickle Sentries" is a puzzle type that both 'lady or tiger' and 'lion and unicorn' puzzles have a strong family resemblance to, illustrating how those two puzzle types are closely related.

The setup of the puzzle is as follows:

> You are at the entrance to a cave within which there is a treasure. The cave contains one of silver, gold, platinum, or diamonds. In this world, silver is worth less than gold, which is worth less than platinum, which is woth less than diamonds.  

> In front of the cave are two guards. If you can determine the contents of the cave based on the statements the guards make, the treasure is yours. Unfortunately, the guards are unreliable - the first guard lies whenever she is guarding silver or gold, but tells the truth otherwise, and the second lies whenever she is guarding platinum or diamonds, and tells the truth otherwise.

A puzzle may be something like:

- guard 1 says: "The cave contains silver.", 
- guard 2 says: "The cave does not contain diamonds."

Using this information, you must determine the contents of the cave.

## Building the Puzzles
In the build folder there is a Python script to generate the puzzles.
```
python fickleSentries.py
> There were 266 puzzles generated
```
