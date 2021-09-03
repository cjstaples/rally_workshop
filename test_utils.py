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
