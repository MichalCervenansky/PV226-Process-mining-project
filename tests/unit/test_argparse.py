import os
import tempfile


def test_args():
    assert 256 == os.system('python jira-pm/__main__.py')
    assert 256 == os.system('python jira-pm/__main__.py --jira-server arg_one')
    assert 512 == os.system('python jira-pm/__main__.py --jira-server --query arg_one arg_two')


def run_main():
    return os.system(
        """python jira-pm/__main__.py --jira-server https://issues.redhat.com --query 'project=WFLY AND type="Feature Request"' """)


def test_without_specified_output():
    run_main()
    assert os.path.exists('output.xes')


def test_relative_output():
    os.system(
        """python jira-pm/__main__.py --jira-server https://issues.redhat.com --query 'project=WFLY AND type="Feature Request"' --output wildfly-feature-requests """)
    assert os.path.exists('wildfly-feature-requests-process')


def test_absolute_output():
    tmp = tempfile.mkdtemp()
    filename = tmp + "/absolute"
    os.system(
        """python jira-pm/__main__.py --jira-server https://issues.redhat.com --query 'project=WFLY AND type="Feature Request"' --output filename""")
    assert os.path.exists(filename)
    os.remove(filename)
    os.removedirs(tmp)
