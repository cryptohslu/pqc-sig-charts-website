import secrets
import time

from datetime import datetime
from pathlib import Path

import oqs
import pandas as pd


N_SAMPLES = 1
SIZE_MESSAGE = 32


def benchmark_pqc_sigs():
    nist_sec_level = []
    public_key_lengths = []
    secret_key_lenghts = []
    signature_lenghts = []
    # Measured times in μs
    keygen_times = []
    sign_times = []
    verify_times = []

    sig_algs = oqs.get_supported_sig_mechanisms()
    n_sig_algs = len(sig_algs)

    print("Benchmarking PQC sig algs")
    for n, alg_name in enumerate(sig_algs):
        print(f"{alg_name} {n + 1}/{n_sig_algs}", end="")
        with oqs.Signature(alg_name) as signer:
            with oqs.Signature(alg_name) as verifier:
                nist_sec_level.append(signer.claimed_nist_level)
                public_key_lengths.append(signer.length_public_key)
                secret_key_lenghts.append(signer.length_secret_key)
                signature_lenghts.append(signer.length_signature)

                # Measure keygen
                t = time.perf_counter_ns()
                for i in range(N_SAMPLES):
                    signer.generate_keypair()
                keygen_times.append((time.perf_counter_ns() - t) / N_SAMPLES / 1e3)
                print(".", end="")

                # Measure sign
                pubkey = signer.generate_keypair()
                message = secrets.token_bytes(SIZE_MESSAGE)
                t = time.perf_counter_ns()
                for i in range(N_SAMPLES):
                    signer.sign(message)
                sign_times.append((time.perf_counter_ns() - t) / N_SAMPLES / 1e3)
                print(".", end="")

                # Measure verify
                signature = signer.sign(message)
                t = time.perf_counter_ns()
                for i in range(N_SAMPLES):
                    verifier.verify(message, signature, pubkey)
                verify_times.append((time.perf_counter_ns() - t) / N_SAMPLES / 1e3)
                print(".✓")

    print("Saving dataframe", end="")
    df = pd.DataFrame(
        data={
            "Algorithm": oqs.get_supported_sig_mechanisms(),
            "NIST": nist_sec_level,
            "Pubkey (bytes)": public_key_lengths,
            "Privkey (bytes)": secret_key_lenghts,
            "Signature (bytes)": signature_lenghts,
            "Keygen (μs)": keygen_times,
            "Sign (μs)": sign_times,
            "Verify (μs)": verify_times,
        }
    )
    # df["Keygen (μs)"] = df["Keygen (μs)"].map(lambda x: f"{x:.1f}")
    # df["Sign (μs)"] = df["Sign (μs)"].map(lambda x: f"{x:.1f}")
    # df["Verify (μs)"] = df["Verify (μs)"].map(lambda x: f"{x:.1f}")
    df.set_index(["NIST", "Algorithm"], inplace=True)
    df.sort_index(inplace=True)
    print(" ✓")
    return df


def main():
    df = benchmark_pqc_sigs()
    filename = datetime.now().isoformat() + ".zst"
    df.to_pickle(
        Path(__file__).resolve().parent.parent / "data" / filename, compression="zstd"
    )


if __name__ == "__main__":
    main()
