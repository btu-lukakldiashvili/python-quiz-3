## Crypto CLI (Python Quiz - 3)

Crypto CLI is simple program (cli like) that can be used to view crypto prices, save token data and etc.

App uses public Coingecko API (does not require API key)<br>
More info at: https://www.coingecko.com/en/api#explore-api


### Commands:

help () -> displays all available commands<br>
exit () -> stops and exits out of the program<br>

find (string: name) -> finds token with similar name<br>
price (string: token_id) -> gets and displays price for specified token<br>
dump (string: token_id) -> gets and dump json info for specified token<br>
save (string: token_id) -> saves given tokens current data to database<br>
