from pathlib import Path

import pandas as pd

DATASETS = {
    "dataset_v6_aarch64_c8g.large.zst": "AWS C8g (AArch64 Neoverse V2)",
    "dataset_v6_x86_64_c8a.large.zst": "AWS C8a (x86-64 AMD EPYC 9R45)",
    "dataset_v6_x86_64_c8i.large.zst": "AWS C8i (x86-64 Intel Xeon 6975P-C)",
    "dataset_v6_x86_64_laptop.zst": "Laptop (x86-64 Intel Core i7-1185G7)",
    "dataset_v6_x86_64_pc.zst": "PC (x86-64 AMD Ryzen 9 7900X3D)",
    "dataset_v6_aarch64_rpi3b.zst": "Raspberry Pi 3B+ (AArch64 Cortex A53)",
    "dataset_v6_aarch64_rpi4b.zst": "Raspberry Pi 4B (AArch64 Cortex A72)",
    "dataset_v6_aarch64_rpi5.zst": "Raspberry Pi 5 (AArch64 Cortex A76)",
}

DEFAULT_DATASET = "dataset_v6_x86_64_c8i.large.zst"

FEATURES = [
    "Pubkey (bytes)",
    "Privkey (bytes)",
    "Signature (bytes)",
    "Keygen (μs)",
    "Sign (μs)",
    "Verify (μs)",
]

_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

ALL_DATA = {filename: pd.read_pickle(_DATA_DIR / filename).reset_index() for filename in DATASETS}
