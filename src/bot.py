from datetime import datetime
from pydantic import BaseModel
import requests
from src.common import submission_link, extract_submission_id


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
      bot.send_message(chat_id, "Please, send me a submission id or a link to a submission for today's daily challenge")
      return

    submission_id = extract_submission_id(text.strip())
    
    if submission_id:
      print(f"Will update submissions for {username} on {today}: {text}")
      result = db.submissions.update_one(
        {'username': name, 'date': today, 'chat_id': chat_id},
        {'$set': {'text': submission_id}},
        True,
      )

      print(username, today, submission_id, result)
      bot.send_message(chat_id, f"Updated submission for {today}: {submission_link(submission_id)}")
      bot.send_message(LEETCODE_DAILY_GROUP_ID, f"New submission from {name}: {submission_link(submission_id)}")
    else:
      bot.send_message(chat_id, "Incorrect input! Please, send me a submission id or a link to a submission")
      raise ValueError(f"Incorrect link {data}")

  except Exception as e:
    print("Oops!")
    print(e)