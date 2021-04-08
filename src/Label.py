
import github


class Label_Controller:
    def __init__(self, g_token,g_repo):
        g_owner,g_repo = g_repo.split("/")
        assert isinstance(g_owner, str)
        assert isinstance(g_repo, str)


        g = github.Github(g_token)
        assert g.get_user().login

        rate_limit = g.get_rate_limit()

        orgs = [org.login for org in g.get_user().get_orgs()]
        
        if g_owner in orgs:
            owner = g.get_organization(g_owner)
        else:
            owner = g.get_user()
        self._repo = owner.get_repo(g_repo)



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
