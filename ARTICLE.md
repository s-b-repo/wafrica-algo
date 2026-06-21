# How I Built a High-Performance South African ID Number Generator in Python

## Reverse-Engineering the Luhn Algorithm Behind 60 Million Identities

---

Every South African citizen carries a 13-digit identity number. It encodes your date of birth, your gender, your citizenship status, and a mathematical checksum that validates the entire sequence. That checksum uses the Luhn algorithm — the same formula that validates your credit card number every time you shop online.

I wanted to understand how it works. So I built a tool that generates every valid South African ID number ever possible — all 900 million of them.

Here's what I learned, what went wrong, and how I made it fast.

---

## What's Inside a South African ID Number?

Let's break down the 13 digits: `YYMMDDSSSSCAZ`

| Position | Digits | Meaning |
|----------|--------|---------|
| 1-2 | `YY` | Year of birth (last two digits) |
| 3-4 | `MM` | Month of birth |
| 5-6 | `DD` | Day of birth |
| 7-10 | `SSSS` | Gender sequence — 0000-4999 for female, 5000-9999 for male |
| 11 | `C` | Citizenship — 0 = SA citizen, 1 = permanent resident |
| 12 | `A` | Previously used for race classification (now fixed at 8) |
| 13 | `Z` | Luhn check digit |

That last digit is where the maths lives. It's calculated using the **Luhn algorithm**, a checksum formula invented by IBM scientist Hans Peter Luhn in 1954. If you change even a single digit in the ID number, the check digit breaks and the number fails validation.

---

## The Luhn Algorithm: A Quick Primer

The Luhn algorithm is deceptively simple:

1. Starting from the **rightmost digit**, move left
2. **Double every second digit**
3. If doubling produces a number greater than 9, subtract 9
4. Sum all the digits
5. If the total is divisible by 10, the number is valid

For generating an ID, you compute digits 1-12 and then calculate what digit 13 must be to make the total divisible by 10. That's your check digit.

Here's the Python implementation:

```python
def luhn_check_digit(payload):
    total = 0
    for i, ch in enumerate(payload):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return (10 - total % 10) % 10
```

Twelve digits go in. One check digit comes out. Deterministic, fast, and elegant.

---

## The SA Luhn Fumble

Here's where it gets interesting. According to research by Ryan Neil Parker, South Africa's Department of Home Affairs implemented the Luhn algorithm **differently** from the global standard. While most systems (credit cards, IMEI numbers) process digits from right to left, the SA implementation reportedly processes left to right.

This has been called the "SA ID Fumble" — whether it was a deliberate choice, a technical workaround, or simply a mistake remains unclear. What matters for practical purposes is that the standard Luhn implementation produces ID numbers that pass real-world validation. I confirmed this by testing generated IDs against multiple online SA ID validators.

---

## From Single-Threaded to Multicore

My first version was painfully slow. A single Python loop iterating through every possible combination:

- 126 years (1900-2026)
- 365 days per year (approximately)
- 10,000 gender sequences per day
- 2 citizenship values

That's roughly **920 million combinations**. On a single core, with the `za-id-number` library validating each one, it would take **days**.

### The Fix: Multiprocessing + Ditch the Library

Two changes made it practical:

**1. Parallelise by month.** Each year-month pair is independent — January 1985 doesn't depend on February 1985. I split the work into 1,524 month-chunks and distributed them across CPU cores using Python's `multiprocessing.Pool`:

```python
with open(args.output, "w") as fh, mp.Pool(processes=workers) as pool:
    for i, batch in enumerate(pool.imap(generate_ids_for_month, work_units), 1):
        fh.write("\n".join(batch))
        fh.write("\n")
```

**2. Remove the external library.** The `za-id-number` library instantiates a Python object for every single ID — parsing dates, computing gender, resolving citizenship. That's useful for analysis, but massive overkill for generation. Since we already construct valid dates and compute correct Luhn check digits, every generated ID is valid by construction.

For optional verification, I wrote a lightweight inline validator:

```python
def luhn_verify(id_str):
    total = 0
    for i, ch in enumerate(reversed(id_str)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0
```

No object instantiation. No date parsing. Just maths. **7x faster** than the library approach.

### The Results

| Metric | Before | After |
|--------|--------|-------|
| Cores used | 1 | All available |
| Validation | External library (~70K IDs/s) | Inline Luhn (~486K IDs/s) |
| Throughput | ~9 IDs/s with validation | ~2.3M IDs/s generation |
| Time for 1 year | Hours | ~3 seconds |
| Dependencies | `za-id-number` | None (stdlib only) |

On a 12-core machine, generating a full year of IDs (7.3 million numbers) takes about 3 seconds.

---

## The Bug That Made Everything Invalid

During development, I hit a critical bug. My initial Luhn implementation doubled the **wrong positions** — even indices instead of odd indices in the payload. The difference is subtle:

```python
# WRONG (left-to-right doubling)
if i % 2 == 0:
    d *= 2

# CORRECT (standard Luhn)
if i % 2 == 1:
    d *= 2
```

This produced IDs that looked valid at a glance — 13 digits, valid dates, proper structure — but failed every real-world validator. The check digit was consistently wrong.

The fix was one character: changing `== 0` to `== 1`. That's the kind of bug that can survive code review, pass unit tests that only check format, and only surface when you test against an external validator.

**Lesson: always validate against a ground truth source, not just your own implementation.**

---

## CLI Design: Making It Usable

The original script hardcoded everything — year range, output file, no way to generate just a few IDs without editing the code. I added `argparse` to make it a proper CLI tool:

```bash
# Generate 200 validated IDs
python gen.py --validate -n 200

# Estimate output size before committing to a full run
python gen.py --dry-run
# Range: 1900-2026 (1524 months)
# Estimated IDs: 927,720,000
# Estimated file size: 12.1 GB

# Custom range with 8 workers
python gen.py -s 1980 -e 2000 -w 8 -o output.txt
```

The `--dry-run` flag turned out to be essential. When your output file is 12 GB, you want to know that before you start.

Live progress reporting shows percentage, count, and throughput in real-time:

```
[ 41.7%] 5/12 months | 3,040,000 IDs | 1,989,598 IDs/s
```

---

## What Could You Do With This?

This tool generates test data. Some applications:

- **Software testing**: If you're building a system that accepts SA ID numbers, you need valid test data that covers edge cases — leap years, boundary dates, both citizenship values
- **Data validation**: Verify that your ID validation logic correctly accepts valid numbers and rejects invalid ones
- **Statistical analysis**: Study the distribution of check digits, gender sequences, or date patterns
- **Security research**: Understand the entropy and predictability of ID number schemes

---

## Technical Details

The full source is on GitHub: [wafrica-algo](https://github.com/s-b-repo/wafrica-algo)

**Stack:**
- Python 3.7+ (no external dependencies)
- `multiprocessing.Pool` for parallelism
- `calendar` module for date validation
- `argparse` for CLI

**Output format:** One ID per line, plain text. A full 1900-2026 run produces approximately 927 million IDs in a 12 GB file.

**Memory:** Work is chunked by month (~600K IDs per chunk, ~8 MB per worker). Even a machine with 4 GB of RAM can generate the full dataset.

---

## Key Takeaways

1. **The Luhn algorithm is everywhere** — credit cards, IMEI numbers, SA IDs. Understanding it unlocks a whole class of validation logic.

2. **Direction matters in Luhn** — doubling even vs. odd positions produces completely different check digits. One character in the code. Completely different output.

3. **Multiprocessing is free performance** — if your work can be split into independent chunks, `multiprocessing.Pool` turns a single-core crawl into a multicore sprint with minimal code changes.

4. **External libraries aren't always faster** — sometimes inlining the critical path and dropping the abstraction gives you a 7x speedup with zero dependencies.

5. **Always validate against ground truth** — your implementation might be self-consistent but wrong. Test against a real-world validator before you trust your output.

---

*Built with Python. Validated against real-world SA ID checkers. Zero dependencies.*
