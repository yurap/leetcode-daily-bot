from src.common import submission_link


def test_submission_link():
    assert submission_link(123) == 'https://leetcode.com/submissions/detail/123'
