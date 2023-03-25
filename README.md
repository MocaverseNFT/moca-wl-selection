# Mocaverse WL Selection

This repository contains the code for generating the selection summaries of the Mocaverse White List (WL) for our moca holder. The summaries are generated using a Python script that run randomization process and generates an HTML file for each WL selection.



## What is the selection design?
`selec_moca.py` script randomly selects a specified number of winners from a staked list of Moca NFT owners. The script reads data from a CSV file containing information about Moca owners, including their wallets, their Moca IDs, and the corresponding  Moca XP (experience points). It then filters the Mocas based on a minimum XP threshold and randomly selects a Moca from the remaining eligible Mocas.


### Rules for selection
- Moca XP is the weight
- Moca will only win once
- Remove Mocas that have XP below the threshold from the list of eligible Mocas
- Remove the selected Moca from the list of eligible Mocas after each selection
- Check if the wallet has already won the maximum number of times, then remove all the Mocas in the wallet from the list of eligible Mocas


### How to use?

The script also has several optional arguments that allow you to customize the selection process. For example, you can specify the maximum number of wins per wallet, the XP threshold, the number of winners to select, and the name of the whitelist.

After selecting the winners, the script generates HTML files containing the details of the winners and saves them in a directory named after the whitelist.


The script has several command line arguments that you can use to customize the selection process. Here are the arguments:

- csv_file: The path to the CSV file containing the Moca data (required).
- --max_wins_per_wallet: The maximum number of wins per wallet (default: 1).
- --xp_threshold: The Moca XP threshold (default: 8).
- --num_winners: The number of winners to select (default: 10).
- --whitelist_name: The whitelist name (default: "moca").


Here's an example of how to use these arguments:

`python moca_wl_selection.py data/moca.csv --max_wins_per_wallet 2 --xp_threshold 8 --num_winners 5 --whitelist_name moca`


## Project website and social media

To learn more about MocaVerse and its NFT drops, please visit our website:

https://www.mocaverse.xyz/

You can also follow us on Twitter for updates and announcements:

https://twitter.com/MocaverseNFT

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.