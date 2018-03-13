# shapleyvalue
This pyhton function calculates the Shapley value of a TU game.

Examples are provided: calculate the Shapley Shubik index of the UN security council or the EU 27 (after Brexit)

Description of the algorithm
The method proceeds by iterating over all coalitions, starting with smaller coalitions. For each coalition, the potential is calculated, and partially added to supercoaltions containing one more player. Adding the coalition value, one gets the potential of that coalition.
Finally, Shapley value of player i = potential(playerset) - potential(playerset\i).
More information on Shapley value on wikipedia: https://en.wikipedia.org/wiki/Shapley_value

Author: Frank Huettner www.frankhuettner.de
