import json
from os import mkdir, path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

def get_cred(path):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None

    if path.exists(path + 'token.json'):
        with open(path + 'token.json', 'r') as token:
            creds = json_to_cred(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(path + 'token.json', 'w') as token:
            json.dump(cred_to_json(creds), token, sort_keys=True, indent=4)
    return creds

def cred_to_json(cred_to_pass):
    cred_json = {
        'token': cred_to_pass.token,
        'refresh_token': cred_to_pass.refresh_token,
        'id_token': cred_to_pass.id_token,
        'token_uri': cred_to_pass.token_uri,
        'client_id': cred_to_pass.client_id,
        'client_secret': cred_to_pass.client_secret,
    }

    return cred_json

def json_to_cred(json_to_pass):
    cred_json = json.load(json_to_pass)
    creds = Credentials(
        cred_json['token'],
        refresh_token=cred_json['refresh_token'],
        id_token=cred_json['id_token'],
        token_uri=cred_json['token_uri'],
        client_id=cred_json['client_id'],
        client_secret=cred_json['client_secret']
    )

    return creds
