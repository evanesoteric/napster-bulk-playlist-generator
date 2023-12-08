"""
    Parse
    ~~~

    Parse album metadata from web app
    Scrape track id metadata from album via API
"""

from config import *
from api_auth import *


# create tracklist of all albums
master_tracklist = []

# pseudo list of parsed album id tags
# api_albums = []

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
  # for api_album in api_albums:

    # pseudo list of tracks in album
    album_tracklist = []

    try:
        r = requests.get(url=api_url + '/' + api_version + f'/albums/{album}/tracks', headers=headers)
        # r = requests.get(url=api_url + '/' + api_version + f'/albums/{api_album}/tracks', headers=headers)

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

# write master_tracklist to file
with open('master_tracklist.txt', 'r') as f:
    for track in master_tracklist:
        f.write(track + '\n')

# done
print(f'[{str(len(master_tracklist))} tracks]')
print('Saved to \'master_tracklist.txt\'.')
print()
print(master_tracklist)
