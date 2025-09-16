# create_asa.py
import json, hashlib, time
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import AssetConfigTxn



# flexible import for AssetConfigTxn (works across SDK versions)
try:
    from algosdk.transaction import AssetConfigTxn, AssetTransferTxn
except Exception:
    from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn

# ---------- CONFIG ----------
CREATOR_MNEMONIC = "trade surface crawl patch banner only very another stadium lawn pitch coach sorry emerge tray there often inch present step social vast buyer absorb resource"
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""   # AlgoNode TestNet = no token

# ---------- prepare keys + client ----------
creator_private_key = mnemonic.to_private_key(CREATOR_MNEMONIC)
creator_address = account.address_from_private_key(creator_private_key)
algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

print("Using address:", creator_address)

# ---------- optional: metadata you want anchored (example) ----------
metadata = {
    "company": "Pharm_Trust",
    "token_for": "batch markers / provenance",
    "created_by": "Pharm_Trust",
    "date": "2025-09-16",
    "notes": "This metadata can be stored on IPFS and referenced by asset url + metadataHash."
}
# compute metadata_hash (32 bytes)
metadata_bytes = json.dumps(metadata, separators=(',', ':'), sort_keys=True).encode()
metadata_hash = hashlib.sha256(metadata_bytes).digest()

# If you uploaded your metadata to IPFS, set asset_url to ipfs://<CID>
asset_url = "https://pharmtrust.example/metadata.json"  # placeholder; optional

# ---------- create ASA transaction ----------
params = algod_client.suggested_params()

txn = AssetConfigTxn(
    sender=creator_address,
    sp=params,
    total=1000000,                     # total supply (1,000,000)
    default_frozen=False,
    unit_name="PHRT",                  # ticker
    asset_name="Pharm Trust Token",    # full name
    manager=creator_address,           # you control it
    reserve=None,                      # no reserve account
    freeze=None,                       # no freeze account
    clawback=None,                     # no clawback account
    url="https://pharmtrust.example.com",  # optional link
    decimals=0,                        # indivisible token
    strict_empty_address_check=False   # allow empty addresses
)


# sign and send
stxn = txn.sign(creator_private_key)
txid = algod_client.send_transaction(stxn)
print("Create ASA tx submitted. txid =", txid)

# helper: wait for confirmation
def wait_for_confirmation(client, txid, timeout=30):
    start = time.time()
    last_round = client.status().get('last-round')
    while True:
        try:
            txinfo = client.pending_transaction_info(txid)
            if txinfo.get('confirmed-round', 0) > 0:
                return txinfo
        except Exception:
            pass
        if time.time() - start > timeout:
            raise Exception("Timeout waiting for tx confirmation")
        last_round += 1
        client.status_after_block(last_round)

confirmed_txn = wait_for_confirmation(algod_client, txid)
print("Confirmed in round:", confirmed_txn.get("confirmed-round"))
asset_id = confirmed_txn["asset-index"]
print("Created ASA Asset ID:", asset_id)

# print on-chain asset params for quick check
asset_info = algod_client.asset_info(asset_id)
print("\nAsset params (on-chain):")
print(json.dumps(asset_info["params"], indent=2))
