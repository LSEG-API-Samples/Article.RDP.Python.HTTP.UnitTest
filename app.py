#|-----------------------------------------------------------------------------
#|            This source code is provided under the MIT license             --
#|  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
#|                See the project's LICENSE.md for details.                  --
#|           Copyright Refinitiv 2022.       All rights reserved.            --
#|-----------------------------------------------------------------------------

"""
Example Code Disclaimer:
ALL EXAMPLE CODE IS PROVIDED ON AN “AS IS” AND “AS AVAILABLE” BASIS FOR ILLUSTRATIVE PURPOSES ONLY. REFINITIV MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, AS TO THE OPERATION OF THE EXAMPLE CODE, OR THE INFORMATION, CONTENT, OR MATERIALS USED IN CONNECTION WITH THE EXAMPLE CODE. YOU EXPRESSLY AGREE THAT YOUR USE OF THE EXAMPLE CODE IS AT YOUR SOLE RISK.
"""

import sys
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from rdp_controller import rdp_http_controller

def convert_pandas(json_data):
    if not json_data:
        raise TypeError('Received invalid (None or Empty) JSON data')

    try:
        headers=json_data['headers'] 
        #Get column headers/titles using lambda
        titles=map(lambda header:header['title'], headers)
            
        dataArray=np.array(json_data['data'])
        df = pd.DataFrame(data=dataArray,columns=titles)

        return df
    except Exception as exp:
        print(f'Error converting JSON to Dataframe exception: {str(exp)}') 
        raise TypeError('Error converting JSON to Dataframe')


if __name__ == '__main__':
    username = os.getenv('RDP_USERNAME')
    password = os.getenv('RDP_PASSWORD')
    client_id = os.getenv('RDP_CLIENTID')

    rdp_controller = rdp_http_controller.RDPHTTPController()

    base_URL = os.getenv('RDP_BASE_URL')
    auth_endpoint = base_URL + os.getenv('RDP_AUTH_URL')
    esg_endpoint = base_URL + os.getenv('RDP_ESG_URL')
    search_endpoint = base_URL + os.getenv('RDP_SEARCH_EXPLORE_URL')

    access_token = None
    refresh_token = None
    expires_in = 0
    universe = 'LSEG.L'

    try:
        access_token, refresh_token, expires_in = rdp_controller.rdp_authentication(auth_endpoint, username, password, client_id)
        if not access_token:
            print('Cannot login to RDP, exiting application')
            sys.exit(1)
        
        esg_data = None
        esg_data = rdp_controller.rdp_request_esg(esg_endpoint, access_token, universe)
        if not esg_data:
            print(f'No ESG data for {universe}, exiting application')
        
        esg_df = convert_pandas(esg_data)
        esg_df = pd.DataFrame(esg_df,columns=['Instrument','Period End Date','ESG Score','ESG Combined Score','ESG Controversies Score'])
        print(esg_df.head())

        company_data = None
        search_payload = {
            'View': 'Entities',
            'Filter': f'RIC eq \'{universe}\'',
            'Select': 'IssuerCommonName,DocumentTitle,RCSExchangeCountryLeaf,IssueISIN,ExchangeName,ExchangeCode,SearchAllCategoryv3,RCSTRBC2012Leaf'
        }
        company_data = rdp_controller.rdp_request_search_explore(search_endpoint, access_token, search_payload)
        if not company_data:
            print(f'No Meta data for {universe}, exiting application')
        print(f'RIC: {universe} Metadata:')
        print('\tIssuerCommonName: {}'.format(company_data['Hits'][0]['IssuerCommonName']))
        print('\tRCSExchangeCountryLeaf: {}'.format(company_data['Hits'][0]['RCSExchangeCountryLeaf']))
        print('\tISIN: {}'.format(company_data['Hits'][0]['IssueISIN']))
        print('\tExchange Name: {}'.format(company_data['Hits'][0]['ExchangeName']))
        print('\tRCSTRBC2012Leaf: {}'.format(company_data['Hits'][0]['RCSTRBC2012Leaf']))
    except Exception as exp:
        print(f'Caught exception: {str(exp)}')

