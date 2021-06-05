import app.utils as common_utils
import calendar
import time
from app import oauth_vars
import requests
from app import oauth_google_client
from app.customer.enums import OauthTypeEnum
import json
import urllib.parse

def clean_up_request(d):
    return common_utils.clean_up_request(d)

def send_mail(customer):
    common_utils.send_auth_email(customer)

def get_oauth_url(type, redirect_uri):
    if type == OauthTypeEnum.GOOGLE:
        try:
            authorization_endpoint = get_google_provider_config()["authorization_endpoint"]
            request_uri = oauth_google_client.prepare_request_uri(
                authorization_endpoint,
                redirect_uri=redirect_uri,
                scope=["openid", "email", "profile"],
            )
            return request_uri
        except Exception as e:
            print(e)
    else:
        vars = {
            "client_id": oauth_vars["social_id"],
            "redirect_uri": redirect_uri,
            "state": "abc",
            "scope": "email"
        }
        return (oauth_vars["social_url"] + "?" + urllib.parse.urlencode(vars))
    return None

def get_user_email_from_oauth(code, url, redirect_url, type):
    if type == OauthTypeEnum.GOOGLE:
        return get_email_from_google_oauth(code, url, redirect_url)
    return get_email_from_facebook_oauth(code, url, redirect_url)

def get_email_from_facebook_oauth(code, url, redirect_url):
    access_token_url = "https://graph.facebook.com/v10.0/oauth/access_token"
    access_vars = {
        "client_id": oauth_vars["social_id"],
        "client_secret": oauth_vars["social_secret"],
        "redirect_uri": redirect_url,
        "code": code,
        "scope": "email"
    }
    res = requests.get(access_token_url, params = access_vars).json()
    if "access_token" in res:
        access_token = res["access_token"]
        info_url = "https://graph.facebook.com/me"
        info_vars = {
            "fields": "email",
            "access_token": access_token
        }
        res = requests.get(info_url, params = info_vars).json()
        return res['email']
    return None

def get_email_from_google_oauth(code, url, redirect_url):
    google_config = get_google_provider_config()
    token_endpoint = google_config["token_endpoint"]
    token_url, headers, body = oauth_google_client.prepare_token_request(
        token_endpoint,
        authorization_response = url,
        redirect_url = redirect_url,
        code = code
    )
    token_response = requests.post(
        token_url,
        headers = headers,
        data = body,
        auth = (oauth_vars["client_id"], oauth_vars["client_secret"])
    )
    oauth_google_client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_config["userinfo_endpoint"]
    uri, headers, body = oauth_google_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers = headers, data = body)
    if userinfo_response.json().get("email_verified"):
        user_email = userinfo_response.json()["email"]
        return user_email
    return None

def get_google_provider_config():
    return requests.get(oauth_vars["discovery_url"]).json()
