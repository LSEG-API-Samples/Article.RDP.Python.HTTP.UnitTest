import requests
import json

class RDPHTTPController():

    # Constructor Method
    def __init__(self):
        self.scope = 'trapi'
        self.client_secret = ''
        pass
    
    # Send HTTP Post request to get Access Token (Password Grant and Refresh Grant) from RDP Auth Service
    def rdp_authentication(self, auth_url, username, password, client_id, old_refresh_token = None):
        """
        Send Authentication to RDP Auth service
        """

        if not auth_url or not username or not password or not client_id:
            raise TypeError('Received invalid (None or Empty) arguments')

        access_token = None
        refresh_token = None
        expires_in = 0
        if old_refresh_token is None: # For the Password Grant scenario
            payload=f'username={username}&password={password}&grant_type=password&scope={self.scope}&takeExclusiveSignOnControl=true&client_id={client_id}'
        else:  # For the Refresh Token scenario
            payload=f'username={username}&refresh_token={old_refresh_token}&grant_type=refresh_token&client_id={client_id}'

        # Send HTTP Request
        try:
            response = requests.post(auth_url, 
                headers = {'Content-Type':'application/x-www-form-urlencoded'}, 
                data = payload, 
                auth = (client_id, self.client_secret)
                )
        except Exception as exp:
            print(f'Caught exception: {exp}')
    

        if response.status_code == 200:  # HTTP Status 'OK'
            print('Authentication success')
            access_token = response.json()['access_token']
            refresh_token = response.json()['refresh_token']
            expires_in = int(response.json()['expires_in'])
        if response.status_code != 200:
            print(f'RDP authentication failure: {response.status_code} {response.reason}')
            print(f'Text: {response.text}')
            raise requests.exceptions.HTTPError(f'RDP authentication failure: {response.status_code} - {response.text} ', response = response )
        
        return access_token, refresh_token, expires_in
    
    def rdp_request_esg(self, esg_url, access_token, universe):

        if not esg_url or not access_token or not universe:
            raise TypeError('Received invalid (None or Empty) arguments')

        payload = {'universe': universe}
        # Request data for ESG Score Full Service
        try:
            response = requests.get(esg_url, headers={'Authorization': f'Bearer {access_token}'}, params = payload)
        except Exception as exp:
            print(f'Caught exception: {exp}')

        if response.status_code == 200:  # HTTP Status 'OK'
            print('Receive ESG Data from RDP APIs')
            #print(response.json())
        else:
            print(f'RDP APIs: ESG data request failure: {response.status_code} {response.reason}')
            print(f'Text: {response.text}')
            raise requests.exceptions.HTTPError(f'ESG data request failure: {response.status_code} - {response.text} ', response = response )

        return response.json()

    def rdp_request_search_explore(self, search_url, access_token, payload):

        if not search_url or not access_token or not payload:
            raise TypeError('Received invalid (None or Empty) arguments')

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        try:
            response = requests.post(search_url, headers = headers, data = json.dumps(payload))
        except Exception as exp:
            print(f'Caught exception: {exp}')
        
        if response.status_code == 200:  # HTTP Status 'OK'
            print('Receive Search Explore Data from RDP APIs')
            #print(response.json())
        else:
            print(f'RDP APIs: Search Explore request failure: {response.status_code} {response.reason}')
            print(f'Text: {response.text}')
            raise requests.exceptions.HTTPError(f'Search Explore request failure: {response.status_code} - {response.text} ', response = response )

        return response.json()

