from dotenv import load_dotenv
import os

load_dotenv()

with open(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/worms_from_mac.csv', 'r') as original:
    with open(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/cleaned_mac_worms.csv', 'w') as output:
        for row in original:
            new_row = row[:-20]
            output.write(new_row) 
            output.write('\n')