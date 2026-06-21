#!/usr/bin/env python3
"""South African ID number generator.

Generates valid SA ID numbers for specified date ranges using the Luhn
algorithm as implemented by the Department of Home Affairs (left-to-right).
"""

import argparse
import calendar
import multiprocessing as mp
import os
import sys
import time


def luhn_check_digit(payload):
    """Compute SA ID Luhn check digit for a 12-digit payload (left-to-right)."""
    total = 0
    for i, ch in enumerate(payload):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return (10 - total % 10) % 10


def generate_ids_for_month(args):
    """Generate all valid IDs for a single year-month pair."""
    full_year, month = args
    yy = f"{full_year % 100:02d}"
    mm = f"{month:02d}"
    _, days_in_month = calendar.monthrange(full_year, month)

    ids = []
    for day in range(1, days_in_month + 1):
        dd = f"{day:02d}"
        prefix = f"{yy}{mm}{dd}"
        for seq in range(10000):
            ssss = f"{seq:04d}"
            for cit in (0, 1):
                payload = f"{prefix}{ssss}{cit}8"
                ids.append(f"{payload}{luhn_check_digit(payload)}")
    return ids


def validate_batch(ids):
    """Filter a batch through the za-id-number library and Luhn check."""
    from za_id_number.za_id_number import SouthAfricanIdentityNumber

    valid = []
    for id_str in ids:
        try:
            sa = SouthAfricanIdentityNumber(id_str)
            if not sa.identity_length():
                continue
            if sa.birthdate is None:
                continue
            expected = luhn_check_digit(id_str[:12])
            if int(id_str[12]) != expected:
                continue
            valid.append(id_str)
        except Exception:
            continue
    return valid


def build_work_units(start_year, end_year):
    """Return list of (year, month) tuples covering the requested range."""
    return [
        (year, month)
        for year in range(start_year, end_year + 1)
        for month in range(1, 13)
    ]


def estimate_count(start_year, end_year):
    """Estimate total ID count for the given range."""
    total = 0
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            _, days = calendar.monthrange(year, month)
            total += days * 10000 * 2
    return total


def main():
    parser = argparse.ArgumentParser(
        description="Generate valid South African ID numbers"
    )
    parser.add_argument(
        "-s", "--start-year", type=int, default=1900,
        help="start year (default: 1900)",
    )
    parser.add_argument(
        "-e", "--end-year", type=int, default=None,
        help="end year (default: current year)",
    )
    parser.add_argument(
        "-o", "--output", default="valid_ids.txt",
        help="output file path (default: valid_ids.txt)",
    )
    parser.add_argument(
        "-w", "--workers", type=int, default=None,
        help="parallel worker count (default: CPU count)",
    )
    parser.add_argument(
        "--validate", action="store_true",
        help="cross-check each ID with the za-id-number library (much slower)",
    )
    parser.add_argument(
        "-n", "--limit", type=int, default=None,
        help="stop after generating N IDs",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="estimate output size without generating",
    )
    args = parser.parse_args()

    if args.end_year is None:
        from datetime import date
        args.end_year = date.today().year

    if args.start_year < 0 or args.end_year < 0:
        sys.exit("Error: years must be non-negative")
    if args.start_year > args.end_year:
        sys.exit("Error: start year must be <= end year")

    work_units = build_work_units(args.start_year, args.end_year)
    total_months = len(work_units)
    est_ids = estimate_count(args.start_year, args.end_year)
    est_size_gb = est_ids * 14 / (1024 ** 3)

    if args.dry_run:
        print(f"Range: {args.start_year}-{args.end_year} ({total_months} months)")
        print(f"Estimated IDs: {est_ids:,}")
        print(f"Estimated file size: {est_size_gb:.1f} GB")
        return

    workers = args.workers or mp.cpu_count()
    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    limit_str = f", limit {args.limit:,}" if args.limit else ""
    print(f"Generating SA IDs: {args.start_year}-{args.end_year} ({est_ids:,} estimated{limit_str})")
    print(f"Workers: {workers} | Output: {args.output}")
    if args.validate:
        print("Library validation enabled (slower)")

    start_time = time.time()
    total_ids = 0
    done = False

    with open(args.output, "w") as fh, mp.Pool(processes=workers) as pool:
        for i, batch in enumerate(
            pool.imap(generate_ids_for_month, work_units), 1
        ):
            if args.validate:
                batch = validate_batch(batch)
            if args.limit and total_ids + len(batch) >= args.limit:
                batch = batch[: args.limit - total_ids]
                done = True
            fh.write("\n".join(batch))
            fh.write("\n")
            total_ids += len(batch)
            elapsed = time.time() - start_time
            pct = i / total_months * 100
            rate = total_ids / elapsed if elapsed > 0 else 0
            print(
                f"\r[{pct:5.1f}%] {i}/{total_months} months | "
                f"{total_ids:,} IDs | {rate:,.0f} IDs/s",
                end="",
                flush=True,
            )
            if done:
                break

    elapsed = time.time() - start_time
    print(f"\nDone: {total_ids:,} IDs written to {args.output} in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
