from datetime import datetime, timedelta

def calculate_luhn_sa(id_number):
    """
    Calculate the Luhn checksum for a South African ID number.
    The Luhn algorithm is applied in reverse, where every second digit from the right is doubled.
    """
    total = 0
    reverse_digits = id_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # Apply doubling for every second digit from the right
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

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

def generate_valid_sa_id_numbers(start_date, end_date, gender, citizenship):
    """
    Generate all possible valid South African ID numbers within a date range, gender, and citizenship.
    
    Parameters:
    start_date (str): The start date in 'YYYYMMDD' format.
    end_date (str): The end date in 'YYYYMMDD' format.
    gender (str): 'female' or 'male'.
    citizenship (int): 0 for SA citizen, 1 for permanent resident.
    
    Returns:
    list: List of valid South African ID numbers.
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
    
    # Iterate over each date and generate possible IDs
    for yymmdd in dates:
        for ssss in range(ssss_start, ssss_end + 1):
            ssss_str = str(ssss).zfill(4)
            
            # Form the first 10 digits of the ID
            id_base = f"{yymmdd}{ssss_str}{c_value}{a_value}"
            
            # Brute-force the last digit (Z)
            for z in range(10):
                full_id = f"{id_base}{z}"
                if calculate_luhn_sa(full_id):
                    valid_ids.append(full_id)
    
    return valid_ids

# Example usage
start_date = "19920101"  # Start date in 'YYYYMMDD' format
end_date = "19921231"    # End date in 'YYYYMMDD' format
gender = "female"        # Gender: 'female' or 'male'
citizenship = 0          # Citizenship: 0 for SA citizen, 1 for permanent resident

# Generate valid South African ID numbers
valid_id_numbers = generate_valid_sa_id_numbers(start_date, end_date, gender, citizenship)

# Display the first 10 valid IDs for demonstration
print("First 10 valid ID numbers:", valid_id_numbers[:10])
print("Total number of valid IDs generated:", len(valid_id_numbers))

