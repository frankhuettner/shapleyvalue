# shapleyvalue
Calculates the Shapley value (using the potential function)
This pyhton function calculates the Shapley value of a TU game

Examples are provided: calculate the Shapley Shubik index of the UN security council or the EU 27 (after Brexit)

Description of the algorithm
The method proceeds by iterating over all coalitions, starting with smaller coalitions. More concretely, for each coalition:

the potential is calculated, and added to supercoaltions containing one more player ... 
Shapley value of player i = potential(playerset) - potential(playerset\i).
More information on Shapley value on wikipedia: https://en.wikipedia.org/wiki/Shapley_value

Author: Frank Huettner www.frankhuettner.de
