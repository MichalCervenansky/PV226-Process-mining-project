def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5


def test_not_enough_arguments():
    assert ValueError == exec(open('jira-pm/__main__.py').read())
