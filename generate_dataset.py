import secrets
import time
from datetime import datetime
from pathlib import Path

import Crypto
import oqs
import pandas as pd
from Crypto.Hash import SHA512, SHAKE256
from Crypto.PublicKey import ECC, RSA
from Crypto.Signature import DSS, eddsa, pss

N_SAMPLES = 10**3
SIZE_MESSAGE = 32


def benchmark_traditional_sigs():
    nist_sec_level = [1, 1, 1, 1, 3, 5, 1, 5]
    public_key_lengths = []
    secret_key_lenghts = []
    signature_lenghts = []
    # Measured times in μs
    keygen_times = []
    sign_times = []
    verify_times = []
    sig_algs = [
        "RSASSA-PSS (2048)",
        "RSASSA-PSS (3072)",
        "RSASSA-PSS (4096)",
        "P-256",
        "P-384",
        "P-521",
        "Ed25519",
        "Ed448",
    ]
    _sig_algs = [RSA, ECC]
    _rsa_bits = [2048, 3072, 4096]
    _ecdsa = [
        "p256",
        "p384",
        "p521",
    ]
    _eddsa = [
        "ed25519",
        "ed448",
    ]
    n_sig_algs = len(sig_algs)

    print("Benchmarking traditional sig algs (RSA, ECC)")

    for alg in _sig_algs:
        if alg == RSA:
            for bits in _rsa_bits:
                print(f"RSASSA-PSS ({bits})", end="", flush=True)
                secret_key_lenghts.append(len(alg.generate(bits).export_key(format="DER")))
                public_key_lengths.append(len(alg.generate(bits).public_key().export_key(format="DER")))

                # Measure keygen
                t = time.perf_counter_ns()
                for i in range(N_SAMPLES):
                    alg.generate(bits)
                keygen_times.append((time.perf_counter_ns() - t) / N_SAMPLES / 1e3)
                print(".", end="", flush=True)

                # Measure sign
                privkey = alg.generate(bits)
                signer = pss.new(privkey)
                message = secrets.token_bytes(SIZE_MESSAGE)
                h = SHA512.new(message)
                signature_lenghts.append(len(signer.sign(h)))

                t = time.perf_counter_ns()
                for _ in range(N_SAMPLES):
                    signer.sign(h)
                sign_times.append((time.perf_counter_ns() - t) / N_SAMPLES / 1e3)
                print(".", end="", flush=True)

                # Measure verify
                message = secrets.token_bytes(SIZE_MESSAGE)
                h = SHA512.new(message)
                signature = signer.sign(h)
                pubkey = privkey.public_key()
                verifier = pss.new(pubkey)
                t = time.perf_counter_ns()
                for _ in range(N_SAMPLES):
                    verifier.verify(h, signature)
                verify_times.append((time.perf_counter_ns() - t) / N_SAMPLES / 1e3)
                print(".✓")

        elif alg == ECC:
            for curve in _ecdsa:
                print(f"ECDSA ({curve})", end="", flush=True)
                secret_key_lenghts.append(len(alg.generate(curve=curve).export_key(format="DER")))
                public_key_lengths.append(len(alg.generate(curve=curve).public_key().export_key(format="DER")))

                # Measure keygen
                t = time.perf_counter_ns()
                for _ in range(N_SAMPLES):
                    alg.generate(curve=curve)
                keygen_times.append((time.perf_counter_ns() - t) / N_SAMPLES / 1e3)
                print(".", end="", flush=True)

                # Measure sign
                privkey = alg.generate(curve=curve)
                signer = DSS.new(privkey, mode="fips-186-3")
                message = secrets.token_bytes(SIZE_MESSAGE)
                h = SHA512.new(message)
                signature_lenghts.append(len(signer.sign(h)))

                t = time.perf_counter_ns()
                for _ in range(N_SAMPLES):
                    signer.sign(h)
                sign_times.append((time.perf_counter_ns() - t) / N_SAMPLES / 1e3)
                print(".", end="", flush=True)

                # Measure verify
                message = secrets.token_bytes(SIZE_MESSAGE)
                h = SHA512.new(message)
                signature = signer.sign(h)
                pubkey = privkey.public_key()
                verifier = DSS.new(pubkey, mode="fips-186-3")
                t = time.perf_counter_ns()
                for i in range(N_SAMPLES):
                    verifier.verify(h, signature)
                verify_times.append((time.perf_counter_ns() - t) / N_SAMPLES / 1e3)
                print(".✓")

            print("EdDSA", end="", flush=True)
            for curve in _eddsa:
                print(f"EdDSA ({curve})", end="", flush=True)
                secret_key_lenghts.append(len(alg.generate(curve=curve).export_key(format="DER")))
                public_key_lengths.append(len(alg.generate(curve=curve).public_key().export_key(format="DER")))

                # Measure keygen
                t = time.perf_counter_ns()
                for _ in range(N_SAMPLES):
                    alg.generate(curve=curve)
                keygen_times.append((time.perf_counter_ns() - t) / N_SAMPLES / 1e3)
                print(".", end="", flush=True)

                # Measure sign
                privkey = alg.generate(curve=curve)
                signer = eddsa.new(privkey, mode="rfc8032")
                message = secrets.token_bytes(SIZE_MESSAGE)
                if curve == "ed25519":
                    h = SHA512.new(message)
                elif curve == "ed448":
                    h = SHAKE256.new(message)
                else:
                    raise RuntimeError
                signature_lenghts.append(len(signer.sign(h)))

                t = time.perf_counter_ns()
                for _ in range(N_SAMPLES):
                    signer.sign(h)
                sign_times.append((time.perf_counter_ns() - t) / N_SAMPLES / 1e3)
                print(".", end="", flush=True)

                # Measure verify
                message = secrets.token_bytes(SIZE_MESSAGE)
                if curve == "ed25519":
                    h = SHA512.new(message)
                elif curve == "ed448":
                    h = SHAKE256.new(message)
                else:
                    raise RuntimeError
                signature = signer.sign(h)
                pubkey = privkey.public_key()
                verifier = eddsa.new(pubkey, mode="rfc8032")
                t = time.perf_counter_ns()
                for _ in range(N_SAMPLES):
                    # Temporary workaround (https://github.com/Legrandin/pycryptodome/issues/862)
                    if curve == "ed448":
                        h = SHAKE256.new(message)
                    verifier.verify(h, signature)
                verify_times.append((time.perf_counter_ns() - t) / N_SAMPLES / 1e3)
                print(".✓")

    print("Saving dataframe", end="")
    df = pd.DataFrame(
        data={
            "Algorithm": sig_algs,
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

    print("\nSaving dataframe", end="")
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
    t0 = time.perf_counter()
    df_traditional = benchmark_traditional_sigs()
    print()
    df_pqc = benchmark_pqc_sigs()
    df = pd.concat([df_traditional, df_pqc]).sort_index()
    t1 = time.perf_counter() - t0
    df.attrs = {
        "timestampt": datetime.isoformat(datetime.now()),
        "duration": t1,
        "n_samples": N_SAMPLES,
        "liboqs_version": oqs.oqs_python_version(),
        "pycryptodome_version": Crypto.__version__,
    }
    filename = datetime.now().isoformat() + ".zst"
    df.to_pickle(Path(__file__).resolve().parent / "data" / filename, compression="zstd")
    print(f"\nDataFrame generated in {t1 / 60 / 60:.0f}h {(t1 / 60) % 60:.0f}m {t1 % 60}s")


if __name__ == "__main__":
    main()
