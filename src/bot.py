from datetime import datetime
from pydantic import BaseModel
import requests
from src.common import submission_link
import re


LEETCODE_DAILY_GROUP_ID = '-1002270137956'


class Bot(BaseModel):
  token: str
  
  def api_url(self):
    return f"https://api.telegram.org/bot{self.token}/"

  def send_message(self, chat_id, message, useV2=False):
      if chat_id is None or message is None:
          return False

      params = {
          'chat_id': chat_id,
          'text': message,
          'disable_web_page_preview': True,
      }
      if useV2:
        params['parse_mode'] = 'MarkdownV2'
      res = requests.post(self.api_url() + "sendMessage", data=params).json()
      print(res)

      if res is None or 'result' not in res or 'message_id' not in res['result']:
          return None
      return res['result']['message_id']
    
    
def extract_id(text):
    # Define two separate patterns
    pattern1 = r"https://leetcode\.com/submissions/detail/(\d+)/?"
    pattern2 = r"https://leetcode\.com/problems/.+/submissions/(\d+)/?"
    
    # Try matching the first pattern
    match1 = re.search(pattern1, text)
    if match1:
        return match1.group(1)
    
    # Try matching the second pattern
    match2 = re.search(pattern2, text)
    if match2:
        return match2.group(1)
    
    # If no match, return None
    return None
    
    
def process_message(bot, db, data):
  try:
    message = data['message']
    chat_id = message['chat']['id']
    text = message['text']
    today = datetime.today().strftime('%Y-%m-%d')
    
    username = message['from']['username'] if 'username' in message['from'] else '😊'
    first_name = message['from']['first_name'] if 'first_name' in message['from'] else '😊'
    name = f'{first_name} ({username})'

    if text.startswith('/start') or text.startswith('/help'):
      bot.send_message(chat_id, "Please, send me a submission id for today's daily challenge")
    elif text.isnumeric():
      submission_id = text
    else:
      submission_id = extract_id(text)
    
    if submission_id is not None and submission_id.isnumeric():
      print(f"Will update submissions for {username} on {today}: {text}")
      result = db.submissions.update_one(
        {'username': name, 'date': today, 'chat_id': chat_id},
        {'$set': {'text': text}},
        True,
      )

      print(username, today, text, result)
      bot.send_message(chat_id, f"Updated submission for {today}: {submission_link(submission_id)}")
      bot.send_message(LEETCODE_DAILY_GROUP_ID, f"New submission from {name}: {submission_link(submission_id)}")
    else:
      bot.send_message(chat_id, "Incorrect input! please send me a submission id")
      raise ValueError(f"Incorrect link {data}")

  except Exception as e:
    print("Oops!")
    print(e)