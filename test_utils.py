import argparse
import utils


def test_get_limit():
    args = argparse.Namespace(limit=99)
    limit = utils.get_limit(args)
    assert limit == 99


def test_get_test_false():
    args = argparse.Namespace(limit=66, test=False)
    test = utils.get_test(args)
    assert test is False


def test_get_test_true():
    args = argparse.Namespace(limit=99, test=True)
    test = utils.get_test(args)
    assert test is True


def test_get_project():
    args = argparse.Namespace(rally_project='Project Starlink')
    project = utils.get_project(args)
    assert project == 'Project Starlink'


def test_get_sitename():
    args = argparse.Namespace(sitename='sandbox_sitename_replace')
    sitename = utils.get_sitename(args)
    assert sitename == 'something_other_than_this'


def test_get_workspace():
    args = argparse.Namespace(rally_workspace='2021')
    workspace = utils.get_workspace(args)
    assert workspace == '2021'