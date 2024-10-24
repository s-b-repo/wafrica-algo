#credit
###
https://pypi.org/project/za-id-number/
###
https://medium.com/@ryanneilparker/sa-id-fumble-how-south-africa-managed-to-incorrectly-apply-the-luhn-algorithm-352dd6f10738
# South African ID Number Generator

This project generates all possible valid South African ID numbers using the **left-to-right Luhn algorithm**, as applied in South Africa. It systematically produces every valid combination of birthdate, gender, and citizenship, ensuring that the generated ID numbers are valid according to South African standards.

## Features
- Generates **all possible valid ID numbers** within a specified date range (e.g., 1900-2023).
- Applies the **left-to-right Luhn algorithm** to compute the checksum and ensure the validity of each ID.
- Skips invalid dates (e.g., February 30, April 31).
- Saves all valid ID numbers to a text file (`valid_ids.txt`).
- Optimized for large-scale generation, though the file size may be very large due to the number of possible combinations.

## ID Number Structure

A South African ID number is a **13-digit number** with the following format:

```
YYMMDDSSSSCAZ
```

- **YYMMDD**: The first 6 digits represent the date of birth.
    - `YY`: The last two digits of the year.
    - `MM`: Month of birth (01 to 12).
    - `DD`: Day of birth (01 to 31, with invalid dates skipped).
- **SSSS**: A 4-digit sequence that indicates gender.
    - `0000-4999`: Female.
    - `5000-9999`: Male.
- **C**: Citizenship status.
    - `0`: South African citizen.
    - `1`: Permanent resident.
- **Z**: The checksum digit, calculated using the **left-to-right Luhn algorithm**.

## How the Luhn Algorithm is Applied

In South Africa, the Luhn algorithm is applied from **left to right**, unlike the standard implementation which processes digits from right to left. The checksum digit is used to verify the validity of the ID number.

## Prerequisites

- Python 3.x
- Basic understanding of how the Luhn algorithm works (left-to-right variant for South African IDs).

## How to Use

### 1. Clone the Repository

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/your-username/sa-id-generator.git
cd sa-id-generator
```

### 2. Run the Script

You can generate all valid South African ID numbers within a specified date range and save them to a file by running the following script:

```bash
python generate_valid_ids.py
```

By default, it generates IDs from **1900 to 2023** and saves them to `valid_ids.txt`. You can customize the range of years by modifying the function parameters.

### 3. Customize the Date Range

To generate IDs for a specific date range, you can modify the `generate_all_valid_ids()` function call:

```python
generate_all_valid_ids(start_year=1950, end_year=2020, file_name="output_ids.txt")
```

This will create IDs from 1950 to 2020 and save them to `output_ids.txt`.

### 4. Check for Output

The generated ID numbers will be saved in the file specified (default: `valid_ids.txt`). Each line in the file represents one valid ID number.

### Example Output:

```
9002300000083
9002305000087
8201136721086
...
```

## Code Explanation

### `calculate_luhn_left_to_right(id_number)`
This function calculates the Luhn checksum by processing the digits of the ID from **left to right**. The odd-indexed digits (counting from the left) are doubled, and if the result is a two-digit number, it subtracts 9. The sum of the digits is used to compute the checksum.

### `generate_all_valid_ids(start_year, end_year, file_name)`
This function systematically generates all valid ID numbers:
- Iterates over all possible **birthdates** (years, months, and days) within the given range.
- Generates all possible **gender** and **citizenship** values.
- Computes the checksum using the Luhn algorithm and combines it to form the final ID.
- Writes the valid IDs to a text file.

## Performance Considerations

- **File Size**: This script generates **billions of IDs**, depending on the date range, and may produce extremely large output files. Ensure you have sufficient disk space before running it.
- **Memory**: The script efficiently writes the IDs to a file as they are generated, preventing memory overflow issues during execution.

### Reducing Output Size

To reduce the output file size, you can:
1. Narrow the range of birth years (e.g., 1980 to 2000 instead of 1900 to 2023).
2. Filter based on gender or citizenship if specific conditions are needed.

## Contributing

We welcome contributions to improve this project! To contribute:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the GPL License - see the [LICENSE](LICENSE) file for details.

---

## Future Work

- Add command-line parameters to customize the date range and output file without modifying the script.
- Optimize the performance for larger date ranges.
- Add unit tests for the Luhn algorithm and ID generation.

---

Feel free to modify the wording, formatting, or any details to match your specific repository and goals. Let me know if you'd like any further adjustments!
