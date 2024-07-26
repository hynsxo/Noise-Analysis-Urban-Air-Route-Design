import urllib.request
import json
import pandas as pd
from datetime import datetime, timedelta
import schedule
import time
from tabulate import tabulate

def fetch_and_update_data():
    per_page = 1000
    total_records = 36384

    all_data = pd.DataFrame()

    for page in range(1, (total_records // per_page) + 2):
        url = f'https://api.odcloud.kr/api/getNoiseMeasureRT/v1/noiseMeasureRT?page={page}&perPage={per_page}&serviceKey=%2F6HAk2j2exeF7cOQSGBfBA8oCy5Op%2BZOAEVumc6swZBH36z92Mi81NiQJUqJ0ZySb5wehJRMNUTbL%2BIaVMCsZA%3D%3D'

        try:
            response = urllib.request.urlopen(url)
            json_str = response.read().decode('utf-8')

            json_object = json.loads(json_str)

            data = pd.json_normalize(json_object['data'])

            data = data[['ARP_SE', 'NMS_NM', 'NMT_DT', 'NMT_LVL', 'NMT_NO']]

            data['NMT_DT'] = pd.to_datetime(data['NMT_DT'], format='%Y%m%d%H%M%S')

            all_data = pd.concat([all_data, data], ignore_index=True)

        except urllib.error.HTTPError as e:
            print(f"HTTPError: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            print(f"URLError: {e.reason}")
        except ValueError as e:
            print(f"ValueError: {e}")
        except Exception as e:
            print(f"General Exception: {e}")
            break

    def load_previous_data(file_path):
        try:
            previous_data = pd.read_csv(file_path, encoding='utf-8-sig')
            previous_data['NMT_DT'] = pd.to_datetime(previous_data['NMT_DT'], format='%Y.%m.%d.%H:%M:%S')
        except FileNotFoundError:
            previous_data = pd.DataFrame(columns=['ARP_SE', 'NMS_NM', 'NMT_DT', 'NMT_LVL', 'NMT_NO'])
        return previous_data

    previous_data = load_previous_data('output.csv')
    previous_gmp_data = load_previous_data('GMP_output.csv')
    previous_pus_data = load_previous_data('PUS_output.csv')
    previous_cju_data = load_previous_data('CJU_output.csv')

    combined_data = pd.concat([previous_data, all_data]).drop_duplicates(subset=['ARP_SE', 'NMS_NM', 'NMT_DT']).reset_index(drop=True)

    gmp_data = combined_data[combined_data['ARP_SE'] == 'GMP']
    pus_data = combined_data[combined_data['ARP_SE'] == 'PUS']
    cju_data = combined_data[combined_data['ARP_SE'] == 'CJU']

    # Convert specific PUS data from UTC to KST
    specific_pus_data = pus_data[pus_data['NMS_NM'].isin(['불암동', '유도등', '불암주민센터', '식만', '월포', '신덕', '구마을'])]
    specific_pus_data.loc[:, 'NMT_DT'] = specific_pus_data['NMT_DT'].apply(lambda x: (x + timedelta(hours=9)).strftime('%Y.%m.%d.%H:%M:%S'))
    other_pus_data = pus_data[~pus_data['NMS_NM'].isin(['불암동', '유도등', '불암주민센터', '식만', '월포', '신덕', '구마을'])]
    other_pus_data.loc[:, 'NMT_DT'] = other_pus_data['NMT_DT'].apply(lambda x: x.strftime('%Y.%m.%d.%H:%M:%S'))

    updated_pus_data = pd.concat([specific_pus_data, other_pus_data]).sort_values(by='NMT_DT').reset_index(drop=True)

    previous_gmp_data = pd.concat([previous_gmp_data, gmp_data]).drop_duplicates(subset=['ARP_SE', 'NMS_NM', 'NMT_DT']).reset_index(drop=True)
    previous_pus_data = pd.concat([previous_pus_data, updated_pus_data]).drop_duplicates(subset=['ARP_SE', 'NMS_NM', 'NMT_DT']).reset_index(drop=True)
    previous_cju_data = pd.concat([previous_cju_data, cju_data]).drop_duplicates(subset=['ARP_SE', 'NMS_NM', 'NMT_DT']).reset_index(drop=True)

    combined_data['NMT_DT'] = combined_data['NMT_DT'].apply(lambda x: x.strftime('%Y.%m.%d.%H:%M:%S'))
    combined_data.to_csv('output.csv', index=False, encoding='utf-8-sig')
    previous_gmp_data['NMT_DT'] = previous_gmp_data['NMT_DT'].apply(lambda x: x.strftime('%Y.%m.%d.%H:%M:%S'))
    previous_gmp_data.to_csv('GMP_output.csv', index=False, encoding='utf-8-sig')
    previous_pus_data['NMT_DT'] = previous_pus_data['NMT_DT'].apply(lambda x: x.strftime('%Y.%m.%d.%H:%M:%S'))
    previous_pus_data.to_csv('PUS_output.csv', index=False, encoding='utf-8-sig')
    previous_cju_data['NMT_DT'] = previous_cju_data['NMT_DT'].apply(lambda x: x.strftime('%Y.%m.%d.%H:%M:%S'))
    previous_cju_data.to_csv('CJU_output.csv', index=False, encoding='utf-8-sig')

    print("Combined Data:")
    print(tabulate(combined_data, headers='keys', tablefmt='pipe', showindex=False))

    print("\nGMP Data:")
    print(tabulate(previous_gmp_data, headers='keys', tablefmt='pipe', showindex=False))

    print("\nPUS Data:")
    print(tabulate(previous_pus_data, headers='keys', tablefmt='pipe', showindex=False))

    print("\nCJU Data:")
    print(tabulate(previous_cju_data, headers='keys', tablefmt='pipe', showindex=False))

schedule.every(15).seconds.do(fetch_and_update_data)

while True:
    schedule.run_pending()
    time.sleep(1)