
from typing import List, Tuple, Dict
import requests
from dotenv import load_dotenv; load_dotenv()
import os
import json
from pathlib import Path
import logging
import pandas as pd

GFW_API_KEY = os.environ.get('GFW_API_KEY')

PATH_DATA = Path(os.environ.get('PATH_DATA'))


filename = PATH_DATA.parent.joinpath('logs', 'logs.logs')
filename.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, 
                    filename=filename, 
                    filemode='w', 
                    format=('%(asctime)s - %(levelname)s - %(message)s'))


def parse_vessels(response: List
                    )-> Tuple[pd.DataFrame, pd.DataFrame]:
    
    vessels = []
    owners = []

    for result in response:
        entries = result.get('entries')
        for entry in entries:
            if entry.get('registryInfoTotalRecords') != 0:
                ships = entry.get('registryInfo')
            else:
                ships = entry.get('selfReportedInfo')
            vessels.append(ships[0])
            coms = entry.get('registryOwners')
            if len(coms) > 0:
                for com in coms:
                    owners.append(com)
            
    vessels = pd.DataFrame(vessels)
    owners = pd.DataFrame(owners)

    return vessels, owners


def get_vessels(query: List,
                filename: str,
                limit: int = 5,
                field: str = 'mmsi'
                )-> Tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Search for vessels based on MMSI or IMO
    returns a list with information vessel, gear and,
    if available, owners. 
    
    Parameters:
    ----------
    query: list of MMSI or IMO numbers
    limit: the number of result for each query, default is 5
    field: mmsi or imo
    filename: filename for json output
    
    Returns:
    --------
    dataframe of vessels and dataframe of owners (so a tuple)

    Example:
    --------
    vessels, owners = gfw.get_vessels(query[123456, 2121432], filename='vessels')
    '''

    ENDPOINT = 'https://gateway.api.globalfishingwatch.org/v3/vessels/search?'

    headers = {'Authorization': f"Bearer {GFW_API_KEY}",
               'Content-Type': 'application/json'}

    results = []

    if field == 'mmsi':
        field = 'ssvid'
    elif field == 'imo':
        field = field
    else: 
        raise ValueError(f'Field must be "mmsi" or "imo" and not {field}')

    for q in query:
        url = f'where={field}="{q}"&datasets[0]=public-global-vessel-identity:latest&includes[0]=OWNERSHIP&includes[1]=AUTHORIZATIONS&limit={limit}'
        r = requests.get(ENDPOINT + url, headers=headers)

        if r.status_code == 200:
            result = r.json()
            result.update({'query': q})
            results.append(result)
            filepath = PATH_DATA.joinpath('data', f'{filename}.json')
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'a') as file:
                file.write(f'{result}\n')

        elif r.status_code != 200:                
                logging.error(f'Something went wrong with query: {q} --> status code: {r.status_code} - reason: {r.reason}\nplease check')

    vessels, owners = parse_vessels(results)

    return vessels, owners


def get_events(vessel_id: str,
               event_type: str,
               filename: str,
               start_date: str,
               end_date: str
               )-> pd.DataFrame:
    '''
    Searches for encounters, fishing, loitering, port visits
    and ais gap events by global fishing watch vessel id (so not the 
    mmsi or imo; use get_vessels module to get the vessel ids)
    
    Parameters:
    -----------
    vessel_id: vessel id from global fishing watch
    event_type: "encounter", "fishing", "loitering", "port_visits", "ais"
    filename: filename for json output
    start_date: format is 'yyyy-mm-dd', earliest date is 2012-01-01
    end_date: format is 'yyyy-mm-dd'
    
    Returns:
    --------
    A dataframe of events and a json file in data folder

    Example:
    ----------
    response = gfw.get_events('509dd770de5aa17235d569f255f24fcd', 'loitering', 'loitering', '2012-01-01', '2024-01-01')
    '''

    ENDPOINT = 'https://gateway.api.globalfishingwatch.org/v3/events?'

    headers = {'Authorization': f"Bearer {GFW_API_KEY}",
               'Content-Type': 'application/json'}

    if event_type == 'encounter':
        dataset = 'public-global-encounters-events:latest'
    elif event_type == 'fishing': 
        dataset = 'public-global-fishing-events:latest'
    elif event_type == 'loitering':
        dataset = 'public-global-loitering-events:latest'
    elif event_type == 'port_visits':
        dataset = 'public-global-port-visits-c2-events:latest'
    elif event_type == 'ais':
        dataset = 'public-global-gaps-events:latest&gap-intentional-disabling=True'
    else:
        raise ValueError(f'Event type must be "encounter", "fishing", "loitering", "port_visits" or "ais" not {event_type}')

    url = f'vessels[0]={vessel_id}&datasets[0]={dataset}&start-date={start_date}&end-date={end_date}&limit=99999&offset=0'

    r = requests.get(ENDPOINT + url, headers=headers)    

    if r.status_code == 200:
        result = r.json()
        result.update({'query': vessel_id})
        filepath = PATH_DATA.joinpath('data', f'{filename}.json')
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'a') as file:
            file.write(f'{result}\n')

        df = pd.json_normalize(result.get('entries'))
    
        return df

    elif r.status_code != 200:                
            logging.error(f'Something went wrong with query: {vessel_id} --> status code: {r.status_code} - reason: {r.reason}\nplease check')

    return None
    

def get_eez_list():
    ENDPOINT = 'https://gateway.api.globalfishingwatch.org/v3/datasets/public-eez-areas/context-layers'

    headers = {'Authorization': f"Bearer {GFW_API_KEY}",
               'Content-Type': 'application/json'}
    
    r = requests.get(ENDPOINT, headers=headers)
    result = r.json()
    
    return result 


def get_events_by_geometry(start_date: str,
                            end_date: str,
                            event_type: str,
                            filename: str,
                            flag: List = None,
                            geometry: Dict  = None,
                            region: Dict = None
                            )-> pd.DataFrame:

    ENDPOINT = 'https://gateway.api.globalfishingwatch.org/v3/events?'

    headers = {'Authorization': f"Bearer {GFW_API_KEY}",
               'Content-Type': 'application/json'}

    
    if event_type == 'encounter':
        dataset = 'public-global-encounters-events:latest'
    elif event_type == 'fishing': 
        dataset = 'public-global-fishing-events:latest'
    elif event_type == 'loitering':
        dataset = 'public-global-loitering-events:latest'
    elif event_type == 'port_visits':
        dataset = 'public-global-port-visits-c2-events:latest'
    elif event_type == 'ais':
        dataset = 'public-global-gaps-events:latest&gap-intentional-disabling=True'
    else:
        raise ValueError(f'Event type must be "encounter", "fishing", "loitering", "port_visits" or "ais" not {event_type}')

    url = f'limit=99999&offset=0'

    data = {"datasets": [ f"{dataset}" ],
            "startDate": f"{start_date}",
            "endDate": f"{end_date}",
            "vesselTypes": [ 'BUNKER','CARGO','DISCREPANCY','CARRIER','FISHING','GEAR','OTHER','PASSENGER','SEISMIC_VESSEL','SUPPORT' ]
            }
    
    if flag is not None:
        flags = ','.join(flag)
        data.update({'flags': [ f"{flags}" ]})
    
    if region is not None:
        data.update({'region': {'id': region,
                                'dataset': 'public-eez-areas'}})
    elif geometry is not None:
        data.update({'geometry': geometry})
    
    r = requests.post(ENDPOINT + url, headers=headers, data=json.dumps(data))

    if r.status_code == 200 or r.status_code==201:
        result = r.json()
        filepath = PATH_DATA.joinpath('data', f'{filename}.json')
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'a') as file:
            file.write(f'{result}\n')

        df = pd.json_normalize(result.get('entries'))
    
        return df

    elif r.status_code != 200: 
            print(r.text)               
            logging.error(f'Something went wrong --> status code: {r.status_code} - reason: {r.reason}\nplease check')

    return None
    