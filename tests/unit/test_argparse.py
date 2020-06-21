import os


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4


def test_args():
    assert 512 == os.system('python jira-pm/__main__.py')
    assert 512 == os.system('python jira-pm/__main__.py --jira-server arg_one')
    assert 512 == os.system('python jira-pm/__main__.py --jira-server --query arg_one arg_two')


def run_main():
    return os.system(
        """python jira-pm/__main__.py --jira-server https://issues.redhat.com --query 'project=WFLY AND type="Feature 
        Request"' """)


def test_without_specified_output():
    run_main()
    assert os.path.exists('output.xes')


def test_relative_output():
    os.system(
        """python jira-pm/__main__.py --jira-server https://issues.redhat.com --query 'project=WFLY AND type="Feature 
        Request"' --output wildfly-feature-requests """)
    assert os.path.exists('wildfly-feature-requests-process.xes')


def test_absolute_output():
    os.system(
        """python jira-pm/__main__.py --jira-server https://issues.redhat.com --query 'project=WFLY AND type="Feature 
        Request"' --output /home/mcervenansky/PycharmProjects/PV226-Process-mining-project/wildfly-feature-requests""")
    assert os.path.exists('/home/mcervenansky/PycharmProjects/PV226-Process-mining-project/wildfly-feature-requests')
