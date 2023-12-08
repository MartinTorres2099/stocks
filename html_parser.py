import os
import csv
import re
from bs4 import BeautifulSoup
from config import html_dir, csv_file  # Import variables from config.py

# Function to extract data from an HTML file
def extract_data_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        # Find the script element that contains the data
        script_tag = soup.find('script', text=lambda x: "txType" in (x or ''))

        if script_tag:
            # Extract the text content of the script tag
            script_content = script_tag.text

            # Use regular expressions to extract the desired data
            tx_type_match = re.search(r'"txType"\s*:\s*"([^"]+)"', script_content)
            pub_date_match = re.search(r'"pubDate"\s*:\s*"([^"]+)"', script_content)
            filing_date_match = re.search(r'"filingDate"\s*:\s*"([^"]+)"', script_content)
            tx_date_match = re.search(r'"txDate"\s*:\s*"([^"]+)"', script_content)
            reporting_gap_match = re.search(r'"reportingGap"\s*:\s*([\d.]+)', script_content)
            # reporting_gap_match = re.search(r'"reportingGap"\s*:\s*"([^"]+)"', script_content)
            value_match = re.search(r'"value"\s*:\s*"([\d.]+)"', script_content)
            # value_match = re.search(r'"value"\s*:\s*"([^"]+)"', script_content)
            first_name_match = re.search(r'"firstName"\s*:\s*"([^"]+)"', script_content)
            gender_match = re.search(r'"gender"\s*:\s*"([^"]+)"', script_content)
            last_name_match = re.search(r'"lastName"\s*:\s*"([^"]+)"', script_content)
            party_match = re.search(r'"party"\s*:\s*"([^"]+)"', script_content)
            ## labels_match = re.search(r'"labels"\s*:\s*"([^"]+)"', script_content)
            ## has_capital_gains_match = re.search(r'"hasCapitalGains"\s*:\s*"([^"]+)"', script_content)
            owner_match = re.search(r'"owner"\s*:\s*"([^"]+)"', script_content)
            chamber_match = re.search(r'"chamber"\s*:\s*"([^"]+)"', script_content)
            price_match = re.search(r'"price"\s*:\s*"([\d.]+)"', script_content)
            # price_match = re.search(r'"price"\s*:\s*"([^"]+)"', script_content)
            filing_url_match = re.search(r'"filingURL"\s*:\s*"([^"]+)"', script_content)
            comment_match = re.search(r'"comment"\s*:\s*"([^"]+)"', script_content)
            ## committees_match = re.search(r'"committees"\s*:\s*"([^"]+)"', script_content)
            issuer_name_match = re.search(r'"issuerName"\s*:\s*"([^"]+)"', script_content)
            issuer_ticker_match = re.search(r'"issuerTicker"\s*:\s*"([^"]+)"', script_content)

            # Extract data from the matches or provide default values
            tx_type = tx_type_match.group(1) if tx_type_match else ''
            pub_date = pub_date_match.group(1) if pub_date_match else ''
            filing_date = filing_date_match.group(1) if filing_date_match else ''
            tx_date = tx_date_match.group(1) if tx_date_match else ''
            reporting_gap = float(reporting_gap_match.group(1)) if reporting_gap_match else 0  # Parse as float
            # reporting_gap = reporting_gap_match.group(1) if reporting_gap_match else ''
            value =  float(value_match.group(1)) if value_match else ''  # Parse as float
            # value = value_match.group(1) if value_match else ''
            first_name = first_name_match.group(1) if first_name_match else ''
            gender = gender_match.group(1) if gender_match else ''
            last_name = last_name_match.group(1) if last_name_match else ''
            party = party_match.group(1) if party_match else ''
            ## labels = labels_match.group(1) if labels_match else ''
            ## has_capital_gains = has_capital_gains_match.group(1) if has_capital_gains_match else ''
            owner = owner_match.group(1) if owner_match else ''
            chamber = chamber_match.group(1) if chamber_match else ''
            price = float(price_match.group(1)) if price_match else ''  # Parse as float
            # price = price_match.group(1) if price_match else ''
            filing_url = filing_url_match.group(1) if filing_url_match else ''
            comment = comment_match.group(1) if comment_match else ''
            ## committees = committees_match.group(1) if committees_match else ''
            issuer_name = issuer_name_match.group(1) if issuer_name_match else ''
            issuer_ticker = issuer_ticker_match.group(1) if issuer_ticker_match else ''

            # Extract data from the HTML
            description = soup.find('meta', {'name': 'description'})['content']
            trade_value = soup.find('span', {'class': 'q-field trade-value'}).text.strip()
            # q_value = soup.find('span', {'class': 'q-value'}).text.strip()
            # trade_size = soup.find('span', {'class': 'q-field trade-size'}).text.strip()

            # Return extracted data as a dictionary
            return {
                "issuerName": issuer_name,
                "issuerTicker": issuer_ticker,
                "txType": tx_type,
                "tradeValue": trade_value,
                "reportingGap": reporting_gap,
                "Description": description,
                "pubDate": pub_date,
                "filingDate": filing_date,
                "txDate": tx_date,
                "value": value,
                # "qValue": q_value,
                # "tradeSize": trade_size,
                "gender": gender,
                "firstName": first_name,
                "lastName": last_name,
                "party": party,
                # "labels": labels,
                # "hasCapitalGains": has_capital_gains,
                "owner": owner,
                "chamber": chamber,
                "price": price,
                "filingURL": filing_url,
                "comment": comment,
                # "committees": committees,
            }
        else:
            # Handle cases where the script tag is not found by returning an empty dictionary
            return {}

# Function to write data to CSV file
def write_to_csv(data, csv_file):
    # Check if the CSV file already exists
    csv_exists = os.path.exists(csv_file)
    
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header only if the file is newly created
        if not csv_exists:
            writer.writeheader()
        
        # Write data to CSV
        writer.writerow(data)

# Iterate through HTML files in the directory
for filename in os.listdir(html_dir):
    if filename.endswith('.html'):
        html_file_path = os.path.join(html_dir, filename)
        data = extract_data_from_html(html_file_path)
        write_to_csv(data, csv_file)

print("Data extraction and CSV file creation completed.")
