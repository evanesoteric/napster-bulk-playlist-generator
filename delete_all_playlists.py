from config import *
from api_auth import *

# delete all playlists
for account in accounts:
    headers = api_auth(account=account)

    # pseudo list for detected playlists
    playlist_tags = []

    # detect playlist id tags
    try:
        r = requests.get(url=api_url + '/' + api_version + f'/me/library/playlists', headers=headers)

        if r.status_code == 200:
            playlists = json.loads(r.text)
            playlists = playlists.get('playlists')

            for i in playlists:
                playlist_tags.append(i.get('id'))

        else:
            rs = str(r.status_code)
            logging.error(f'Request did not return \'200\' status!: [{rs}]')
            print(f'Request did not return \'200\' status!: [{rs}]')

    except Exception as e:
        logging.critical(f'Could not detect playlist IDs!: {e}')
        print(f'Could not detect playlist IDs!: {e}')


    # delete playlists
    # sleep for 5 seconds after every 5 requests
    sitrep = 0
    for playlist_id in playlist_tags:
        sitrep += 1

        try:
            r = requests.delete(url=api_url + '/' + api_version + f'/me/library/playlists/{playlist_id}', headers=headers)
        except Exception as e:
            logging.critical(f'Could not delete playlist [playlist_id]!: {e}')
            print(f'Could not delete playlist [playlist_id]!: {e}')

        if sitrep % 5 == 0:
            logging.info(f'[delete_all_playlists] sleeping...!: {e}')
            time.sleep(5.6)