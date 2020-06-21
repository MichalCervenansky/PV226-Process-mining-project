import os


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4


def test_args():
    # 256 seems to be ValueError
    assert 256 == os.system('python jira-pm/__main__.py')
    assert 512 == os.system('python jira-pm/__main__.py arg_one')
    assert 512 == os.system('python jira-pm/__main__.py arg_one arg_two')


def test_output():
    os.system(
        """python jira-pm/__main__.py --jira-server https://issues.redhat.com --query 'project=WFLY AND type="Feature Request"' wildfly-feature-requests""")