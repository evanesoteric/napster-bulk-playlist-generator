from config import *
from api_auth import *

# choose random playlist name
playlist_name = playlist_names
random.shuffle(playlist_name)
playlist_name = playlist_name[0]

master_tracklist = ['tra.000000000', 'tra.111111111', 'tra.222222222', 'tra.333333333']
data_tracklist = []

# convert list to list of dictionaries
for track in master_tracklist:
    track = {'id': track}
    data_tracklist.append(track)

# convert list to json
json_tracklist = json.dumps(data_tracklist)

# tags (Hip-Hop, Rap)
data = '{"playlists": {"name": "' + playlist_name + '", "privacy": "public", "tags": [{"id": "tag.152196515"}, {"id": "tag.219660537"}], "tracks": ' + json_tracklist + '}}'

# create playlist for each account:
for account in accounts:
    headers = api_auth(account=account)

    # create new playlist
    try:
        r = requests.post(url=api_url + '/' + api_version + '/me/library/playlists', headers=headers, data=data)

        if r.status_code == 201:
            print(f'Playlist [{playlist_name}] created successfully!')
        else:
            rs = str(r.status_code)
            logging.error(f'Request did not return \'201\' status!: [{rs}]')
            print(f'Request did not return \'201\' status!: [{rs}]')

    except Exception as e:
        logging.critical(f'Could not create new playlist!: {e}')
        print(f'Could not create new playlist!: {e}')
        # or ...