"""
    Main
"""

from config import *
from api_auth import *

# create tracklist of all albums
master_tracklist = []

# pseudo list of parsed album id tags
api_albums = []


# Parse album metadata from web app
# for album in albums:
#     try:
#         r = requests.get(url=album, timeout=15, headers=user_agent_header)

#         # valid response
#         if r.status_code == 200:
#             page = BeautifulSoup(r.text, 'lxml')
#             # parse metadata from 'page' request
#             page_metadata = page.find('div', class_='page-metadata')

#             # parse metadata
#             try:
#                 parse_meta_artist_id = re.search(r'meta_artist_id="(.*?)"', str(page_metadata)).group()
#                 parse_meta_artist_id = parse_meta_artist_id.replace('meta_artist_id=', '')
#                 meta_artist_id = parse_meta_artist_id.replace('"', '')

#                 parse_meta_album_id = re.search(r'meta_album_id="(.*?)"', str(page_metadata)).group()
#                 parse_meta_album_id = parse_meta_album_id.replace('meta_album_id=', '')
#                 meta_album_id = parse_meta_album_id.replace('"', '')

#                 # add to api_links for later track scraping
#                 api_albums.append(meta_album_id)
#             except Exception as e:
#                 logging.critical(f'Could not parse \'page_metadata\'!: {e}')
#                 print(f'Could not parse \'page_metadata\'!: {e}')
#                 print(e)

#         else:
#             rs = str(r.status_code)
#             logging.error(f'Request did not return \'200\' status!: [{rs}]')
#             print(f'Request did not return \'200\' status!: [{rs}]')

#     except Exception as e:
#         logging.critical(f'Could not get artist and album information!: {e}')
#         print(f'Could not get artist and album information!: {e}')
#         # or could not get all instances... try again...


# Scrape track id metadata from album via API
for album in albums:

    # pseudo list of tracks in album
    album_tracklist = []

    headers = api_auth()

    try:
        r = requests.get(url=api_url + '/' + api_version + f'/albums/{album}/tracks', headers=headers)

        # get tracks
        if r.status_code == 200:
            try:
                data = json.loads(r.text)

                # add album tracks to tracklist
                for track in data.get('tracks'):
                    album_tracklist.append(track.get('id'))
                    print(track.get('id'))

                # clean-up tracklist
                album_tracklist = list(filter(None, album_tracklist))

                # append tracklist to master tracklist
                master_tracklist = master_tracklist + album_tracklist

            except Exception as e:
                logging.critical(f'Could not parse \'data\'!: {e}')
                print(f'Could not parse \'data\'!: {e}')
                print(e)

        else:
            rs = str(r.status_code)
            logging.error(f'Request did not return \'200\' status!: [{rs}]')
            print(f'Request did not return \'200\' status!: [{rs}]')

    except Exception as e:
        logging.critical(f'Could not make request [{album}]!: {e}')
        print(f'Could not make request [{album}]!: {e}')


# remove duplicates from master_tracklist
master_tracklist = list(set(master_tracklist))

# done
print(f'[{str(len(master_tracklist))} tracks]')
print(master_tracklist)
print()

# # shuffle tracklist
# nova_tracklist = master_tracklist
# random.shuffle(nova_tracklist)
# print(nova_tracklist[0:4])

# choose random playlist name
playlist_name = playlist_names
random.shuffle(playlist_name)
playlist_name = playlist_name[0]

# master_tracklist = ['tra.000000000', 'tra.111111111', 'tra.222222222', 'tra.333333333']

# create playlist for each account:
for account in accounts:
    # authenticate via OAUTH
    headers = api_auth(account)

    # randomize master_tracklist order
    account_tracklist = master_tracklist
    random.shuffle(account_tracklist)

    # pseudo list for dict objects
    data_tracklist = []

    # convert list to list of dictionaries
    for track in account_tracklist:
        track = {'id': track}
        data_tracklist.append(track)

    # convert list to json
    json_tracklist = json.dumps(data_tracklist)

    # tags (Hip-Hop, Rap) [public or private playlist scope]
    # data = '{"playlists": {"name": "' + playlist_name + '", "privacy": "public", "tags": [{"id": "tag.152196515"}, {"id": "tag.219660537"}], "tracks": ' + json_tracklist + '}}'
    data = '{"playlists": {"name": "' + playlist_name + '", "privacy": "private", "tags": [{"id": "tag.152196515"}, {"id": "tag.219660537"}], "tracks": ' + json_tracklist + '}}'

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


print()
print("Done")