'''Action Source code.'''
import sys, os
import requests
import github
from pprint import pprint

# required to run the script locally
# from os.path import join, dirname
# from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)
class Label_Controller:
    def __init__(self, g_token,g_repo):
        g = github.Github(g_token)
        self._repo = g.get_repo(g_repo)




    def _get_labels_def(self, labels_from):
        assert labels_from
        if isinstance(labels_from, dict):
            labels_def = [labels_from]
        else:
            labels_def = labels_from
        assert isinstance(labels_from, list)
        assert isinstance(labels_from[0], dict)
        return labels_def

    def _get_label_properties(self, label_dict):
        assert isinstance(label_dict, dict)
        assert 'name' in label_dict
        assert 'color' in label_dict
        name = label_dict['name']
        color = label_dict['color']
        if color.startswith('#'):
            color = color[1:]
        description = github.GithubObject.NotSet
        if 'description' in label_dict:
            description = label_dict['description']
        old_name = name
        if 'old_name' in label_dict:
            old_name = label_dict['old_name']
        elif 'current_name' in label_dict:
            old_name = label_dict['current_name']
        print(name, color, description, old_name)
        return name, color, description, old_name

    def create_label(self, label_dict):
        name, color, description, *_ = self._get_label_properties(label_dict)
        if name == self._repo.get_label(name).name:
            return 'label already exsist'
        self._repo.create_label(name, color, description)
    def add_label(self,name,pnr):
        try:
            if name is None:
                name= ''
            if pnr is None:
                return ' PR number required'
            label = self._repo.get_label(name)
        except github.UnknownObjectException as e:
            return "Check label name"

        self._repo.get_issue(pnr).add_to_labels(label)


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
