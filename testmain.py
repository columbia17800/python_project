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

	listen.event_loop()

main()