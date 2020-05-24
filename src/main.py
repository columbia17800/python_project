#!usr/bin/env python3

try:
	from . import listui
	from . import loginui
	from . import chatui
	from . import uisetting
except:
	import listui
	import loginui
	import chatui
	import uisetting
import asyncio

async def main():
	Setting = uisetting.UISetting()
	namelist = ["1", "2"]
	id = loginui.LogUI()
	listen = listui.ListUI(namelist, id) # namelist should delete id
	that = listen.event_loop()
	Setting.setUpButton()
	Setting.setUpButton()
	chatroom = chatter()
	online = chatroom.pickAfriend(that)
	if online:
		chatroom.pickAfriend(that)
	else:
		print("Unexistint friend!")
	chat = chatui.ChatUI(Setting)

	await chat.event_loop()

asyncio.run(main())