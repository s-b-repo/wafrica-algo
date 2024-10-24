#credit
###
https://pypi.org/project/za-id-number/
###
https://medium.com/@ryanneilparker/sa-id-fumble-how-south-africa-managed-to-incorrectly-apply-the-luhn-algorithm-352dd6f10738
# South African ID Number Generator and Validator

This project generates valid South African ID numbers based on certain criteria, and validates them using the [za-id-number](https://pypi.org/project/za-id-number/) Python library before saving the results to a file.

## Features

- Generates South African ID numbers from specified date ranges (default: 1900 to 2023).
- Ensures valid date combinations (handles leap years, month-day limits).
- Supports gender differentiation in ID numbers.
- Citizenship indicator (South African or Permanent Resident).
- Calculates the Luhn checksum to validate each ID number.
- Uses the `za-id-number` library to validate each ID number before saving.
- Saves only the successfully validated IDs to a text file.

## Requirements

- Python 3.x
- `za-id-number` library

### Install the required dependencies:

```bash
pip install za-id-number

## Contributing

We welcome contributions to improve this project! To contribute:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Usage

To generate valid South African ID numbers and save them to a file:

python

from id_generator import generate_all_valid_ids

# Example: Generate all valid IDs from 1900 to 2023 and save to 'valid_ids.txt'
generate_all_valid_ids(1900, 2023, file_name="valid_ids.txt")

Parameters:

    start_year (int): The starting year for generating IDs (default is 1900).
    end_year (int): The ending year for generating IDs (default is 2023).
    file_name (str): The file where the validated IDs will be saved (default is valid_ids.txt).

Example:


generate_all_valid_ids(1900, 2023, file_name="valid_sa_ids.txt")

This will generate and validate South African ID numbers from 1900 to 2023 and save them to the specified file.
How It Works

    ID Generation: The program generates all possible ID numbers for given years, months, days, and gender combinations. Each ID has a checksum calculated using the Luhn algorithm.
    Validation: After generating an ID number, it is validated using the za-id-number library.
    Saving: Only IDs that pass the validation are saved to the output file.

Notes

    The ID generation process is optimized with buffering to reduce frequent disk writes.
    The default buffer size is set to 100,000 IDs, but you can adjust this based on memory availability.

## License

This project is licensed under the GPL License - see the [LICENSE](LICENSE) file for details.

---

## Future Work

- Add command-line parameters to customize the date range and output file without modifying the script.
- Optimize the performance for larger date ranges.
- Add unit tests for the Luhn algorithm and ID generation.

---

Feel free to modify the wording, formatting, or any details to match your specific repository and goals. Let me know if you'd like any further adjustments!
