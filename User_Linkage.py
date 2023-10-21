import pandas as pd
import random
import string
import numpy as np


def generate_random_data(num_records, num_ips_per_record):
  data = {
    'first_name': [random.choice(['Alice', 'Bob', 'Charlie', 'David', 'Eva']) for _ in range(num_records)],
    'last_name': [random.choice(['Smith', 'Johnson', 'Williams', 'Jones', 'Brown']) for _ in range(num_records)],
    'preferred_contact': [f'{random.choice(string.ascii_lowercase)}_{random.choice(string.ascii_lowercase)}_{random.choice(string.digits)}@example.com' for _ in range(num_records)],
    'last_four_digits': [''.join(random.choices(string.digits, k=4)) for _ in range(num_records)],
    'billing_zip_code': [''.join(random.choices(string.digits, k=5)) for _ in range(num_records)],
    'non_mfa_ip_addresses': [
      [
        f'{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
        for _ in range(num_ips_per_record)
      ]
      for _ in range(num_records)
    ]
  }
  return pd.DataFrame(data)


df_spotify = generate_random_data(100,5)
df_youtube = generate_random_data(100,5)

spotify_records_to_include = random.sample(range(len(df_spotify)), 78)
for index in spotify_records_to_include:
  df_youtube.loc[len(df_youtube)] = df_spotify.loc[index]

print("df_youtube:")
print(df_youtube)
print("\ndf_spotify:")
print(df_spotify)


# df_youtube: first_name, last_name, preferred_contact, last_four_digits,
# billing_zip_code, non_mfa_ip_addresses

# df_spotify: first_name, last_name, preferred_contact, last_four_digits,
# billing_zip_code, non_mfa_ip_addresses

# Return overlapping subscribers to both youtube and spotify: Overlap is:
# match on preferred contact
# match on first and last name, last 4 digits of the payment instrument and
# the billing zip code
# match on first and last name, billing zip code, and the first 3 octets of
# any non-mfa ip addresses

# Result: Only the records in the youtube dataframe that satisfy any match condition


def link_records(df_youtube, df_spotify):
  matched_emails = np.argwhere(np.isin(df_spotify.preferred_contact, df_youtube.preferred_contact)).ravel()
  df_spotify.iloc[matched_emails]
  df_youtube['preferred_contact']
    
  df_youtube['owner'] = (df_youtube['first_name'] + ' ' + df_youtube['last_name']).str.lower()
  df_spotify['owner'] = (df_spotify['first_name'] + ' ' + df_spotify['last_name']).str.lower()
  
  matched_name = np.argwhere(np.isin(df_spotify.owner, df_youtube.owner))
  
  matched_zip = np.argwhere(np.isin(df_spotify.billing_zip_code, df_youtube.billing_zip_code))
  
  matched_name_and_zip = np.intersect1d(matched_name, matched_zip)
  matched_name_and_zip
    
  matched_last_four = np.argwhere(np.isin(df_spotify.last_four_digits, df_youtube.last_four_digits))
  matched_last_four
  
  matched_name_and_zip_and_last_four = np.intersect1d(matched_last_four, matched_name_and_zip)
  matched_name_and_zip_and_last_four
  

  df_spotify['first_three_octets_ip'] = df_spotify['non_mfa_ip_addresses'].map(lambda x:[''.join(i.split('.')[:-1]) for i in x])
  df_youtube['first_three_octets_ip'] = df_youtube['non_mfa_ip_addresses'].map(lambda x:[''.join(i.split('.')[:-1]) for i in x])
  fuzzy_matched_ip = np.argwhere(np.any(np.isin([i for i in df_spotify.first_three_octets_ip], [j for j in df_youtube.first_three_octets_ip]), axis = 1))
  
  matched_name_and_zip_and_ip = np.intersect1d(fuzzy_matched_ip, matched_name_and_zip)
  all_matches = np.union1d(np.union1d(matched_emails, matched_name_and_zip_and_last_four), matched_name_and_zip_and_ip)
  
  return df_youtube.iloc[all_matches]

link_records(df_youtube, df_spotify)
