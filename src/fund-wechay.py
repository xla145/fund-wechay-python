# -*- coding: UTF-8 -*-
"""doc"""
import asyncio
import logging
import os
from typing import Optional, Union

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from wechaty import Wechaty, Contact, UrlLink
from wechaty.user import Message, Room
from wechaty_puppet import ScanStatus, get_logger  # type: ignore

from service.fund import get_south_north_fund
from service.msg_service import get_wx_public_article_url_link, get_weather_url_link, get_music_file_url

"""
微信机器人
"""

log: logging.Logger = get_logger('MyBot')


class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """

    def __init__(self):
        super().__init__()
        global contact_ids
        global room_ids
        contact_ids = ['wxid_zs0tjy7p1jl922']
        room_ids = ["9680172400@chatroom"]

    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        from_contact = msg.talker()
        log.info(from_contact.get_id())
        text = msg.text()
        room = msg.room()
        if msg.message_type() == bot.Message.Type.MESSAGE_TYPE_RECALLED:
            recalled_msg = await msg.to_recalled()
            log.info("撤回的消息 %s" % recalled_msg)
        if room:
            # 如果不是@的消息，不用进行回复
            if text.find("@") == -1:
                return
        # 根据收到的信息，进行回复
        log.info(text)
        if text.find("英语") != -1:
            url_link = get_wx_public_article_url_link("田间小站")
        elif text.find("早上") != -1:
            url_link = get_wx_public_article_url_link("早晨简报")
        elif text.find("天气") != -1:
            url_link = get_weather_url_link()
        elif text.find("北上资金") != -1:
            url_link = get_south_north_fund()
        elif text.find("音乐") != -1:
            text = text.replace("音乐-", "")
            url_link = get_music_file_url(text)
        else:
            url_link = "开发中。。。。。。。。。。。。。。"
        conversation: Union[
            Room, Contact] = from_contact if room is None else room
        await conversation.ready()
        await conversation.say(url_link)

    # 登录成功后，，，
    async def on_login(self, contact: Contact):
        log.info(f'user: {contact} has login')
        # async中使用定时任务框架APScheduler，使用子类 AsyncIOScheduler
        scheduler.add_job(self.send_weather_msg, 'cron', id='send_weather_msg', hour=7, minute=40)
        scheduler.add_job(self.morning_news, 'cron', id='morning_news', hour=7, minute=40)
        scheduler.start()

    # 发送当天天气
    async def send_weather_msg(self):
        url_link: UrlLink = get_weather_url_link()
        for room_id in room_ids:
            await self.Room.load(room_id[0]).say(url_link)
        await self.Contact.load(contact_ids[0]).say(url_link)

    # 发送公众号相关信息
    async def morning_news(self):
        url_link = get_wx_public_article_url_link('早晨简报')
        for room_id in room_ids:
            await self.Room.load(room_id[0]).say(url_link)
        await self.Contact.load(contact_ids[0]).say(url_link)

    async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
                      data: Optional[str] = None):
        contact = self.Contact.load(self.contact_id)
        log.info(f'user <{contact}> scan status: {status.name} , '
                 f'qr_code: {qr_code}')


bot: Optional[MyBot] = None
os.environ['WECHATY_PUPPET'] = 'wechaty-puppet-hostie'
os.environ['WECHATY_PUPPET_HOSTIE_TOKEN'] = 'puppet_padplus_34e72d35e81e6ae1'


async def main():
    """doc"""
    global bot
    global scheduler
    bot = MyBot()
    scheduler = AsyncIOScheduler()
    await bot.start()


asyncio.run(main())
