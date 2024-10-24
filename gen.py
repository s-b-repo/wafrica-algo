import itertools

# Function to calculate the Luhn checksum digit (left-to-right for SA ID numbers)
def calculate_luhn_left_to_right(id_number):
    digits = [int(d) for d in id_number]
    checksum = 0
    for i in range(len(digits)):
        if i % 2 == 0:  # Odd positions (from left, 0-based index)
            double = digits[i] * 2
            checksum += double if double < 10 else double - 9
        else:  # Even positions
            checksum += digits[i]
    return (10 - (checksum % 10)) % 10

# Function to generate all valid ID numbers and save them to a text file
def generate_all_valid_ids(start_year=1900, end_year=2023, file_name="valid_ids.txt"):
    with open(file_name, "w") as file:
        # Loop through all possible years, months, and days
        for year in range(start_year % 100, (end_year % 100) + 1):  # YY (00-99)
            for month in range(1, 13):  # MM (01-12)
                for day in range(1, 32):  # DD (01-31)
                    if month == 2 and day > 28:  # Skip invalid February dates
                        continue
                    if month in [4, 6, 9, 11] and day > 30:  # Skip invalid days in 30-day months
                        continue
                    yy = f"{year:02d}"
                    mm = f"{month:02d}"
                    dd = f"{day:02d}"

                    # Loop through all possible gender (SSSS) and citizenship (C) values
                    for gender in range(0, 10000):  # SSSS (0000-9999)
                        ssss = f"{gender:04d}"

                        for citizenship in range(0, 2):  # C (0 or 1)
                            id_number_without_checksum = f"{yy}{mm}{dd}{ssss}{citizenship}"

                            # Calculate the Luhn checksum using left-to-right method
                            checksum = calculate_luhn_left_to_right(id_number_without_checksum)

                            # Form the full valid ID
                            valid_id = f"{id_number_without_checksum}{checksum}"

                            # Write the valid ID to the file
                            file.write(valid_id + "\n")

    print(f"ID generation complete. Saved to {file_name}")

# Example usage to generate all IDs from 1900 to 2023
generate_all_valid_ids(1900, 2023)
