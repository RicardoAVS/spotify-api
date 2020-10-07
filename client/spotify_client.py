import requests
import base64
import datetime
import urllib.parse


def handle_status_code(status_code):
    if status_code not in range(200, 299):
        raise Exception('Resource Not Found')
    return True


class SpotifyAPI(object):
    client_id = None
    client_secret = None
    access_token = None
    has_expired = datetime.datetime.now()
    token_url = 'https://accounts.spotify.com/api/token'

    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        
        
    def get_credentials(self):
        
        if self.client_id is None or self.client_secret is None :
            raise Exception('Invalid client id or secret id')
        
        client_creds = f'{self.client_id}:{self.client_secret}'
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
       
       
    def get_resource_header(self):
        access_token = self.get_acess_token()
        return { "Authorization": f'Bearer {access_token}' }
        
    def get_token_header(self):
        client_creds_b64 = self.get_credentials()
        return { 'Authorization': f'Basic {client_creds_b64}' }
        
        
    def get_token_body(self):
        return { 'grant_type': 'client_credentials' }
    
    
    # Authenticate user, this step is required since we will need an acess token to call the API 
    def do_authentication(self):
        url = self.token_url
        headers = self.get_token_header()
        body = self.get_token_body()
        response = requests.post(url, data=body, headers=headers)
        status_code = response.status_code
        
        if status_code not in range(200, 299):
            raise Exception('Could not Authenticate client.')
        token_response = response.json()
        self.access_token = token_response['access_token']
        
        now = datetime.datetime.now()
        expires_in = token_response['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.has_expired = now > expires
       
        print('Token generated succesfully')
        return True
    
    
    def get_acess_token(self):
        token = self.access_token
        has_expired = self.has_expired
        if token == None or has_expired:
            raise Exception('Either there is no access token or session has expired.')
        return token
        
        
    """@id: The spotify ID for each resource
        @resource: the search will be based upon this (album, artist, track, etc.)
        @version: spotify API current version 
    """    
    def get_resource(self, _id, resource, version='v1'):
        endpoint = f'https://api.spotify.com/{version}/{resource}/{_id}'
        headers = self.get_resource_header()
        response = requests.get(endpoint, headers=headers)
        status_code = response.status_code
        
        if self.handle_status_code(status_code):
            return response.json()
        
        
    def get_album(self, _id):
        return self.get_resource(_id, resource='albums')
    
    
    def get_artist(self, _id):
        return self.get_resource(_id, resource='artists')
        
        
     """
        Get Spotify Catalog information about albums, artists, playlists, tracks, shows or episodes that match a keyword string
        @query: 	Required.
                    Search query keywords and optional field filters and operators.
                    For example: q=roadhouse%20blues
                    
        @query_type: Required.
                    A comma-separated list of item types to search across.
                    Valid types are: album , artist, playlist, track, show and episode.
                    Search results include hits from all the specified item types.
                    For example: q=name:abacab&type=album,track returns both albums and tracks with “abacab” included in their name.
    """
    def base_search(self, query, query_type='track'):
        endpoint= 'https://api.spotify.com/v1/search?'
        headers = self.get_resource_header()
        look_up = endpoint + query

        response = requests.get(look_up, headers=headers)
        status_code = response.status_code
        
        if not self.handle_status_code(status_code):
            return {}
        return response.json()
        
        
     """
        @operator: The operator NOT can be used to exclude results.
        For example: q=roadhouse%20NOT%20blues returns items that match “roadhouse” but excludes those that also contain the keyword “blues”. 
        
        Similarly, the OR operator can be used to broaden the search: q=roadhouse%20OR%20blues returns all the results that include either of the terms.
        Only one OR operator can be used in a query.
        
        Note: Operators must be specified in uppercase.
        
        example use case: query='All I Want', operator='NOT', query_operator='A Day To Remember'
        
        Field filters: By default, results are returned when a match is found in any field of the target object type. 
        Searches can be made more specific by specifying an album, artist or track field filter.
        
        For example: The query q=album:gold%20artist:abba&type=album 
        returns only albums with the text “gold” in the album name and the text “abba” in the artist name.
    """
    def search(self, query=None, operator=None, query_operator=None, query_type='artists'):
        if query is None:
            raise Exception('A query is required.')
        if isinstance(query, dict):
            # Encode query to q=album:gold%20artist:abba&type=album format
            query = " ".join(f'{key}:{value}' for key, value in query.items())
            
        if operator is not None and query_operator is not None:
            if not isinstance(query_operator, str):
                raise Exception("query_operator must be a valid String")
            if operator.lower() == 'or' or operator.lower() == 'not':
                operator = operator.upper()
                # Allow to perform an operator query like q=roadhouse%20NOT%20blues
                query = f'{query} {operator} {query_operator}'
                
        query_data = urllib.parse.urlencode({'q': query, 'type': query_type.lower()}) 
        return self.base_search(query_data)
      
      
    def handle_status_code(self, status_code):
        if status_code not in range(200, 299):
            raise Exception('Resource Not Found')
        return True