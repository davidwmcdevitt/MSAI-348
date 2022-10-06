# HW2—Game Engine

## Introduction

Connect 4 (also known as Four Up, Plot Four, Find Four, Captain's Mistress, Four in a Row, Drop Four, and Gravitrips) is a two-player connection board game, in which the players choose a color and then take turns dropping colored tokens into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the lowest available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own tokens. Connect 4 is a solved game. The first player to move can always win by playing the right moves.

You can visit https://www.youtube.com/watch?v=utXzIFEVPjA to learn more about the game.

## Description

In this homework, you'll be implementing Minimax and Alpha-Beta Pruning for an agent playing Connect 4. Wait, isn't Alpha-Beta Pruning a variant of Minimax? Yes, it is. It's just that here we're using Minimax and Alpha-Beta Pruning to respectively refer to Minimax WITHOUT Alpha-Beta Pruning and Minimax WITH Alpha-Beta Pruning.

But first, you should get practically familiar with how the game is played, not just be familiar with the rules of the game. To do this, play the game with the provided code by running ``environment.py``. You've been distributed a codebase that includes an interface for playing the game in a variety of modes. Notably, you don't need to actually make the game of Connect 4 — you just need to make an agent that plays it.

Playing the game interactively has been tested on Linux and Mac. However, this is not required for completing the assignment and is only provided to help you to get familiar with the game (and for your entertainment). If you have trouble playing the game on Windows, please let us know.

## What you need to do

Now that you know how the game is played, it is time to make your own intelligent players of the game. You will do this my implementing one player that uses Minimax and another player that uses Alpha-Beta Pruning.

### Minimax

Minimax is an algorithm for determing the best move in an adversarial game. It seeks to minimize the maximum loss posed by the opponent’s strategy. Minimax is typically employed in competitive, discrete-, and finite-space games with abstracted time and perfect information. You will complete the implementation of the *minimax()* function in ``student_code.py``.

### Alpha-Beta Pruning

You may notice that Minimax starts to get terribly slow when you set your maximum search depth to values above, say, 4. This makes perfect sense when you think about the fact that the total number of nodes in your game tree is the branching factor to the power of the search depth. For comparatively "bushy" games (e.g., chess, Go, etc.) the branching factor is prohibitively large, which is why agents that play these games use clever algorithms to choose what move to make next.

One such clever algorithm (although still not clever enough to do well at games like Go) is a modification of Minimax known as Alpha-Beta Pruning. The two algorithms are, at their core, the same. The distinction is that A-B Pruning ignores subtrees that are provably worse than any that it has already considered. This drastically reduces the runtime of the algorithm. Since A-B Pruning is a variant of Minimax, you aren't really writing a new algorithm; rather, you're taking your implementation of Minimax and making it a little smarter.

Strictly speaking, it doesn't change the upper bound on the algorithm's runtime, since in the worst-case, one must still search the entire tree. In practice, however, the performance difference is very noticeable.

As with Minimax, your task is to complete the implementation of the *minimaxAlphaBeta()* function in ``student_code.py``.

## How to run your code

BEFORE YOU PROCEED, look at lines 237 and 238 in ``student_code.py``. Let's give the lines names. Let's call line 237 **"MM_run"** and line 238 **"AB_run"**. Why are we naming them? Well, once you start writing code in the file, the lines will shift and referring to them by line number won't make sense, so we'll refer to them by their names. Likewise, in ``test_headless.py``, let's refer to lines 191 and 192 by the same names, and let's do the same in ``test.py`` for lines 9 and 10.

For Minimax, complete the *minimax()* function in ``student_code.py``. Once you've done that, run the file to play the game using the graphical user interface (GUI). If you notice a lag, that's not unusual. If you are successfully able to play the game, then copy your code for the *minimax()* function over to the same function in ``test_headless.py``. Once you've done that, run ``test.py`` to see if all the test cases pass.

For Alpha-Beta Pruning, complete the *minimaxAlphaBeta()* function in  ``student_code.py``. Once you've done that, comment *MM_run* out and uncomment *AB_run* before running the file to play the game using the GUI. The AI player should now be smarter than when Minimax was used. If you are successfully able to play the game, then copy your code for the *minimaxAlphaBeta()* function over to the same function in ``test_headless.py``. In the same file (``test_headless.py``), comment *MM_run* out and uncomment *AB_run*. Now go to ``test.py`` and comment *MM_run* out while uncommenting *AB_run*. Once you've done all this, run ``test.py`` to see if all the test cases pass.

As stated in class, if you think your methods are correct but the test cases are still not passing, then please reach out to the instructor and the TAs via Campuswire.

Finally, note that the given code was tested using Pythong 3.9.5.
