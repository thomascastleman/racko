# racko
An AI to play the card game Racko. 

While brainstorming strategies for this game, I found it difficult to find a compromise between approaches that make good decisions with the cards, yet also utilize what is given in the initial rack state.

In the end, I decided upon a strategy which maximizes the number of cards it can use from the initial state, and also maximizes its ability to accept future cards out of the stack.

The basic principle is:
- Cards that are exchanged into the rack become "static" i.e. they are never altered later in the game
- To determine whether or not a card can be accepted into the rack, the ranges between all static values are checked and if there is room in the card's corresponding range, then its value in that range is scaled to an index between the surrounding static values, which is where the card is inserted into the rack.

We could start with no static values, and just insert the first card we see into its corresponding index scaled from its position in the 1-50 range, but this would be entirely ignoring the potentially useful cards we are given at the beginning.

Since our AI only really "sees" the static values, starting with no statics is essentially building an ordered rack from scratch, which may be necessary, but in many cases is not

Instead, we try to maximize the number of cards in the initial rack state that we can declare "static" right off the bat, as this puts us closer to our end goal without having made any exchanges.

e.g. If our rack is:

11 23 17 22 9 49 38 48 15 45

then we could declare
11, 17, 22, 38, 45
as statics, since they are spread out and cover a good range of values, and then we only have 5 more values to fill before our rack is complete.
And, we can accept any values in the ranges:

11-17, 22-38, 38-45

The rest of the process is checking whether the available card can fit into one of these available ranges, and if so, making an exchange at the appropriate index and declaring that value static.
