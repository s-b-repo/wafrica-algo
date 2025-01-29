import os
from za_id_number import SouthAfricanIdentityNumber
from za_id_number.exceptions import InvalidIdentityNumberException

def is_leap_year(year):
    """Check if a given year is a leap year."""
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    return False

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

def generate_all_valid_ids(start_year=1900, end_year=2023, file_name="valid_ids.txt"):
    """Generate all valid South African ID numbers and save to a file."""
    try:
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
    except Exception as e:
        print(f"Error creating directory: {e}")
        return

    buffer_size = 100000  # Adjust based on memory availability
    buffer = []

    try:
        with open(file_name, "w") as file:
            for full_year in range(start_year, end_year + 1):
                yy = f"{full_year % 100:02d}"
                for month in range(1, 13):
                    if month == 2:
                        days_in_month = 29 if is_leap_year(full_year) else 28
                    elif month in [4, 6, 9, 11]:
                        days_in_month = 30
                    else:
                        days_in_month = 31

                    for day in range(1, days_in_month + 1):
                        mm = f"{month:02d}"
                        dd = f"{day:02d}"

                        for gender in range(0, 10000):
                            ssss = f"{gender:04d}"

                            for citizenship in range(0, 2):
                                # Construct ID without checksum (12 digits: YYMMDDSSSSC8)
                                id_number_without_checksum = f"{yy}{mm}{dd}{ssss}{citizenship}8"
                                checksum = calculate_luhn_left_to_right(id_number_without_checksum)
                                valid_id = f"{id_number_without_checksum}{checksum}"

                                try:
                                    sa_id = SouthAfricanIdentityNumber(valid_id)
                                    if sa_id.is_valid():
                                        buffer.append(valid_id)
                                except InvalidIdentityNumberException:
                                    continue

                                if len(buffer) >= buffer_size:
                                    file.write("\n".join(buffer) + "\n")
                                    buffer.clear()

            if buffer:
                file.write("\n".join(buffer) + "\n")

        print(f"ID generation complete. Successfully validated IDs saved to {file_name}")
    except Exception as e:
        print(f"Error writing to file: {e}")

# Example usage to generate all IDs from 1900 to 2023
generate_all_valid_ids(1900, 2023)
