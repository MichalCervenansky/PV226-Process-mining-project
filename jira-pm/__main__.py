import argparse
import codecs
import os
import sys
import xes
import dateutil.parser

from jira import JIRA
from progress.bar import IncrementalBar
from progress.spinner import Spinner


def convert_to_valid_timestamp(iso_timestamp):
    return dateutil.parser.isoparse(iso_timestamp).isoformat(sep="T")


def write_xes(output, directory, _issues):
    output = codecs.open(os.path.join(directory, output), 'w', encoding='utf-8')
    output_bar = IncrementalBar('Writing'.ljust(20), max=len(issues))
    log = xes.Log(features=[])
    log.infer_global_attributes = False
    log.global_event_attributes = [
        xes.Attribute(type="string", key="concept:name", value="__INVALID__"),
        xes.Attribute(type="string", key="lifecycle:transition",
                      value="string"),
        xes.Attribute(type="string", key="org:resource", value="string")
    ]
    log.global_trace_attributes = [
        xes.Attribute(type="string", key="concept:name", value="__INVALID__")
    ]
    for _issue in _issues:
        trace = xes.Trace()
        trace.add_attribute(xes.Attribute(
            type="string", key="concept:name", value=_issue["key"]))
        created_event = xes.Event()
        created_event.add_attribute(xes.Attribute(
            type="string", key="org:resource", value=_issue["author"]))
        created_event.add_attribute(xes.Attribute(
            type="date",
            key="time:timestamp",
            value=convert_to_valid_timestamp(_issue["created"])
        ))
        created_event.add_attribute(xes.Attribute(
            type="string", key="concept:name", value="Open"))
        created_event.add_attribute(xes.Attribute(
            type="string", key="lifecycle:transition", value="complete"))
        trace.add_event(created_event)
        for transition in _issue['transitions']:
            event = xes.Event()
            event.add_attribute(xes.Attribute(
                type="string", key="lifecycle:transition", value="complete"))
            event.add_attribute(xes.Attribute(
                type="string", key="org:resource", value=transition["who"]))
            event.add_attribute(xes.Attribute(
                type="date",
                key="time:timestamp",
                value=convert_to_valid_timestamp(transition["when"])
            ))
            if transition["what"]["field"] == "status":
                event_value = transition["what"]["toString"]
            elif transition["what"]["field"] == "comment":
                event_value = "Comment"
            elif transition["what"]["field"] == "description":
                event_value = "Change Description"
            else:
                event_value = "Change Field: {field}".format(
                    field=transition["what"]["field"])
            event.add_attribute(xes.Attribute(
                type="string", key="concept:name", value=event_value))
            trace.add_event(event)
        log.add_trace(trace)
        output_bar.next()
    output_bar.finish()
    log.classifiers = [
        xes.Classifier(name="MXML Legacy Classifier",
                       keys="concept:name lifecycle:transition"),
        xes.Classifier(name="Event Name", keys="concept:name"),
        xes.Classifier(name="Resource", keys="org:resource")
    ]
    output.write(str(log))


def transform_transition_author(transition):
    try:
        return transition.author.displayName
    except AttributeError:
        return ""


def transform_issue_author(_issue):
    try:
        return _issue.fields.creator.displayName
    except AttributeError:
        return ""


def get_transitions(_issue):
    transitions = []
    for history in _issue.changelog.histories:
        for item in history.items:
            transition = {
                'when': history.created,
                'who': transform_transition_author(history),
                'what': {
                    'field': item.field,
                    'fromString': item.fromString if item.fromString else "Undefined",
                    'toString': item.toString if item.toString else "Undefined"
                }
            }
            transitions.append(transition)
    for comment in _issue.fields.comment.comments:
        comment_transition = {
            'when' : comment.created,
            'who' : transform_transition_author(comment),
            'what' : {
                'field' : 'comment'
            }
        }
        transitions.append(comment_transition)
    return transitions


def fetch_issues(jira_client, jql):
    block_size = 100
    block_num = 0
    _issues = []
    fetching_spinner = Spinner('Fetching'.ljust(20))
    while True:
        start_index = block_num * block_size
        if block_num == 0:
            _issues = jira_client.search_issues(
                jql, startAt=start_index, maxResults=block_size, expand="changelog", fields="comment,created,creator")
        else:
            more_issues = jira_client.search_issues(
                jql, startAt=start_index, maxResults=block_size, expand="changelog", fields="comment,created,creator")
            if len(more_issues) > 0:
                for _issue in more_issues:
                    _issues.append(_issue)
            else:
                break
        fetching_spinner.next()
        if len(_issues) == 0:
            break
        block_num += 1
    fetching_spinner.finish()
    return _issues


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Welcome to jira-pm tool")
    parser.add_argument('-j', '--jira-server',
                        help="JIRA server to fetch issues from.")
    parser.add_argument('-q', '--query',
                        help="JQL Query to execute against server")
    parser.add_argument('-o', '--output',
                        help="Output file containing event log. Defaults to output.xes",
                        default="output.xes")
    args = parser.parse_args()
    if (args.jira_server is None or args.query is None):
        parser.print_help()
        sys.exit(1)
    print('Gathering issues from ' + args.jira_server +
          ' returned by JIRA query: ' + args.query)

    jira = JIRA(server=args.jira_server)
    issues = fetch_issues(jira, args.query)

    transformed_issues = []
    transform_bar = IncrementalBar('Transforming'.ljust(20), max=len(issues))

    for issue in issues:
        transformed_issue = {
            'key': issue.key,
            'created': issue.fields.created,
            'author': transform_issue_author(issue),
            'transitions': get_transitions(issue)
        }
        transformed_issues.append(transformed_issue)
        transform_bar.next()
    transform_bar.finish()

    write_xes(args.output, '.', transformed_issues)
