from algosdk.v2client import indexer

# Connect to AlgoNode's free TestNet indexer
indexer_client = indexer.IndexerClient(
    indexer_token="",  
    indexer_address="https://testnet-idx.algonode.cloud"
)

# Replace with your actual ASA ID after creation
asset_id = 745896746  
asset_info = indexer_client.asset_info(asset_id)
asset_info = indexer_client.asset_info(asset_id)
params = asset_info["asset"]["params"]

print("Token Name:", params.get("name"))
print("Symbol:", params.get("unit-name"))
print("Total Supply:", params.get("total"))
print("Decimals:", params.get("decimals"))
print("Creator:", params.get("creator"))

