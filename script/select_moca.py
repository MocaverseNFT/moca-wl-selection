import random
import csv
from html_generator import generate_html
import datetime
import argparse
import json
from get_block import get_block_hash_by_timestamp


# Define the command line arguments
parser = argparse.ArgumentParser(description='Moca Whitelist Randomizer')
parser.add_argument('csv_file', type=str,
                    help='Path to the CSV file containing the Moca data')
parser.add_argument('--max_wins_per_wallet', type=int, default=1,
                    help='Maximum number of wins per wallet (default: 1)')
parser.add_argument('--stake_at_week', type=int, default=1,
                    help='Week number moca has to be staked to join (default: 1)')
parser.add_argument('--num_winners', type=int, default=10,
                    help='Number of winners to select (default: 10)')
parser.add_argument('--whitelist_name', type=str,
                    default='moca', help='Whitelist name (default: "moca")')
parser.add_argument('--date', type=str, default='2023-03-24', help='Timestamp to get Blockhash for the randomization (default: "2023-03-24")')
args = parser.parse_args()

# Define the required number of winners
num_winners = args.num_winners
wl_name = args.whitelist_name
max_wins_per_wallet = args.max_wins_per_wallet

# TODO fix case if stake_at_week is last week, calculate the week number from timestamp
stake_at_week = args.stake_at_week

# Define the blockhash for the randomization
date = args.date
timestamp = f'{date} 13:00:00Z'
blockhash =  get_block_hash_by_timestamp(timestamp)
print(f'Get block hash by timestamp {timestamp}, blockhash is {blockhash}')

# Define the seed phrase for the randomization
seed_phrase = wl_name + blockhash
print(f'Seed Phrase is {seed_phrase}')

# Read the CSV file and create a list of dictionaries
with open(args.csv_file, 'r') as f:
    reader = csv.DictReader(f)
    data = [row for row in reader]

with open('data/moca_name_mapping.json', 'r') as f:
    moca_mapping = json.load(f)

# Initialize the wallets dictionary and the list of eligible Mocas
wallets = {}
eligible_mocas = []

# Loop through each row in the data
for row in data:
    moca_id = int(row['moca_id'])
    wallet = row['wallet']
    moca_xp = float(row['moca_xp'])
    week = int(row['week'])
    moca_name = next((item['moca_name']
                     for item in moca_mapping if item['token_id'] == str(moca_id)), None)

    wallets.setdefault(wallet, []).append({'id': moca_id, 'xp': moca_xp, 'name': moca_name, 'week': week})

    # Check if the Moca has enough XP to be eligible
    if week == stake_at_week:
        eligible_mocas.append(
            {'id': moca_id, 'xp': moca_xp, 'name': moca_name, 'week': week})

# Convert the wallets dictionary to a list of dictionaries with 'address' and 'mocas' keys
wallets = [{'address': wallet, 'mocas': mocas}
           for wallet, mocas in wallets.items()]

# Check for duplicate wallets and Moca IDs
moca_ids = set()
for wallet in wallets:
    if wallet['address'] in moca_ids:
        raise ValueError(f'Duplicate wallet address {wallet["address"]} found')
    moca_ids.add(wallet['address'])

    for moca in wallet['mocas']:
        if moca['id'] in moca_ids:
            raise ValueError(f'Duplicate Moca ID {moca["id"]} found')
        moca_ids.add(moca['id'])

# Initialize the winners list and the wallet wins dictionary
winners = []
wallet_wins = {wallet['address']: 0 for wallet in wallets}

# Sort the wallets list by address in alphabetical order
wallets = sorted(wallets, key=lambda wallet: wallet['address'])

# Set the seed for the randomization
random.seed(seed_phrase)

# Loop until we have the required number of winners
while len(winners) < num_winners:
    # Count the number of eligible Mocas
    num_eligible_mocas = len(eligible_mocas)

    # Raise an error if there are not enough eligible Mocas to choose from
    if num_eligible_mocas < num_winners:
        raise ValueError(
            f'There are not enough eligible Mocas to choose from. Found {num_eligible_mocas} eligible Mocas, but need {num_winners}.')

    # Shuffle the wallets list to randomize the order
    random.shuffle(wallets)

    # Compute the total weight of the Mocas
    total_weight = sum(moca['xp']*10 for moca in eligible_mocas)

    # Check if the total weight is zero
    if total_weight == 0:
        continue

    # Define the weights for each Moca
    weights = [int(moca['xp']*10) / total_weight for moca in eligible_mocas]

    # Randomly select a Moca based on the weights
    moca = random.choices(eligible_mocas, weights=weights)[0]

    # Remove the selected Moca from the list of eligible Mocas
    eligible_mocas = [m for m in eligible_mocas if m['id'] != moca['id']]

    # Check if the Moca has already been assigned to a winner
    if any(moca['id'] == winner['moca_id'] for winner in winners):
        raise ValueError(
            f'Moca ID {moca["id"]} has already been assigned to a winner')

    # Find the wallet that owns the selected Moca
    for wallet in wallets:
        if moca in wallet['mocas']:
            address = wallet['address']
            break

    # Check if the wallet has already won the maximum number of times
    if wallet_wins[address] >= max_wins_per_wallet:
        # Remove all the Mocas in the wallet from the list of eligible Mocas
        eligible_mocas = [
            m for m in eligible_mocas if m not in wallet['mocas']]
        continue

    # Add the Moca and wallet to the winners list
    winners.append({'moca_id': moca['id'], 'address': address})
    wallet_wins[address] += 1

# Print the list of winners
for i, winner in enumerate(winners):
    print(
        f'Winner #{i+1}: Moca #{winner["moca_id"]} owned by {winner["address"]}')
    moca_id = winner['moca_id']
    moca_name = moca_mapping[moca_id]['moca_name']
    winner['moca_name'] = moca_name

# Define timestamp as a string containing the current date and time
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Generate the HTML files
generate_html(wl_name, wallets, max_wins_per_wallet, stake_at_week,
              num_winners, seed_phrase, winners, timestamp)
