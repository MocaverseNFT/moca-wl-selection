# Mocaverse WL Selection

This repository contains the code for generating the selection summaries of the Mocaverse White List (WL) for our moca holder. The summaries are generated using a Python script that run randomization process and generates an HTML file for each WL selection.



## What is the selection design?
`select_moca.py` script randomly selects a specified number of winners from a staked list of Moca NFT owners. The script reads data from a CSV file containing information about Moca owners, including their wallets, their Moca IDs, and the corresponding  Moca XP (experience points). It then filters the Mocas based on a minimum XP threshold and randomly selects a Moca from the remaining eligible Mocas.


### Rules for selection
- Moca XP is the weight
- Moca will only win once
- Remove Mocas that have XP below the threshold from the list of eligible Mocas
- Remove the selected Moca from the list of eligible Mocas after each selection
- Check if the wallet has already won the maximum number of times, then remove all the Mocas in the wallet from the list of eligible Mocas


### How to use?

The script also has several optional arguments that allow you to customize the selection process. For example, you can specify the maximum number of wins per wallet, the staked week, the number of winners to select, and the name of the whitelist.

After selecting the winners, the script generates HTML files containing the details of the winners and saves them in a directory named after the whitelist.

The script has several command line arguments that you can use to customize the selection process. Here are the arguments:

- csv_file: The path to the CSV file containing the Moca data (required).
- `--max_wins_per_wallet`: The maximum number of wins per wallet (default: 1).
- `--stake_at_week`: Week number moca has to be staked to join (default: 1).
- `--num_winners`: The number of winners to select (default: 10).
- `--whitelist_name`: The whitelist name (default: "moca").
- `--date`: Timestamp to get Blockhash for the randomization (default: "2023-03-24").

The script will call Moralis to get the block hash of the closest block given the date. You need to supplement a moralis key in a `.env` file with:
`MORALIS_API_KEY=<your-api-key>`

Here's an example of how to use these arguments:

`python select_moca.py data/moca_data_test.csv --max_wins_per_wallet 2 --stake_at_week1 --num_winners 5 --whitelist_name moca --date 2023-04-24`

Check `script/data/moca_data_test.csv` for how the data should look like. 


## Project website and social media

To Check your Moca XP, please visit our leaderboard:

https://www.mocaverse.xyz/mocana

To learn more about Mocaverse and its NFT drops, please visit our website:

https://www.mocaverse.xyz/

You can also follow us on Twitter for updates and announcements:

https://twitter.com/MocaverseNFT

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
