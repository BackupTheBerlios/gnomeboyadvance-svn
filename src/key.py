gtk_to_sdl = {
65027:313, 	#alt gr
65288:8, 	#backspace
65289:9, 	#tab
65293:13, 	#enter
65299:19,	#pause
65300:302,	#scroll lock
65360:278,	#home
65361:276, 	#left
65362:273, 	#up
65363:275, 	#right
65364:274, 	#down
65365:280, 	#page up
65366:281, 	#page down
65367:279, 	#end
65377:316,	#print screen
65379:277,	#insert
65407:300,	#num lock
65421:271, 	#enter (KP)
65450:268, 	#*
65451:270, 	#+
65453:269, 	#-
65454:266, 	#.
65455:267, 	#/
65456:256, 	#0
65457:257, 	#1
65458:258, 	#2
65459:259, 	#3
65460:260, 	#4
65461:261, 	#5
65462:262, 	#6
65463:263, 	#7
65464:264, 	#8
65465:265, 	#9
65470:282,	#F1
65471:283,	#F2
65472:284,	#F3
65473:285,	#F4
65474:286,	#F5
65475:287,	#F6
65476:288,	#F7
65477:289,	#F8
65478:290,	#F9
65479:291,	#F10
65480:292,	#F11
65481:293,	#F12
65505:304,	#shift left
65506:303, 	#shift right
65507:306, 	#ctrl left
65508:305, 	#ctrl right
65535:127	#delete
}

sdl_refused = []
#F1 -> F11
for k in range(282, 293):
	sdl_refused.append(k)

#invers the dict
sdl_to_gtk = {}
for key, value in gtk_to_sdl.items():
	sdl_to_gtk[value] = key
