# LightControl

Controls lights in a Legrand Home+Control installation in a quick and dirty way.

It has been tested on linux and android using Termux. My only goal was to control my lights through my PinePhone (without installing Anbox) and since it has been acheived for me, here is source (with no warranty whether you can use it).

## Install

This software relies on python3. Install it and if necessaries dependencies through pip.

Configuration is stored in `~/.config/LightControl`.

You should have an account on https://portal.developer.legrand.com and subscribe to the starter kit.

Copy `app_data.json` in the configuration directory and fill the fields with information sent by Legrand on subscription, namely `client_id`, `client_secret` and `subscription_key`.

Then login using the `LE_login.py` script. It should open a webpage to complete the login process and get the token necessary to use the application. Once this process is done, it should not be necessary to login again since the token should be refreshed automatically.

You should now be able to get your topology, try `LE_topology.py`, which should print the topology as a json format to standard output. Before using the TUI interface, you need to create `topology.json` in the configuration directory. You can do so by issuing :

	python LE_topology.py > ~/.config/LightControl/topology.json.

## Usage

Once everything is set-up, you can execute the text ui by launching `lc.py`.

It will print out your lights and their status and give you a command line :

	Room1
	 a - Light1
	 b - Variator1 (100)
	 c # Light2
	Room2
	 d - Light3
	 e - Variator2 (40)
	cmd> 

Each light has a letter in front. 
 * to toggle lights, simply enter the letters you want to toggle (eg: "bcd") and presse Enter
 * to change the value of a variator, enter the letter in uppercase followed by the value you want to set (eg: "B10" to set Variator1 intensity to 10%)
 * to refresh write a non-alpha character 
 * to quit simply press Enter (empty command)
