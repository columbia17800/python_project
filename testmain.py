#!usr/bin/env python3
import listui
import loginui
import chatui
import uisetting


def main():
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

	chat.event_loop()

main()