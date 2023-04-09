import os
from dotenv import load_dotenv
from moralis import evm_api
from requests import HTTPError


def get_block_hash_by_timestamp(timestamp):

    # load the environment variables from the .env file
    load_dotenv('../.env')

    # retrieve the API key from the environment
    api_key = os.environ.get('MORALIS_API_KEY')

    if api_key is None:
        raise ValueError("MORALIS_API_KEY environment variable is not set")

    params = {
        "chain": "eth",
        "date": timestamp
    }

    # make the API request to get the block number
    try:
        result = evm_api.block.get_date_to_block(
            params=params,
            api_key=api_key
        )
    except HTTPError as e:
        raise ValueError(f"No response from Moralis: {e}")

    # extract the block hash from the result
    block_hash = result['hash']

    # return the block hash
    return block_hash
