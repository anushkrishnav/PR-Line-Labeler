'''Action Source code.'''
import os
import requests
from Label import Label_Controller 
# from pprint import pprint

# required to run the script locally
# from os.path import join, dirname
# from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), "../.env")
# load_dotenv(dotenv_path)


def count_additions(prnum,token, repo):
    '''
    Count the number of additions made by the user.
    prnum : PR number
    token : Github Token
    repo : Reository for which we are retriving the count
    '''
    query_url = f"https://api.github.com/repos/{repo}/pulls/{prnum}"

    headers = {"Authorization": f"token {token}"}

    r = requests.get(query_url, headers=headers)
    raw = r.json()
    return raw['additions']-1


def get_latest_PR(token, repo):
    '''
    Get the contributor's latest Open Pull Request
    token : Github Token
    repo : Reository for which we are retriving the count
    '''
    query_url = f"https://api.github.com/repos/{repo}/pulls"
    headers = {"Authorization": f"token {token}"}
    r = requests.get(query_url, headers=headers)
    raw = r.json()
    num = int(raw[0]['number'])
    return num

def get_label(token, repo):
    '''
    Get all the labels present
    token : Github Token
    repo : Reository for which we are retriving the labels
    '''
    query_url = f"https://api.github.com/repos/{repo}/labels"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.symmetra-preview+json"}
    r = requests.get(query_url, headers=headers)
    raw = r.json()


def label_PR(pnr, repo, token,addition):
    '''
    Close the issue and add a comment to the issue stating the reason.

    prn : Pull Request number
    repo : Github Reository
    token : Github Token
    additions : Total number of additions made
    '''
    controller = Label_Controller(token,repo)
    if addition < 10: 
        return controller.add_label('Level0',pnr)
    if addition < 30:
        return controller.add_label('Level1',pnr)
    if addition < 99:
        return controller.add_label('Level2',pnr)
    if addition > 99:
        return controller.add_label('Level3',pnr)

token = os.environ["INPUT_TOKEN"]
repourl = os.environ["INPUT_REPO"]


prn = get_latest_PR(token=token, repo=repourl)
addition = count_additions(prnum = prn,token=token, repo=repourl )
label_PR(prn,repourl,token,addition)