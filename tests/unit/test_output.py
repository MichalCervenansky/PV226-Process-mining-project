import os


def find_in_string(filename, string):
    with open(filename) as f:
        if string in f.read():
            return True
        return False


def run_main():
    return os.system(
        """python jira-pm/__main__.py --jira-server https://issues.redhat.com 'project=WFLY AND type="Feature 
        Request"' """)


def test_output_correct():
    run_main()

    item1 = """<event>
      <string key="lifecycle:transition" value="complete"/>
      <string key="org:resource" value="Paul Ferraro"/>
      <date key="time:timestamp" value="2020-05-26T11:07:17-04:00"/>
      <string key="concept:name" value="Change Field: issuetype"/>
    </event>"""
    item2 = """<event>
      <string key="lifecycle:transition" value="complete"/>
      <string key="org:resource" value="Jason Greene"/>
      <date key="time:timestamp" value="2013-07-18T01:10:07-04:00"/>
      <string key="concept:name" value="Change Field: Fix Version"/>
    </event>"""
    item3 = """"<event>
      <string key="lifecycle:transition" value="complete"/>
      <string key="org:resource" value="Jeff Mesnil"/>
      <date key="time:timestamp" value="2014-07-09T08:16:40-04:00"/>
      <string key="concept:name" value="Change Field: Link"/>
    </event>"""

    assert os.path.exists('output-process.xes') is True

    assert find_in_string('output-process.xes', item1) is True
    assert find_in_string('output-process.xes', item2) is True
    assert find_in_string('output-process.xes', item3) is True
