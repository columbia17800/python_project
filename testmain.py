#!usr/bin/env python3
import listui
import loginui
import chatui
import uisetting


def main():
	Setting = uisetting.UISetting()
	namelist = ["1", "2"]
	login = loginui.LogUI()
	listen = listui.ListUI(namelist)
	Setting.setUpButton()
	Setting.setUpButton()
	chat = chatui.ChatUI(Setting)

	chat.event_loop()

main()