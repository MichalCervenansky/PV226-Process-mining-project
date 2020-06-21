import os


def find_in_string(filename, string):
    with open(filename) as f:
        if string in f.read():
            return True
        return False


def run_main():
    return os.system(
        """python jira-pm/__main__.py https://issues.redhat.com 'project=WFLY AND type="Feature Request"' """)


def test_output_correct():
    run_main()
    assert os.path.exists('output-process.xes')

