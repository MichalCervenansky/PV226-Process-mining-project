
def test_not_enough_arguments():
    assert ValueError == exec(open('jira-pm/__main__.py').read())
