from pathlib import Path
import pandas as pd

OQS_VERSION = "0.12.0"
DATASET = "dataset_v2.zst"

FEATURES = [
    "Pubkey (bytes)",
    "Privkey (bytes)",
    "Signature (bytes)",
    "Keygen (μs)",
    "Sign (μs)",
    "Verify (μs)",
]

data = pd.read_pickle(Path(__file__).resolve().parent.parent.parent / "data" / DATASET)
