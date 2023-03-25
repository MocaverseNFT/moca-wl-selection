import random
import csv
from html_generator import generate_html
import datetime
import argparse


# Define the command line arguments
parser = argparse.ArgumentParser(description='Moca Whitelist Randomizer')
parser.add_argument('csv_file', type=str, help='Path to the CSV file containing the Moca data')
parser.add_argument('--max_wins_per_wallet', type=int, default=1, help='Maximum number of wins per wallet (default: 1)')
parser.add_argument('--xp_threshold', type=int, default=8, help='Moca XP threshold (default: 8)')
parser.add_argument('--num_winners', type=int, default=10, help='Number of winners to select (default: 10)')
parser.add_argument('--whitelist_name', type=str, default='moca', help='Whitelist name (default: "moca")')
# parser.add_argument('--blockhash', type=str, default='0x5dd66b23e557843a06b4860b36a33864b840edff79d8c52e9d11c1f84e3c2429', help='Blockhash for the randomization (default: "0x5dd66b23e557843a06b4860b36a33864b840edff79d8c52e9d11c1f84e3c2429")')
args = parser.parse_args()

# Define the required number of winners
num_winners = args.num_winners
wl_name = args.whitelist_name
max_wins_per_wallet = args.max_wins_per_wallet
xp_threshold = args.xp_threshold

# #TODO add function call to get block number and block hash with timestamp
# # Define the blockhash for the randomization
# # blocknumber: etherscan.io/block/16897664
# blockhash = args.blockhash

# num_winners = 5
# wl_name = 'club3'
# max_wins_per_wallet = 1
# xp_threshold = 16
blockhash='0x5dd66b23e557843a06b4860b36a33864b840edff79d8c52e9d11c1f84e3c2429'



# Read the CSV file and create a list of dictionaries
with open(args.csv_file, 'r') as f:
    reader = csv.DictReader(f)
    data = [row for row in reader]

# Initialize the wallets dictionary
wallets = {}

# Loop through each row in the data and add it to the wallets dictionary
for row in data:
    moca_id = int(row['moca_id'])
    wallet = row['wallet']
    moca_xp = int(row['moca_xp'])
    if wallet not in wallets:
        wallets[wallet] = []
    wallets[wallet].append({'id': moca_id, 'xp': moca_xp})

# Convert the wallets dictionary to a list of dictionaries with 'address' and 'mocas' keys
wallets = [{'address': wallet, 'mocas': mocas}
           for wallet, mocas in wallets.items()]

# Check for duplicate wallets
if len(set(wallet['address'] for wallet in wallets)) != len(wallets):
    raise ValueError('Duplicate wallets found')

# Check for duplicate Moca IDs
moca_ids = set()
for wallet in wallets:
    for moca in wallet['mocas']:
        if moca['id'] in moca_ids:
            raise ValueError(f'Duplicate Moca ID {moca["id"]} found')
        moca_ids.add(moca['id'])

# Sort the wallets list by address in alphabetical order
wallets = sorted(wallets, key=lambda wallet: wallet['address'])

# Define the seed phrase for the randomization
seed_phrase = wl_name + blockhash

# Set the seed for the randomization
random.seed(seed_phrase)

# Initialize the winners list and the wallet wins dictionary
winners = []
wallet_wins = {wallet['address']: 0 for wallet in wallets}

# Initialize the list of eligible Mocas
eligible_mocas = []


# Loop through each wallet and their Mocas
for wallet in wallets:

    # Get the list of Mocas for this wallet
    mocas = wallet['mocas']

    # Remove Mocas that have XP below the threshold
    mocas = [moca for moca in mocas if moca['xp'] >= xp_threshold]

    # Add the remaining Mocas to the list of eligible Mocas
    eligible_mocas.extend(mocas)


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
    total_weight = sum(moca['xp'] for moca in eligible_mocas)

    # Check if the total weight is zero
    if total_weight == 0:
        continue

    # Define the weights for each Moca
    weights = [moca['xp'] / total_weight for moca in eligible_mocas]

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


# Define timestamp as a string containing the current date and time
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Generate the HTML files
generate_html(wl_name, wallets,max_wins_per_wallet, xp_threshold, num_winners, seed_phrase, winners, timestamp)
