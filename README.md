# South African ID Number Generator

Generates valid South African ID numbers based on date ranges, validated using the [Luhn algorithm as applied by Home Affairs](https://medium.com/@ryanneilparker/sa-id-fumble-how-south-africa-managed-to-incorrectly-apply-the-luhn-algorithm-352dd6f10738). Optionally cross-checks results with the [za-id-number](https://pypi.org/project/za-id-number/) library.

## Features

- Generates SA ID numbers for configurable date ranges (default: 1900 to current year)
- Multiprocessing for fast parallel generation across CPU cores
- Live progress reporting (percentage, count, throughput)
- Handles leap years and month-day limits correctly
- Covers all gender sequences (0000-9999) and citizenship values (0-1)
- Optional library-based validation via `--validate`
- Dry-run mode to estimate output size before generating

## Requirements

- Python 3.7+
- `za-id-number` (only required when using `--validate`)

```bash
pip install za-id-number
```

## Usage

```bash
# Generate all IDs from 1900 to current year (default)
python gen.py

# Custom range with output file
python gen.py -s 1980 -e 2000 -o sa_ids_1980_2000.txt

# Use 8 workers
python gen.py -w 8

# Estimate output size without generating
python gen.py --dry-run

# Cross-check with za-id-number library (much slower)
python gen.py --validate
```

### CLI Options

| Flag | Description | Default |
|------|-------------|---------|
| `-s`, `--start-year` | Start year | 1900 |
| `-e`, `--end-year` | End year | Current year |
| `-o`, `--output` | Output file path | `valid_ids.txt` |
| `-w`, `--workers` | Parallel worker count | CPU count |
| `--validate` | Cross-check each ID with za-id-number | Off |
| `--dry-run` | Estimate output size only | Off |

## How It Works

SA ID format: `YYMMDDSSSSCAZ`

| Segment | Meaning |
|---------|---------|
| `YY` | Year of birth |
| `MM` | Month of birth |
| `DD` | Day of birth |
| `SSSS` | Sequence/gender (0000-4999 female, 5000-9999 male) |
| `C` | Citizenship (0 = SA citizen, 1 = permanent resident) |
| `A` | Former race digit (now fixed at 8) |
| `Z` | Luhn check digit |

The generator constructs all valid date/sequence/citizenship combinations, computes the Luhn check digit for each, and writes the results to file. The Luhn algorithm uses the left-to-right variant that SA Home Affairs implemented.

## Notes

- Full generation (1900-2026) produces ~900 million IDs (~12 GB).
- The `--validate` flag is useful for verifying the Luhn implementation matches the library but is orders of magnitude slower.
- Memory usage scales per-month (~8 MB per worker).

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## License

GPL - see [LICENSE](LICENSE).
