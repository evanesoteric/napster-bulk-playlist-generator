from config import *

api_rate_limit = 5
api_url = 'https://api.napster.com'
api_version = 'v2.2'
oauth_url = api_url + '/oauth/token'

app_id = ''         # napster API ID
api_key = ''        # napster API KEY
api_secret = ''     # napster API SECRET

params = (api_key, api_secret)

def api_auth(account=None):
    # use default api credentials if no account passed into function
    if account is None:
        username = api_default_username
        password = api_default_password
    else:
        try:
            username, password = account.split(':')
        except:
            print('[api_auth] Could not split username/password from account!')

    # get API authentication token for account
    try:
        data = {
            'username': username,
            'password': password,
            'grant_type': 'password'
            }

        r_login = requests.post(url=oauth_url, auth=params, data=data)

        tokens = json.loads(r_login.text)

        headers = {
            'Authorization': f"Bearer {tokens['access_token']}",
            'Content-Type': 'application/json',
            }

        return headers

    except Exception as e:
        logging.critical(f'[api_auth] Could not setup api_handler!: Error: {e}')
        print(e)
