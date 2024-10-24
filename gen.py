import os

# Function to check if a given year is a leap year
def is_leap_year(year):
    """Check if a given year is a leap year."""
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    return False

# Function to calculate the Luhn checksum digit (left-to-right for SA ID numbers)
def calculate_luhn_left_to_right(id_number):
    """Calculate Luhn checksum for SA ID numbers (left-to-right)."""
    digits = [int(d) for d in id_number]
    checksum = 0
    for i in range(len(digits)):
        if i % 2 == 0:  # Odd positions (0-based index, left-to-right)
            double = digits[i] * 2
            checksum += double if double < 10 else double - 9
        else:  # Even positions
            checksum += digits[i]
    return (10 - (checksum % 10)) % 10

# Function to generate all valid ID numbers and save them to a text file
def generate_all_valid_ids(start_year=1900, end_year=2023, file_name="valid_ids.txt"):
    """Generate all valid South African ID numbers and save to a file."""
    # Ensure output directory exists
    try:
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
    except Exception as e:
        print(f"Error creating directory: {e}")
        return

    # Buffer to reduce frequent disk writes
    buffer_size = 100000  # Adjust the size based on memory availability
    buffer = []

    try:
        with open(file_name, "w") as file:
            # Loop through all possible years, months, and days
            for year in range(start_year % 100, (end_year % 100) + 1):  # YY (00-99)
                full_year = start_year + year
                for month in range(1, 13):  # MM (01-12)
                    # Determine days in the month
                    if month == 2:  # February (leap year check)
                        days_in_month = 29 if is_leap_year(full_year) else 28
                    elif month in [4, 6, 9, 11]:  # April, June, September, November
                        days_in_month = 30
                    else:
                        days_in_month = 31

                    for day in range(1, days_in_month + 1):  # DD (01-31)
                        # Skip invalid day combinations
                        if not (1 <= day <= days_in_month):
                            continue

                        # Format the year, month, and day as strings
                        yy = f"{year:02d}"
                        mm = f"{month:02d}"
                        dd = f"{day:02d}"

                        # Generate IDs for females (0000-4999) and males (5000-9999)
                        for gender in range(0, 10000):  # SSSS (0000-9999)
                            ssss = f"{gender:04d}"

                            # Citizenship (0 for South African, 1 for Permanent Resident)
                            for citizenship in range(0, 2):  # C (0 or 1)
                                id_number_without_checksum = f"{yy}{mm}{dd}{ssss}{citizenship}"

                                # Calculate the Luhn checksum using left-to-right method
                                checksum = calculate_luhn_left_to_right(id_number_without_checksum)

                                # Form the full valid ID
                                valid_id = f"{id_number_without_checksum}{checksum}"

                                # Add valid ID to buffer
                                buffer.append(valid_id)

                                # Write to file when buffer reaches threshold
                                if len(buffer) >= buffer_size:
                                    file.write("\n".join(buffer) + "\n")
                                    buffer.clear()

            # Write any remaining IDs in the buffer
            if buffer:
                file.write("\n".join(buffer) + "\n")

        print(f"ID generation complete. Saved to {file_name}")
    except Exception as e:
        print(f"Error writing to file: {e}")

# Example usage to generate all IDs from 1900 to 2023
generate_all_valid_ids(1900, 2023)
