from apscheduler.schedulers.background import BackgroundScheduler

from datetime import timedelta, datetime

from fastapi import FastAPI, Request, Body

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import logging, json, uvicorn

from config import Settings, Messages
from .model import Task
from .util import time_conv, text_conv


app = FastAPI()

scheduler = BackgroundScheduler()

bot_name = Settings.bot_name

# configure logging
formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(filename=Settings.log_file_path, level=logging.DEBUG, format=formatter)

# configure database
engine = sqlalchemy.create_engine(Settings.db_path, echo=True)

# configure line api
line_bot_api = LineBotApi(Settings.channel_access_token)
handler = WebhookHandler(Settings.channel_secret)

# configure reply message
Invalid_formard = Messages.Invalid_formard
Accepted = Messages.Accepted
Task_done = Messages.Task_done


@app.on_event("startup")
async def startup_event():
    logging.info("app startup")


@app.on_event("shutdown")
def shutdown_event():
    logging.info("app shutdown")


@app.post("/")
def callback(Request: Request, body: dict = Body(None)):
    # get X-Line-Signature header value
    signature = Request.headers['X-Line-Signature']
    # handle webhook body
    body = json.dumps(body,ensure_ascii=False,separators=(',', ':'))

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logging.error("Invalid signature. Please check your channel access token/channel secret.")

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if bot_name in event.message.text:
        if event.message.type == 'text':
            create_todo(event)

    return 'OK'


def create_todo(event):

    task = Task()

    user_id = event.source.user_id
    if event.source.type == 'group':
        group_id = event.source.group_id
        profile = line_bot_api.get_group_member_profile(group_id, user_id)
        task.push_id = group_id
    else:
        profile = line_bot_api.get_profile(user_id)
        task.push_id = user_id

    try:
        session = sessionmaker(bind=engine)()

        _, to_user, time, *details, by_user = text_conv(event.message.text).split(',')

        if details:
            pass
        else:
            details, by_user = ''.join(by_user), profile.display_name

        task.deadline = time_conv(time)
        task.to_user = to_user
        task.task_details = ''.join(details)
        task.by_user = by_user

        session.add(instance=task)
        session.flush()
        id : int = task.id
        run_date: str = task.deadline.strftime('%Y-%m-%d %H:%M:%S')

        session.commit()

        handle_scheduler(id, run_date)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(Accepted)
            )

    except ValueError:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(Invalid_formard)
            )
            
        logging.error("valueError")
    finally:
        session.close()


def tick(id: int) -> None:
    try:
        session = sessionmaker(bind=engine)()
        task = session.query(Task).filter(Task.id==id).first()
        
        message = Task_done % (task.deadline + timedelta(hours=9), task.to_user, ''.join(task.task_details), task.by_user)
        line_bot_api.push_message(task.push_id, TextSendMessage(text=message))
        
        logging.info("task done: {}...".format(''.join(task.task_details[:10])))
        
        task.is_active = False
        session.commit()
    except:
        logging.error("databaseError")
    finally:
        session.close()


def handle_scheduler(id: int, run_date: str) -> None:
    global scheduler
    scheduler.pause()
    
    scheduler.add_job(tick, 'date', run_date=run_date, args=[id])

    scheduler.resume()


def main():
    try:
        global scheduler
        session = sessionmaker(bind=engine)()
        tasks = session.query(Task).filter_by(is_active=True).order_by(Task.deadline)

        for task in tasks:
            
            id : int = task.id
            run_date: str = task.deadline.strftime('%Y-%m-%d %H:%M:%S')
            if task.deadline > datetime.now():
                scheduler.add_job(tick, 'date', run_date=run_date, args=[id])
            else:
                task.is_active = False
        else:
            session.commit()
            session.close()
        scheduler.start()
        
        uvicorn.run(app, host="0.0.0.0", port=8080)
    except:
        logging.error("startup failed")
    finally:
        scheduler.shutdown()