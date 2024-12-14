from src.common import submission_link, extract_submission_id


def test_submission_link():
    assert submission_link(123) == 'https://leetcode.com/submissions/detail/123'


def test_extract_submission_id():
    assert extract_submission_id('1242352') == '1242352'
    assert extract_submission_id('1') == '1'

    assert extract_submission_id('https://leetcode.com/submissions/detail/123') == '123'
    assert extract_submission_id('https://leetcode.com/submissions/detail/123/') == '123'
    assert extract_submission_id('https://leetcode.com/submissions/detail/1') == '1'

    assert extract_submission_id('https://leetcode.com/problems/two-sum/submissions/123') == '123'
    assert extract_submission_id('https://leetcode.com/problems/two-sum/submissions/123/') == '123'
    assert extract_submission_id('https://leetcode.com/problems/two-sum/submissions/1/') == '1'
    assert extract_submission_id('https://leetcode.com/problems/some-longer-problem-here/submissions/123') == '123'
    assert extract_submission_id('https://leetcode.com/problems/problem-with-69-numbers/submissions/123/') == '123'
    assert extract_submission_id('https://leetcode.com/problems/ii-112-645-32-sdfwsd-435-sad/submissions/123') == '123'
    assert extract_submission_id('https://leetcode.com/problems/a/submissions/123') == '123'

    assert not extract_submission_id('')
    assert not extract_submission_id('awewaefaw')
    assert not extract_submission_id('  ')
    assert not extract_submission_id('https://leetcode.com/submissions/detail/')
    assert not extract_submission_id('https://leetcode.com/problems/two-sum/submissions/')
    assert not extract_submission_id('https://leetcode.com/problems/54323423')
    assert not extract_submission_id('https://leetcode.com/problems/submissions/123')
    assert not extract_submission_id('https://leetcode.com/problems//submissions/123')
