import re


def submission_link(submission_id):
  return f'https://leetcode.com/submissions/detail/{submission_id}'


def extract_submission_id(text: str) -> str:
  if text.isnumeric():
    return text

  for link_pattern in (
          r'https://leetcode.com/submissions/detail/\d+/?$',
          r'https://leetcode.com/problems/[a-zA-Z0-9-]+/submissions/\d+/?$'
  ):
    p = re.compile(link_pattern)
    if match := p.search(text):
      link = match.group()
      # we do know that an id exists here, as each pattern has \d+ qualifier
      return re.findall(r'\d+', link)[-1]

  return ''
