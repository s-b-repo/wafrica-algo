from datetime import datetime, timedelta
from za_id_number import SouthAfricanIdentityNumber

def generate_dates_in_range(start_date, end_date):
    """
    Generate all valid dates in YYMMDD format within the specified date range.
    
    Parameters:
    start_date (str): Start date in 'YYYYMMDD' format.
    end_date (str): End date in 'YYYYMMDD' format.
    
    Returns:
    list: List of dates in 'YYMMDD' format.
    """
    date_list = []
    current_date = datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y%m%d")
    delta = timedelta(days=1)
    
    while current_date <= end_date:
        date_list.append(current_date.strftime("%y%m%d"))
        current_date += delta
    
    return date_list

def generate_and_save_valid_sa_id_numbers(start_date, end_date, gender, citizenship, output_file):
    """
    Generate all possible valid South African ID numbers within a date range, gender, and citizenship.
    Valid IDs are saved to a .txt file.

    Parameters:
    start_date (str): The start date in 'YYYYMMDD' format.
    end_date (str): The end date in 'YYYYMMDD' format.
    gender (str): 'female' or 'male'.
    citizenship (int): 0 for SA citizen, 1 for permanent resident.
    output_file (str): The file path to save the valid IDs.
    """
    valid_ids = []
    
    # Set SSSS range based on gender
    ssss_start = 0 if gender.lower() == 'female' else 5000
    ssss_end = 4999 if gender.lower() == 'female' else 9999
    
    # Generate all valid dates in the specified range
    dates = generate_dates_in_range(start_date, end_date)
    
    # Citizenship and A value (typically set to 8)
    c_value = str(citizenship)
    a_value = '8'
    
    with open(output_file, 'w') as f:
        # Iterate over each date and generate possible IDs
        for yymmdd in dates:
            for ssss in range(ssss_start, ssss_end + 1):
                ssss_str = str(ssss).zfill(4)
                
                # Form the first 10 digits of the ID
                id_base = f"{yymmdd}{ssss_str}{c_value}{a_value}"
                
                # Brute-force the last digit (Z)
                for z in range(10):
                    full_id = f"{id_base}{z}"
                    try:
                        # Validate ID using the za-id-number library
                        id_number = SouthAfricanIdentityNumber(full_id)
                        if id_number.valid:
                            # If valid, write the ID to the file
                            f.write(full_id + "\n")
                            valid_ids.append(full_id)
                    except ValueError:
                        # If ID is invalid, the library raises an exception
                        continue

    return valid_ids

# Example usage
start_date = "19920101"  # Start date in 'YYYYMMDD' format
end_date = "19921231"    # End date in 'YYYYMMDD' format
gender = "female"        # Gender: 'female' or 'male'
citizenship = 0          # Citizenship: 0 for SA citizen, 1 for permanent resident
output_file = "valid_sa_ids.txt"  # Output file to save valid IDs

# Generate and save valid South African ID numbers
valid_id_numbers = generate_and_save_valid_sa_id_numbers(start_date, end_date, gender, citizenship, output_file)

# Display the first 10 valid IDs for demonstration
print("First 10 valid ID numbers:", valid_id_numbers[:10])
print(f"Total number of valid IDs generated: {len(valid_id_numbers)}")
print(f"Valid IDs saved to: {output_file}")
