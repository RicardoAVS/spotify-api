### <h1>SPOTIFY-API</h1>

This project is based on the Spotify API, it consist on a basic class which helps perform simple queries to the API endpoint.

### <h2>Version</h2>

By default the Base Spotify API endpoint is `https://api.spotify.com/` which is currently on v1 version. 
This may change in the future for this reason it is recommended to check Spotify Website for changes.

### <h2>HTTP Status Code</h2>

There are three classes which are the most common

| Status Code | Description |
|   :---:     |:---         |
| ```200```   | This mean the request was successful and will return the response|
| ```404```   | <p>This is the most common which means the resource could not be found either <br>because a bad URL or the resource does not exist</p>|
| ```500```   | <p>When you get a 500 response it usally is because the server has encounter an error</p>|

### <h2>Mehods</h2>

```do_authentication```: Autenthicate the user with the client id and client token provided by Spotify.

```get_access_token``` : Will return True is token has expired otherwise return False

```get_resources```    : Receive as parameters the type of search, id and version of the API and returns the corresponding query
 
```get_album```        : Peforms a search based on the album id 

```get_artist```       : Peforms a search based on the artist id 

```search```           : Pass a dic or operator as params to do a more specific search 

## Example usage for search:

The following query ```new_session.search({"track": "All I Want", "artist": "a day to remember"}, query_type="track")``` will return:

```{'tracks': {'href': 'https://api.spotify.com/v1/search?query=track%3AAll+I+Want+artist%3Aa+day+to+remember&type=track&offset=0&limit=20',
  'items': [{'album': {'album_type': 'album',
     'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/4NiJW4q9ichVqL1aUsgGAN'},
       'href': 'https://api.spotify.com/v1/artists/4NiJW4q9ichVqL1aUsgGAN',
       'id': '4NiJW4q9ichVqL1aUsgGAN',
       'name': 'A Day To Remember',
       'type': 'artist',
       'uri': 'spotify:artist:4NiJW4q9ichVqL1aUsgGAN'}],
     'available_markets': ['AD',
      'AE',
      'AL',
      'AR',
      'AT',
      'AU',
      'BA'
      ....
```

Now using operators ```new_session.search(query="One", operator="NOT", query_operator="Impious", query_type="track")```

```
{'tracks': {'href': 'https://api.spotify.com/v1/search?query=One+NOT+Impious&type=track&offset=0&limit=20',
  'items': [{'album': {'album_type': 'single',
     'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/1vyhD5VmyZ7KMfW5gqLgo5'},
       'href': 'https://api.spotify.com/v1/artists/1vyhD5VmyZ7KMfW5gqLgo5',
       'id': '1vyhD5VmyZ7KMfW5gqLgo5',
       'name': 'J Balvin',
       'type': 'artist',
       'uri': 'spotify:artist:1vyhD5VmyZ7KMfW5gqLgo5'},
      {'external_urls': {'spotify': 'https://open.spotify.com/artist/6M2wZ9GZgrQXHCFfjv46we'},
       'href': 'https://api.spotify.com/v1/artists/6M2wZ9GZgrQXHCFfjv46we',
       'id': '6M2wZ9GZgrQXHCFfjv46we',
       'name': 'Dua Lipa',
       'type': 'artist',
       'uri': 'spotify:artist:6M2wZ9GZgrQXHCFfjv46we'}
       ....
```

### <h2>Disclaimer</h2>

This piece of code was done for the solely purpose of learning and in the future I might improve it as I get more experience along the way.
