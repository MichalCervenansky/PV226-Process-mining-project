from jira import JIRA

import codecs
import os
import sys
import xes
import dateutil.parser


def convertToValidTimeStamp(isoTimestamp):
    return dateutil.parser.isoparse(isoTimestamp).isoformat(sep="T")


def write_xes(basename, dir, issues):
    output = codecs.open(os.path.join(dir, basename + '-process.xes'), 'w', encoding='utf-8')
    log = xes.Log(features=[])
    log.infer_global_attributes = False
    log.global_event_attributes = [
        xes.Attribute(type="string", key="concept:name", value="__INVALID__"),
        xes.Attribute(type="string", key="lifecycle:transition", value="string"),
        xes.Attribute(type="string", key="org:resource", value="string")
    ]
    log.global_trace_attributes = [
        xes.Attribute(type="string", key="concept:name", value="__INVALID__")
    ]
    for issue in issues:
        trace = xes.Trace()
        trace.add_attribute(xes.Attribute(type="string", key="concept:name", value=issue["key"]))
        createdEvent = xes.Event()
        createdEvent.add_attribute(xes.Attribute(type="string", key="org:resource", value=issue["author"]))
        createdEvent.add_attribute(xes.Attribute(
            type="date",
            key="time:timestamp",
            value=convertToValidTimeStamp(issue["created"])
        ))
        createdEvent.add_attribute(xes.Attribute(type="string", key="concept:name", value="Open"))
        createdEvent.add_attribute(xes.Attribute(type="string", key="lifecycle:transition", value="complete"))
        trace.add_event(createdEvent)
        for transition in issue['transitions']:
            event = xes.Event()
            event.add_attribute(xes.Attribute(type="string", key="lifecycle:transition", value="complete"))
            event.add_attribute(xes.Attribute(type="string", key="org:resource", value=transition["who"]))
            event.add_attribute(xes.Attribute(
                type="date",
                key="time:timestamp",
                value=convertToValidTimeStamp(transition["when"])
            ))
            if (transition["what"]["field"] == "status"):
                eventValue = transition["what"]["toString"]
            elif (transition["what"]["field"] == "description"):
                eventValue = "Change Description"
            else:
                eventValue = "Change Field: {field}".format(field=transition["what"]["field"])
            event.add_attribute(xes.Attribute(type="string", key="concept:name", value=eventValue))
            trace.add_event(event)
        log.add_trace(trace)
    log.classifiers = [
        xes.Classifier(name="MXML Legacy Classifier", keys="concept:name lifecycle:transition"),
        xes.Classifier(name="Event Name", keys="concept:name"),
        xes.Classifier(name="Resource", keys="org:resource")
    ]
    output.write(str(log))


def transformTransitionAuthor(transition):
    try:
        return transition.author.displayName
    except AttributeError:
        return ""


def transformIssueAuthor(issue):
    try:
        return issue.fields.creator.displayName
    except AttributeError:
        return ""


def getTransitions(issue):
    transitions = []
    for history in issue.changelog.histories:
        for item in history.items:
            transition = {
                'when': history.created,
                'who': transformTransitionAuthor(history),
                'what': {
                    'field': item.field,
                    'fromString': item.fromString if item.fromString else "Undefined",
                    'toString': item.toString if item.toString else "Undefined"
                }
            }
            transitions.append(transition)
    return transitions


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError('Jira server aj Jira query were not specified')
    print('Gathering issues from ' + sys.argv[1] + ' returned by Jira query: ' + sys.argv[2])

    jira = JIRA(server=sys.argv[1])

    issues = jira.search_issues(sys.argv[2], maxResults=-1, expand="changelog")

    transformedIssues = []

    for issue in issues:
        transformedIssue = {
            'key': issue.key,
            'created': issue.fields.created,
            'author': transformIssueAuthor(issue),
            'transitions': getTransitions(issue)
        }
        transformedIssues.append(transformedIssue)

    write_xes('output', '.', transformedIssues)
