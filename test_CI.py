import os


def test_args():
    # 256 seems to be ValueError
    assert 256 == os.system('python jira-pm/__main__.py')
    assert 256 == os.system('python jira-pm/__main__.py arg_one')
    assert 256 == os.system('python jira-pm/__main__.py arg_one arg_two')


def run_main():
    return os.system(
        """python jira-pm/__main__.py https://issues.redhat.com 'project=WFLY AND type="Feature Request"' """)


def test_without_specified_output():
    os.system('rm *.xes')
    run_main()
    assert os.path.exists('output-process.xes')
    os.system('rm *.xes')


def test_relative_output():
    os.system('rm *.xes')
    os.system(
        """python jira-pm/__main__.py https://issues.redhat.com 'project=WFLY AND type="Feature Request"' wildfly-feature-requests """)
    assert os.path.exists('wildfly-feature-requests-process.xes')
    os.system('rm *.xes')


def test_absolute_output():
    os.system('rm *.xes')
    os.system(
        """python jira-pm/__main__.py https://issues.redhat.com 'project=WFLY AND type="Feature Request"' /home/mcervenansky/PycharmProjects/PV226-Process-mining-project/wildfly-feature-requests""")
    assert os.path.exists('/home/mcervenansky/PycharmProjects/PV226-Process-mining-project/wildfly-feature-requests')
    os.system('rm *.xes')

def find_in_string(filename, string):
    with open(filename) as f:
        if string in f.read():
            return True
        return False

def test_output_correct():
    run_main()
    assert os.path.exists('output-process.xes')
    find_in_string('output-process.xes', )