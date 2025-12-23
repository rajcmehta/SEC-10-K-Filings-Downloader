import os
import json
import pandas as pd

def initialize_risk_df(current_path):
    folder_path = current_path.parent / "edgar-crawler\datasets\EXTRACTED_FILINGS\\10-K"

    with open('cik_to_ticker.json', 'r', encoding='utf-8') as f:
        cik_to_ticker = json.load(f)

    data_list = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            cik = json_data.get('cik', None)
            record = {
                'cik': cik,
                'company': json_data.get('company', None),
                'ticker': cik_to_ticker.get(cik, None),
                'filing_date': json_data.get('filing_date', None),
                'item_1A': json_data.get('item_1A', None),
            }
            data_list.append(record)

    df = pd.DataFrame(data_list)
    return df