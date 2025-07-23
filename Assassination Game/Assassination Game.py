import time
import PySimpleGUI as sg
sg.theme("DarkBrown4")
import pyperclip
import pygame
pygame.mixer.init()
import os
import sys

def main():

    SCRIPT_DIR = os.path.dirname(os.path. abspath(__file__))
    SFX_DIR = os.path.join(SCRIPT_DIR, "Assassination Game SFX")
    IMAGES_DIR = SCRIPT_DIR

    pay = 1000 
    sniper_rounds = 2
    pistol_rounds = 9
    health = 100

    enemy_health = 100

    def restart():
        restart_window = [
            [sg.Text("Would you like to restart?")],
            [sg.Button("Yes", bind_return_key=True), sg.Button("No")]
        ]

        window = sg.Window("Restart Window", restart_window, finalize=True)
        window["Yes"].set_focus()

        while True:
            restart_events, values = window.read()
            if(restart_events == "Yes"):
                sg.popup_no_buttons("Restarting...", no_titlebar=True, auto_close=True, auto_close_duration=2)
                break
            elif restart_events in ("No" or sg.WIN_CLOSED):
                sg.popup_no_buttons("See you!", no_titlebar=True, auto_close=True, auto_close_duration=2)
                sys.exit()
        main()

    def get_status():
        return [
            [sg.Text(f"Health: {health}", key='-HEALTH-')],
            [sg.Text(f"Funds: ${pay}", key='-FUNDS-')],
            [sg.Text(f"Sniper Rounds: {sniper_rounds}", key='-SNIPER_AMMO-')],
            [sg.Text(f"Pistol Rounds: {pistol_rounds}", key='-PISTOL_AMMO-')]
        ]

    def enemy_status():
        return [
            [sg.Text(f"Enemy Health: {enemy_health}", key='-ENEMY_HEALTH-')]
        ]
    
    def no_money(message="Transaction declined. You have no money left."):
        no_money_window = [
            [sg.Text(message, text_color="green")]
        ]

        window = sg.Window("No Money", no_money_window, no_titlebar=True, auto_close=True, auto_close_duration=3, keep_on_top=True)
        window.read()
        window.close()

    def encrypt_plaintext(text1, text2, shifted):
        result = ""
        for char in text1:
            if char.isalpha():
                base = ord('a') if char.islower() else ord('A')
                shifted_text = (ord(char) - base + shifted) % 26 + base
                result += chr(shifted_text)
            else:
                continue
        for char in text2:
            if char.isalpha():
                base = ord('a') if char.islower() else ord('A')
                shifted_text2 = (ord(char) - base + shifted) % 26 + base  
                result += chr(shifted_text2)
            if char.isdigit():
                digit_base = ord('0')
                shifted_digit = (ord(char) - digit_base + shifted) % 26 + base
                result += chr(shifted_digit)
            else:
                continue
        return result
    
    def BruteForce(ciphertext):
        results = ""
        for shift in range(1, 26):
            result = ""
            for char in ciphertext:
                if char.isalpha():
                    base = ord('a') if char.islower() else ord('A')
                    decrypted = (ord(char) - base - shift) % 26 + base
                    result += chr(decrypted)
                else:
                    result += char
            results += f"Shift {shift:2}: {result}\n"
        
        results_window = [
            [sg.Text("The brute force process found the following:")],
            [sg.Multiline(results, size=(80,25), font=("Typold Medium", 10), disabled=True)],
            [sg.Button("Continue", bind_return_key=True)]
        ]

        window = sg.Window("Brute Force Process Results", results_window, no_titlebar=True, finalize=True)
        window["Continue"].set_focus()

        while True:
            brute_force_events, _ = window.read()
            if(brute_force_events == "Continue"):
                window.close()
                break
                    
    def office_search():
        nonlocal pay
        nonlocal pistol_rounds
        gun_sfx = pygame.mixer.Sound(os.path.join(SFX_DIR, "BerettaM9Shot.mp3"))
        office_mission = [
            [sg.Text("You enter the office, only to find it empty. You must search the following places to find the target.")],
            [sg.Button("Under the desk"), sg.Button("Out the window"), sg.Button("Behind the filing cabinet")]
        ]

        window = sg.Window("Office Search", office_mission, no_titlebar=True)
        while True:
            office_events, values = window.read()
            if(office_events == sg.WIN_CLOSED):
                window.close()
                return "Quit"

            elif(office_events == "Under the desk"):
                window.close()
                sg.popup_no_buttons("You fail to find the target.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                sg.popup_no_buttons("Mission failed.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                return "Failure"
            elif(office_events == "Out the window"):
                window.close()
                pay += 250

                home_pwd = "Home Passcode: Eight, Two, Nine, Four."
                suicide_note = "Tell my wife I'm sorry."
                
                shifted = 21
                ciphertext = encrypt_plaintext(home_pwd, suicide_note, shifted)

                hacker_cost = 300

                suicide_message = [
                    [sg.Text("You decided to look out the window, only to find that the target has committed suicide.")],
                    [sg.Text("You look behind you and find that the target typed out a suicide note on their desktop.")],
                    [sg.Text("The note says the following:")],
                    [sg.Multiline(ciphertext, disabled=True, key='-CIPHER_MSG-')],
                    [sg.Button("Continue", bind_return_key=True), sg.Button("Copy to clipboard")]
                ]

                window = sg.Window("Suicide Window", suicide_message, no_titlebar=True, finalize=True)
                window["Continue"].set_focus()

                while True:
                    message_events, values = window.read()
                    if(message_events == "Continue"):
                        window.close()
                        office_check = sg.popup_yes_no("Do you want to head to the target's home?", no_titlebar=True)
                        if(office_check == "Yes"):
                            while True:
                                BF_hacker_options = [
                                    [sg.Text("Would you like to hire a hacker to decrypt the suicide note first?")],
                                    [sg.Text(f"The cost of the hacker service is ${hacker_cost}.")],
                                    [sg.Button("Yes", bind_return_key=True), sg.Button("No"), sg.Button("Check Status")]
                                ]

                                hack_window = sg.Window("Hack Service Window", BF_hacker_options, no_titlebar=True, finalize=True)
                                hack_window["Yes"].set_focus()

                                while True:
                                    hack_options_events, values = hack_window.read()
                                    if(hack_options_events == "Yes"):
                                        if pay - hacker_cost >= 0:
                                            pay -= hacker_cost
                                            hack_window.close()
                                            sg.popup_no_buttons(f"Transaction accepted. You now have ${pay}.", no_titlebar=True, auto_close=True, auto_close_duration=2)

                                            BF_Input = [
                                                [sg.Text("Input the encrypted suicide note for the hacker to decrypt it.")],
                                                [sg.Input(key='-CIPHER_TEXT-')],
                                                [sg.Button("Submit", bind_return_key=True)]
                                            ]

                                            bf_window = sg.Window("Brute_Force Window", BF_Input, no_titlebar=True, finalize=True)
                                            
                                            while True:
                                                bf_window_events, values = bf_window.read()
                                                ciphertext = values['-CIPHER_TEXT-']
                                                if(bf_window_events == "Submit"):
                                                    if not values['-CIPHER_TEXT-'].strip():
                                                        sg.popup_no_buttons("Input the ciphertext to continue.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                                                    else:
                                                        sg.popup_no_buttons("Decrypting the ciphertext...", no_titlebar=True, auto_close=True, auto_close_duration=3)
                                                        break
                                            bf_window.close()

                                            BruteForce(ciphertext)
                                            home_search()
                                            break

                                        else:
                                            sg.popup_no_buttons("Transaction declined. You have insufficient funds.", no_titlebar=True, auto_close=True, auto_close_duration=3)
                                            continue

                                    elif(hack_options_events == "No"):
                                        hack_window.close()
                                        home_search()
                                        break

                                    elif(hack_options_events == "Check Status"):
                                        hack_window.hide()
                                        status_window = [
                                            [sg.Frame("Status", get_status(), key='-STATUS-')]
                                        ]

                                        stat_window = sg.Window("Status", status_window, no_titlebar=True, auto_close=True, auto_close_duration=4)
                                        stat_window.read()
                                        hack_window.un_hide()

                                break

                            break
                                                
                        if(office_check == "No"):
                            break

                    elif(message_events == "Copy to clipboard"):
                        sg.popup_no_buttons("Ciphertext copied to clipboard.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                        pyperclip.copy(ciphertext)
                    
                office_pay = [
                    [sg.Text("The target died, but you failed to kill the target. You will only be paid half for this")],
                    [sg.Text(f"You now have ${pay}.")],
                    [sg.Frame("Status", get_status(), key='-STATUS-')]
                ]

                window = sg.Window("Office Pay Window", office_pay, no_titlebar=True, auto_close=True, auto_close_duration=3)
                window.read()
                window.close()
                return "Partial"
            
            elif(office_events == "Behind the filing cabinet"):
                window.close()
                gun_sfx.play()
                pistol_rounds -= 1
                sg.popup_no_buttons(f"You find the target behind the filing cabinet and kill him on the spot. You have {pistol_rounds} bullets left in your handgun.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                sg.popup_no_buttons("Mission complete.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                return "Success"
    
    def home_search():
        door_sfx2 = pygame.mixer.Sound(os.path.join(SFX_DIR, "OpenCloseDoor (updated).mp3"))
        sg.popup_no_buttons("Soon enough, you arrive at the target's home after a short drive.", no_titlebar=True, auto_close=True, auto_close_duration=2)
        door_sfx2.play()

        max_attempts = 4
        attempts = 0

        home_pwd = [
            [sg.Text("Enter the password to turn off the home security.")],
            [sg.Input(key='-HOME_PWD-')],
            [sg.Button("Submit", bind_return_key=True)]
        ]

        window = sg.Window("Security Passcode", home_pwd, no_titlebar=True, finalize=True)
        window["Submit"].set_focus()

        while True:
            home_pwd_events, values = window.read()
            sec_pcd = values['-HOME_PWD-']
            if home_pwd_events == "Submit" and sec_pcd == "8294":
                window.close()
                break
            else:
                attempts += 1
                if attempts >= max_attempts:
                    window.close()
                    home_mission_fail = [
                        [sg.Text(f"After {max_attempts} failed attempts to turn off the security system, the alarm goes off. The police arrive and you are immediately arrested.")],
                        [sg.Text("Mission failed.")]
                    ]

                    window = sg.Window("Mission Failed", home_mission_fail, no_titlebar=True, auto_close=True, auto_close_duration=3)
                    window.read()
                    sys.exit()
                
                else:
                    sg.popup_no_buttons(f"Incorrect password. You have {attempts - max_attempts} attempts remaining.", no_titlebar=True, auto_close=True, auto_close_duration=2)
        
        sg.popup_ok("You successfully enter the target's home.", no_titlebar=True)
        home_mission()
        
    def garage_mission():
        nonlocal health
        safe_code = 314025

        shotgun_sfx = pygame.mixer.Sound(os.path.join(SFX_DIR, "Shotgun Sound.mp3"))

        garage_layout = [
            [sg.Text("You decide to search around the garage for more things")],
            [sg.Text("Where do you search?")],
            [sg.Button("Trash can"), sg.Button("Car"), sg.Button("Tool Drawer")]
        ]

        window = sg.Window("Garage Layout", garage_layout, no_titlebar=True)

        while True:
            garage_layout_events, values = window.read()
            if(garage_layout_events == "Trash can"):
                window.close()
                sg.popup_no_buttons("You decided to search the trash can", no_titlebar=True, auto_close=True, auto_close_duration=2)
                sg.popup_no_buttons("Whilst your back is turned, the target's spouse approaches you with a shotgun. ", no_titlebar=True, auto_close=True, auto_close_duration=2)
                shotgun_sfx.play()
                injury_notification()

                health -= 100
                if health <= 0:
                    health = 0

                garage_death = [
                    [sg.Text("The target's spouse shot and killed you with a shotgun.")], 
                    [sg.Text("You are dead.")],
                    [sg.Frame("Status", get_status(), key='-STATUS-')],
                    [sg.Text("Mission failed.")]
                ]

                window = sg.Window("Garage Death", garage_death, no_titlebar=True, auto_close=True, auto_close_duration=3)
                window.read()
                sys.exit()
            elif(garage_layout_events == "Car"):
                window.close()
                sg.popup_no_buttons("You decide to search the target's car.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                sg.popup("You find nothing of value.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                garage_mission()
            elif(garage_layout_events == "Tool Drawer"):
                window.close()

                tool_drawer_layout = [
                    [sg.Text("You search the tool drawer and find a note with the code to the safe")],
                    [sg.Multiline(safe_code, key='-SAFE_CODE-', disabled=True)],
                    [sg.Button("Close drawer", bind_return_key=True), sg.Button("Copy to clipboard")]
                ]

                tool_window = sg.Window("Tool Window", tool_drawer_layout, no_titlebar=True, finalize=True)
                tool_window["Close drawer"].set_focus()

                while True:
                    tool_drawer_events, values = tool_window.read()
                    if(tool_drawer_events == "Close drawer"):
                        tool_window.close()
                        sg.popup_no_buttons("You take the note and close the drawer.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                        break
                    elif(tool_drawer_events == "Copy to clipboard"):
                        sg.popup_no_buttons("Text copied to clipboard", no_titlebar=True, auto_close=True, auto_close_duration=2)
                        pyperclip.copy(safe_code)
                        
                break

        sg.popup_no_buttons("You now have the password to the safe.", no_titlebar=True, auto_close=True, auto_close_duration=2)

    def home_mission():
        nonlocal health
        nonlocal pay

        shotgun_sfx2 = pygame.mixer.Sound(os.path.join(SFX_DIR, "Shotgun Sound.mp3"))

        max_safe_attempts = 3
        safe_attempts = 0

        home_layout = [
            [sg.Text("You are now in the living room of the target's home. What room will you go to?")],
            [sg.Button("Kitchen"), sg.Button("Garage"), sg.Button("Master Bedroom")],
            [sg.Button("Leave the House")]
        ]

        window = sg.Window("Home Layout", home_layout, no_titlebar=True)

        while True:
            home_layout_events, values = window.read()
            if(home_layout_events == "Kitchen"):
                health += 25
                if health >= 100:
                    health = 100

                refrigerator_search = [
                    [sg.Text("Whilst in the kitchen, you raid the fridge and eat some food.")],
                    [sg.Text("You gained some health.")],
                    [sg.Frame("Status", get_status(), key='-STATUS-')]
                ]

                refrigerator_window = sg.Window("Fridge Search", refrigerator_search, no_titlebar=True, auto_close=True, auto_close_duration=2)
                refrigerator_window.read()

            elif(home_layout_events == "Master Bedroom"):
                window.close()

                health -= 100
                if health <= 0:
                    health = 0
                
                shotgun_sfx2.play()
                
                injury_notification()

                home_invasion_death = [
                    [sg.Text("Just as you enter the master bedroom, the target's spouse blasts you in the stomach with a shotgun. You die immediately.")],
                    [sg.Text("Mission failed.")],
                    [sg.Frame("Status", get_status(), key='-STATUS-')]
                ]

                window = sg.Window("Status", home_invasion_death, no_titlebar=True, auto_close=True, auto_close_duration=4)
                window.read()
                window.close()
                sys.exit()
            elif(home_layout_events == "Garage"):
                window.close()
                safe_amount = 300

                garage_search = [
                    [sg.Text("You enter the garage and find a safe.")],
                    [sg.Button("Open the safe"), sg.Button("Continue searching garage")]
                ]

                window = sg.Window("Opening Safe", garage_search, no_titlebar=True)
                

                while True:
                    garage_events, values = window.read()
                    if(garage_events == "Continue searching garage"):
                        window.hide()
                        garage_mission()
                        window.un_hide()
                        continue
                        
                    elif(garage_events == "Open the safe"):
                        window.close()

                        safe_pwd = [
                            [sg.Text("You discover that the safe has a password.")],
                            [sg.Text("Enter the Password:"), sg.Input(key='-SAFE_PWD-')],
                            [sg.Button("Submit", bind_return_key=True), sg.Button("Cancel")]
                        ]

                        window = sg.Window("Safe Password", safe_pwd, no_titlebar=True, finalize=True)

                        while True:
                            safe_pwd_events, values = window.read()
                            safe_pcd = values['-SAFE_PWD-']

                            if safe_pwd_events =="Submit" and safe_pcd == "314025":
                                window.close()
                                sg.popup_no_buttons("Password accepted.", no_titlebar=True, auto_close=True, auto_close_duration=3)
                                break
                            elif safe_pwd_events == "Cancel":
                                continue
                            else:
                                safe_attempts += 1
                                if safe_attempts >= max_safe_attempts:
                                    sg.popup_no_buttons("You run out of attempts and an alarm sounds off.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                                    sg.popup_no_buttons("Mission failed.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                                    sys.exit()
                                else:
                                    safe_input_error = [
                                        [sg.Text("Incorrect password. Try again.")],
                                        [sg.Text(f"You have {safe_attempts} left.")]
                                    ]

                                    safe_window_error = sg.Window("Safe Window Error", safe_input_error, no_titlebar=True, auto_close=True, auto_close_duration=3)
                                    safe_window_error.read()

                        break
                break

            elif(home_layout_events == "Leave the House"):
                window.close()
                shotgun_sfx2.play()

                health -= 100
                if health <= 0:
                    health = 0

                injury_notification()

                house_death = [
                    [sg.Text("Just as you walk out the house, the target's spouse ambushes you with a shotgun blast to the chest.")],
                    [sg.Text("You are dead.")],
                    [sg.Frame("Status", get_status(), key='-STATUS-')],
                    [sg.Text("Mission failed.")]
                ]

                house_death_window = sg.Window("House Death", house_death, no_titlebar=True, auto_close=True, auto_close_duration=4)
                house_death_window.read()
                sys.exit()

        pay += 300

        safe_amount_layout = [
            [sg.Text(f"You successfully open the safe and find ${safe_amount}.")],
            [sg.Text(f"You now have ${pay}")],
            [sg.Frame("Status", get_status(), key='-STATUS-')]
        ]

        safe_window = sg.Window("Status", safe_amount_layout, no_titlebar=True, auto_close=True, auto_close_duration=3.5)
        safe_window.read()
        
    def injury_notification(message="You sustained an injury and lost some health"):
        layout4 = [
            [sg.Text(message, text_color="red")]]
        
        window = sg.Window("Injury", layout4, no_titlebar=True, auto_close=True, auto_close_duration=3, keep_on_top=True, finalize=True,)
        window.read()
        window.close()

    def tutorial():
        tutorial_layout =  [
            [sg.Text("The following below indicates your current status.")],
            [sg.Frame("Status", get_status(), key='-STATUS-')],
            [sg.Text("Press 'continue' to see what happens when you get hurt.")],
            [sg.Button("Continue", bind_return_key=True)]
        ]
    
        window = sg.Window("Status", tutorial_layout, no_titlebar=True, finalize=True)
        window["Continue"].set_focus()

        while True:
            tutorial_mission, values = window.read()
            if(tutorial_mission == "Continue"):
                window.close()
                break
        
        nonlocal health
        health -= 15
        injury_notification()
        tutorial_new_health = [
            [sg.Frame("Status", get_status(), key='-STATUS-')],
            [sg.Button("Continue", bind_return_key=True)]
        ]

        window = sg.Window("Status", tutorial_new_health, no_titlebar=True, finalize=True)
        window["Continue"].set_focus()
        while True:
            new_health_events, values = window.read()
            if(new_health_events == "Continue"):
                window.close()
                break

        heal_notice = [
            [sg.Text("As you just saw, you sustained some damage and lost some health.")],
            [sg.Text("What will you do now?")],
            [sg.Button("Heal"), sg.Button("Die")]
        ]

        window = sg.Window("Heal Window", heal_notice, no_titlebar=True, finalize=True)
        window["Heal"].set_focus()

        while True:
            heal_events, values = window.read()
            if(heal_events == "Heal"):
                health += 15
                window.close()
                new_health = [
                    [sg.Text("You are now healed.")],
                    [sg.Frame("Status", get_status(), key='-STATUS-')]
                ]

                window = sg.Window("Status", new_health, no_titlebar=True, auto_close=True, auto_close_duration=4)
                window.read()
                window.close()
                break
            elif(heal_events == "Die"):
                health -= 85
                injury_notification()
                window.close()
                death_health = [
                    [sg.Text("You are now dead.")],
                    [sg.Frame("Status", get_status(), key='-STATUS-')]
                ]

                window = sg.Window("Death Window", death_health, no_titlebar=True, auto_close=True, auto_close_duration=4)
                window.read()
                window.close()
                sys.exit()
        
        sg.popup_no_buttons("You have successfully completed the tutorial.", no_titlebar=True, auto_close=True, auto_close_duration=2)
        
    startup_window = [
        [sg.Image(os.path.join(IMAGES_DIR, "Game Logo.png"))],
        [sg.Text("WELCOME TO THE GAME!", font=("Typold Medium", 25), text_color="white")]
    ]

    window = sg.Window("Startup Window", startup_window, no_titlebar=True, modal=True, auto_close=True, auto_close_duration=4)
    window.read()

    layout1 = [
        [sg.Text("You are a hitman. Your objective is to eliminate three targets")],
        [sg.Text("Would you like to continue?")],
        [sg.Button("Yes", bind_return_key=True), sg.Button("No"), sg.Button("Office Search")]
    ]

    window = sg.Window("Objectives", layout1, no_titlebar=True, finalize=True)
    window["Yes"].set_focus()

    while True:
        objectives, values = window.read()
        if(objectives == "Yes"):
            window.close()
            break
        elif(objectives == "No"):
            window.close()
            sg.popup_no_buttons("See you!", no_titlebar=True, auto_close=True, auto_close_duration=2)
            sys.exit()
        elif(objectives == "Office Search"):
            window.close()
            office_search()
            sys.exit()

    sg.popup_no_buttons("Starting game...", no_titlebar=True, auto_close=True, auto_close_duration=2)

    game_objectives = [
        "1.) A man who regularly goes to a bar", 
        "2.) A man in an office building", 
        "3.) [REDACTED]"
    ]

    game_objectives_list = "\n".join(game_objectives)

    layout2 = [
        [sg.Text("Here are your following targets:")],
        [sg.Multiline(game_objectives_list, disabled=True, size=(40,5))],
        [sg.Button("Continue to tutorial"), sg.Button("Skip tutorial", bind_return_key=True), sg.Button("Exit")]
    ]

    window = sg.Window("Objectives", layout2, no_titlebar=True, finalize=True)
    window["Skip tutorial"].set_focus()

    while True:
        game_start_2, values = window.read()
        if(game_start_2 == "Continue to tutorial"):
            window.close()
            tutorial()
            break
        elif(game_start_2 == "Skip tutorial"):
            window.close()
            break
        elif(game_start_2 == "Exit"):
            window.close()
            sg.popup_no_buttons("See you!", no_titlebar=True, auto_close=True, auto_close_duration=3)
            sys.exit()

    sg.popup_no_buttons("Game starting...", no_titlebar=True, auto_close=True, auto_close_duration=2)
    sniper_sfx1 = pygame.mixer.Sound(os.path.join(SFX_DIR, "370332__morganpurkis__single-gunshot-2-v2 (updated).mp3"))
    door_sfx = pygame.mixer.Sound(os.path.join(SFX_DIR, "OpenCloseDoor (updated).mp3"))

    layout6 = [
        [sg.Text("Your first target is a man who goes to a bar")],
        [sg.Text("What will you do to eliminate the target?")],
        [sg.Button("1.) Snipe the target"), sg.Button("2.) Enter the bar"), sg.Button("3.) Ambush the target at their home")]
    ]

    window = sg.Window("Mission #1", layout6)

    while True:
        mission_one, values = window.read()
        if(mission_one == sg.WIN_CLOSED):
            sg.popup_no_buttons("See you!", no_titlebar=True, auto_close=True, auto_close_duration=2)
            sys.exit()
        
        elif(mission_one == "1.) Snipe the target"):
            sniper_rounds -= 1
            window.close()
            sniper_sfx1.play()
            layout7 = [
                [sg.Text(f"You opted to snipe the target. You have {sniper_rounds} sniper round left.")],
                [sg.Frame("Status", get_status(), key='-STATUS-')],
                [sg.Button("Continue")]
                ]

            window = sg.Window("Stats", layout7, no_titlebar=True)
            while True:
                new_sniper_stats, values = window.read()
                if(new_sniper_stats == "Continue"):
                    window.close()
                    break
            break

        elif(mission_one == "2.) Enter the bar"):
            window.close()
            door_sfx.play()
            pygame.mixer.music.load(os.path.join(SFX_DIR, "766655__blaastaal__murmuring-cafe.wav"))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            gun_sfx2 = pygame.mixer.Sound(os.path.join(SFX_DIR, "BerettaM9Shot.mp3"))
            layout8a = [
                [sg.Text("You enter the bar and take a seat next to the target.")],
                [sg.Text("What is your next course of action?")],
                [sg.Button("Head to the bathroom"), sg.Button("Open fire")],
            ]

            window = sg.Window("Mission #1", layout8a, no_titlebar=True)

            while True:
                bar_scene, values = window.read()
                if(bar_scene == "Head to the bathroom"):
                    window.close()
                    door_sfx.play()
                    pygame.mixer.music.stop()
                    sg.popup_no_buttons("You head to the bathroom. While there, you notice some rat poison left in the corner of the bathroom.", no_titlebar=True, auto_close=True, auto_close_duration=3)
                    sg.popup_no_buttons("You take the rat poison with you before exiting the bathroom. You then slip the poison into the target's drink.", no_titlebar=True, auto_close=True, auto_close_duration=3)
                    sg.popup_no_buttons("You sit and wait for several moments before the poison starts taking effect. The target stumbles out of the bar, taking the back door, before collapsing and dying in the alley.", no_titlebar=True, auto_close=True, auto_close_duration=3)
                    pay += 500
                    
                    secret_mission1_ending = [
                        [sg.Text("You search the target and steal some cash from their wallet.")],
                        [sg.Text(f"You now have ${pay}.")],
                        [sg.Frame("Status", get_status(), key='-STATUS-')]
                    ]

                    window = sg.Window("Money Found", secret_mission1_ending, no_titlebar=True, auto_close=True, auto_close_duration=4)
                    window.read()
                    break

                if(bar_scene == "Open fire"):
                    pistol_rounds -= 3
                    window.close()
                    pygame.mixer.music.stop()

                    for _ in range(3):
                        gun_sfx2.play()
                        time.sleep(0.30)

                    pygame.mixer.music.load(os.path.join(SFX_DIR, "435716__belthazarus__crowdpanic.mp3"))
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)

                    carcrash_sfx = pygame.mixer.Sound(os.path.join(SFX_DIR, "237375__squareal__car-crash (updated).mp3"))
                    gunfire_1 = [
                    [sg.Text(f"You draw your gun and open fire, killing the target on the spot. You have {pistol_rounds} rounds in your handgun left.")],
                    [sg.Frame("Status", get_status(), key='-STATUS-')],
                    [sg.Text("How will you escape?")],
                    [sg.Button("1.) Blend into the crowd to escape")], 
                    [sg.Button("2.) Hide in a dumpster in an alleyway")], 
                    [sg.Button("3.) Run to your car")],
                    [sg.Button("4.) Pay a driver to help you escape")]
                    ]

                    window = sg.Window("Pistol Stats", gunfire_1, no_titlebar=True)
                    while True:
                        new_pistol_stats, values = window.read()
                        if(new_pistol_stats == "1.) Blend into the crowd to escape"):
                            window.close()
                            pygame.mixer.music.stop()
                            sg.popup_no_buttons("You manage to abscond the crime scene.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                            sg.popup_no_buttons("During your escape, a police officer spots you and opens fire.", auto_close=True, no_titlebar=True, auto_close_duration=2)
                            health -= 10
                            injury_notification()

                            layout8b = [
                                [sg.Text(f"You are injured and are now at {health}% health.")],
                                [sg.Frame("Status", get_status(), key='-STATUS-')],
                                [sg.Button("Continue", bind_return_key=True)]
                            ]

                            window = sg.Window("Status Window", layout8b, no_titlebar=True, finalize=True)
                            window["Continue"].set_focus()

                            lost_health1, values = window.read()
                            if(lost_health1 == "Continue"):
                                window.close()
                                break

                        elif(new_pistol_stats == "2.) Hide in a dumpster in an alleyway"):
                            window.close()
                            pygame.mixer.music.stop()
                            sg.popup_no_buttons("You run to the alleyway in the back of the bar and hide in a dumpster.", no_titlebar=True, auto_close=True, auto_close_duration=3)
                            sg.popup_no_buttons("Once you're sure that the coast is clear, you get out of the dumpster and run away.", no_titlebar=True, auto_close=True, auto_close_duration=3)
                            break

                        elif(new_pistol_stats == "3.) Run to your car"):
                            window.close()
                            pygame.mixer.music.stop()
                            sg.popup_no_buttons("You run out the bar and toward your car before driving off.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                            carcrash_sfx.play()
                            sg.popup_no_buttons("You get into an intense car chase with police that ends with you colliding into a police car.", no_titlebar=True, auto_close=True, auto_close_duration=3)
                            health -= 100
                            if health <= 0:
                                health = 0

                            injury_notification()
                            layout8c = [
                                [sg.Text(f"You have {health}% health. You died in the car crash.")],
                                [sg.Frame("Status", get_status(), key='-STATUS-')]
                            ]
                            window = sg.Window("Death Window", layout8c, no_titlebar=True, auto_close=True, auto_close_duration=4)
                            window.read()
                            sg.popup_no_buttons("Game over...", no_titlebar=True, auto_close=True, auto_close_duration=2)
                            sys.exit()
                        
                        elif(new_pistol_stats == "4.) Pay a driver to help you escape"):
                            window.close()
                            pygame.mixer.music.stop()
                            sg.popup_no_buttons("You run out the bar and jump into a nearby taxi.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                            sg.popup_no_buttons("You bribe the taxi driver for their silence and to help you escape.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                            pay -= 500
                            layout8d = [
                                [sg.Text(f"You now have ${pay} from having paid the taxi driver.")],
                                [sg.Frame("Status", get_status(), key='-STATUS-')]
                            ]
                            window = sg.Window("Stats", layout8d, no_titlebar=True, auto_close=True, auto_close_duration=4)
                            window.read()
                            break
                    break
            break

        elif(mission_one == "3.) Ambush the target at their home"):
            window.close()
            door_sfx.play()

            home_invasion = [
                [sg.Text("You pick the lock of the front door and enter the target's home. However, you set off the security system alarm in the process. The police arrive within minutes.")],
                [sg.Text("Mission failed.")],
                [sg.Button("Retry", bind_return_key=True), sg.Button("Exit")]
            ]

            window = sg.Window("Home Invasion", home_invasion, no_titlebar=True, finalize=True)
            window["Retry"].set_focus()

            while True:
                home_invasion_events, values = window.read()
                if(home_invasion_events == "Retry"):
                    window.close()
                    restart()
                    break
                elif(home_invasion_events == "Exit"):
                    window.close()
                    sg.popup_no_buttons("See you!", no_titlebar=True, auto_close=True, auto_close_duration=2)
                    sys.exit()

    layout8e = [
        [sg.Text(f"You successfully eliminated your first target!")],
        [sg.Button("Ok")]
    ]

    window = sg.Window("Random window", layout8e, no_titlebar=True)

    while True:
        random_window, values = window.read()
        if(random_window == "Ok"):
            window.close()
            sg.popup_no_buttons("Mission complete!", no_titlebar=True, auto_close=True, auto_close_duration=2)
            pay += 500
            window.close()
            layout9 = [
                [sg.Text(f"You have ${pay} now.")],
                [sg.Frame("Status", get_status(), key='-STATUS-')],
                [sg.Button("Continue")]
            ]

            window = sg.Window("Status", layout9, no_titlebar=True)

            while True:
                mission_one_pay, values = window.read()
                if(mission_one_pay == "Continue"):
                    window.close()
                    break
            break
        
    sg.popup_no_buttons("You are ready for the second target.", no_titlebar=True, auto_close=True, auto_close_duration=2)
    sg.popup_no_buttons("Your next target is a businessman working overtime in his office, located in an office building.", no_titlebar=True, auto_close=True, auto_close_duration=2)
    sniper_sfx2 = pygame.mixer.Sound(os.path.join(SFX_DIR, "370332__morganpurkis__single-gunshot-2-v2 (updated).mp3"))
    window_shatter = pygame.mixer.Sound(os.path.join(SFX_DIR, "613879__rangoanimations__window-breaking.mp3"))
    enemy_cocking_sfx = pygame.mixer.Sound(os.path.join(SFX_DIR, "545958__cloud-10__gun-cocking-sound.mp3"))
    enemy_sfx2 = pygame.mixer.Sound(os.path.join(SFX_DIR, "717584__trp__220816-gunshot-stage-pistol-soulpepper-r-07.mp3"))

    layout10 = [
        [sg.Text("How will you eliminate the target?")],
        [sg.Button("1.) Snipe the target from across another building"), sg.Button("2.) Parachute into the office building"), sg.Button("3.) Sneak into the office building")]
    ]

    window = sg.Window("Mission #2", layout10)
    while True:
        mission2, values = window.read()
        if(mission2 == "1.) Snipe the target from across another building"):
            window.close()
            sniper_sfx2.play()
            sniper_rounds -= 1
            layout_mission2_rounds = [
                [sg.Text("You sniped the target and achieved a head shot.")],
                [sg.Frame("Status", get_status(), key='-STATUS-')],
                [sg.Text("Mission complete")]
            ]

            window = sg.Window("Mission_2_status", layout_mission2_rounds, no_titlebar=True, auto_close=True, auto_close_duration=4)
            window.read()
            window.close()
            break
        elif(mission2 == "2.) Parachute into the office building"):
            sg.popup_no_buttons("You chose to parachute into the building. However, you must pay for a helicopter pilot first.", no_titlebar=True, auto_close=True, auto_close_duration=2)
            pilot_price = 2000
            gun_sfx3 = pygame.mixer.Sound(os.path.join(SFX_DIR, "BerettaM9Shot.mp3"))
            enemy_sfx1 = pygame.mixer.Sound(os.path.join(SFX_DIR, "717584__trp__220816-gunshot-stage-pistol-soulpepper-r-07.mp3"))
            if pay - pilot_price >= 0:
                pay -= pilot_price
                window.close()
                sg.popup_no_buttons("Transaction accepted. You pay the helicopter pilot to fly you over the office building.",no_titlebar=True, auto_close=True, auto_close_duration=2)
                pygame.mixer.music.load(os.path.join(SFX_DIR, "383940__mattc90__helicopter-engine-noise-sound-effect (updated).mp3"))
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                sg.popup_no_buttons("Flying to the building...", no_titlebar=True, auto_close=True, auto_close_duration=4)
                time.sleep(4)
                pygame.mixer.music.stop()
                sg.popup_no_buttons("You enter the building through a skylight.",no_titlebar=True, auto_close=True, auto_close_duration=2)    
                window_shatter.play() 
                time.sleep(4)
                enemy_cocking_sfx.play()

                guard_encounter = [
                    [sg.Text("A guard spots you just as you've entered the building.")],
                    [sg.Button("Shoot the guard"), sg.Button("Charge the guard")],
                    [sg.Text("What will you do to neutralize the guard?")]
                ]

                window = sg.Window("Guard Encounter", guard_encounter, no_titlebar=True)    
                while True:
                    guard_events, values = window.read()
                    if(guard_events == "Shoot the guard"):
                        window.close()
                        pistol_rounds -= 3
                        enemy_health -= 25
                        health -= 15

                        for _ in range(3):
                            gun_sfx3.play()
                            time.sleep(0.30)

                        sg.popup_no_buttons(f"You shot the guard. You have {pistol_rounds} bullets left in your handgun.", no_titlebar=True, auto_close=True, auto_close_duration=2)  

                        for _ in range(2):
                            enemy_sfx1.play()
                            time.sleep(0.25)

                        injury_notification()

                        guard_health = [
                            [sg.Text("Your gunshots only wound the guard. Meanwhile, the guard returns fire.")],
                            [sg.Frame("Enemy Status", enemy_status(), key='-ENEMY_STATUS-')]
                        ]
                        window = sg.Window("Status", guard_health, no_titlebar=True, auto_close=True, auto_close_duration=4)
                        window.read()
                        window.close()

                        gun_sfx4 = pygame.mixer.Sound(os.path.join(SFX_DIR, "BerettaM9Shot.mp3"))

                        player_fight_health = [
                            [sg.Text("You suffer a considerable injury.")],
                            [sg.Frame("Status", get_status(), key='-STATUS-')],
                            [sg.Button("Return fire"), sg.Button("Charge the guard")],
                            [sg.Text("What will you do next?")]
                        ]

                        window = sg.Window("Guard Fight", player_fight_health, no_titlebar=True)
                        while True:
                            guard_fight_events, values = window.read()
                            if(guard_fight_events == "Return fire"):
                                window.close()

                                for _ in range(2):
                                    gun_sfx4.play()
                                    time.sleep(0.28)

                                pistol_rounds -= 2
                                enemy_health -= 75
                                if enemy_health <=0:
                                    enemy_health = 0
                                guard_fight_end1 = [
                                    [sg.Text(f"You managed to kill the guard. You have {pistol_rounds} bullets left in your handgun.")],
                                    [sg.Frame("Enemy Status", enemy_status(), key='-ENEMY_STATUS-')]
                                ]

                                window = sg.Window("Enemy Status", guard_fight_end1, no_titlebar=True, auto_close=True, auto_close_duration=4)
                                window.read()

                                result = office_search()
                                if result == "Quit":
                                    window.close()
                                    sys.exit()
                                if result == "Failure":
                                    window.close()
                                    sys.exit()
                                if result == "Success":
                                    window.close()
                                    sg.popup_no_buttons("You win!",no_titlebar=True, auto_close=True, auto_close_duration=2)  
                                    break
                                if result == "Partial":
                                    window.close()
                                    sg.popup_no_buttons("You partially win!", no_titlebar=True, auto_close=True, auto_close_duration=2)  
                                    break
                            elif(guard_fight_events == "Charge the guard"):
                                window.close()
                                health -= 20
                                injury_notification()
                                execution_sfx1 = pygame.mixer.Sound(os.path.join(SFX_DIR, "BerettaM9Shot.mp3"))
                                tackle_injury = [
                                    [sg.Text("The guard shoots your torso just as you tackle him to the ground.")],
                                    [sg.Frame("Status", get_status(), key='-STATUS-')],
                                    [sg.Button("Execute the Guard"), sg.Button("Pistol Whip Guard")],
                                    [sg.Text("What will you do?")]
                                ]

                                window = sg.Window("Status", tackle_injury, no_titlebar=True)
                                while True:
                                    tackle_guard_events, values = window.read()
                                    if(tackle_guard_events == "Execute the Guard"):
                                        window.close()
                                        execution_sfx1.play()
                                        pistol_rounds -= 1
                                        enemy_health -= 80
                                        if enemy_health <= 0:
                                            enemy_health = 0
                                        guard_tackle_death = [
                                            [sg.Text(f"You executed the guard. You have {pistol_rounds} bullets left in your handgun.")],
                                            [sg.Frame("Enemy Status", enemy_status(), key='-ENEMY_STATUS-')]
                                        ]

                                        window = sg.Window("Guard Death", guard_tackle_death, no_titlebar=True, auto_close=True, auto_close_duration=4)
                                        window.read()
                                        guard_tackle_end = [
                                            [sg.Text("You proceed to the target's office.")],
                                            [sg.Frame("Status", get_status(), key='-STATUS-')]
                                        ]

                                        window = sg.Window("Status", guard_tackle_end, no_titlebar=True, auto_close=True, auto_close_duration=3)
                                        window.read()
                                        result = office_search()
                                        if result == "Quit":
                                            window.close()
                                            sys.exit()
                                        if result == "Failure":
                                            window.close()
                                            sys.exit()
                                        if result == "Success":
                                            window.close()
                                            sg.popup_no_buttons("You win!",no_titlebar=True, auto_close=True, auto_close_duration=2)  
                                            break
                                        if result == "Partial":
                                            window.close()
                                            sg.popup_no_buttons("You partially win!", no_titlebar=True, auto_close=True, auto_close_duration=2)  
                                            break
                                    elif(tackle_guard_events == "Pistol Whip Guard"):
                                        window.close()
                                        enemy_health -= 30
                                        if enemy_health <=50:
                                            enemy_health = 50
                                        guard_unconscious = [
                                            [sg.Text("You knock the guard out when you pistol whip him.")],
                                            [sg.Frame("Enemy Status", enemy_status(), key='-ENEMY_STATUS-')]
                                        ]

                                        window = sg.Window("Status", guard_unconscious, no_titlebar=True, auto_close=True, auto_close_duration=3)
                                        window.read()
                                        result = office_search()
                                        if result == "Quit":
                                            window.close()
                                            sys.exit()
                                        if result == "Failure":
                                            window.close()
                                            sys.exit()
                                        if result == "Success":
                                            window.close()
                                            sg.popup_no_buttons("You win!",no_titlebar=True, auto_close=True, auto_close_duration=2)  
                                            break
                                        if result == "Partial":
                                            window.close()
                                            sg.popup_no_buttons("You partially win!", no_titlebar=True, auto_close=True, auto_close_duration=2)  
                                            break

                                break

                        break

                    elif(guard_events == "Charge the guard"):
                        window.close()
                        health -= 35
                        enemy_health -= 30
                        execution_sfx2 = pygame.mixer.Sound(os.path.join(SFX_DIR, "BerettaM9Shot.mp3"))
                        guard_fight_events2 = [
                            [sg.Text("You tackle the guard to the ground but lose some health in the process when the guard shoots your thigh.")],
                            [sg.Frame("Status", get_status(), key='-STATUS-')],
                            [sg.Frame("Enemy Status", enemy_status(), key='-ENEMY_STATUS-')],
                            [sg.Button("Execute the Guard"), sg.Button("Pistol Whip Guard")],
                            [sg.Text("What will you do next?")]
                        ]

                        window = sg.Window("Status", guard_fight_events2, no_titlebar=True)
                        while True:
                            guard_tackle_events2, values = window.read()
                            if(guard_tackle_events2 == "Execute the Guard"):
                                window.close()
                                execution_sfx2.play()
                                enemy_health -= 70
                                pistol_rounds -= 1
                                if enemy_health <=0:
                                    enemy_health = 0
                                guard_tackle_death2 = [
                                    [sg.Text(f"You draw your gun and execute the guard. You have {pistol_rounds} bullets left in your handgun.")],
                                    [sg.Frame("Enemy Status", enemy_status(), key='-ENEMY_STATUS-')]
                                ]

                                window = sg.Window("Enemy Status", guard_tackle_death2, no_titlebar=True, auto_close=True, auto_close_duration=4)
                                window.read()
                                sg.popup_no_buttons("You begin making your way to the office.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                                result = office_search()
                                if result == "Quit":
                                    window.close()
                                    sys.exit()
                                if result == "Failure":
                                    window.close()
                                    sys.exit()
                                if result == "Success":
                                    window.close()
                                    sg.popup_no_buttons("You win!",no_titlebar=True, auto_close=True, auto_close_duration=2)  
                                    break
                                if result == "Partial":
                                    window.close()
                                    sg.popup_no_buttons("You partially win!", no_titlebar=True, auto_close=True, auto_close_duration=2)  
                                    break

                            elif(guard_tackle_events2 == "Pistol Whip Guard"):
                                window.close()
                                enemy_health -= 20
                                if enemy_health <=50:
                                    enemy_health = 50
                                guard_unconscious2 = [
                                    [sg.Text("You pistol whip the guard, knocking him unconscious.")],
                                    [sg.Frame("Enemy Status", enemy_status(), key='-ENEMY_STATUS-')]
                                ]

                                window = sg.Window("Enemy Status", guard_unconscious2, no_titlebar=True, auto_close=True, auto_close_duration=4)
                                window.read()
                                sg.popup_no_buttons("You begin making your way to the target's office.", no_titlebar=True, auto_close=True, auto_close_duration=2)
                                result = office_search()
                                if result == "Quit":
                                    window.close()
                                    sys.exit()
                                if result == "Failure":
                                    window.close()
                                    sys.exit()
                                if result == "Success":
                                    window.close()
                                    sg.popup_no_buttons("You win!",no_titlebar=True, auto_close=True, auto_close_duration=2)  
                                    break
                                if result == "Partial":
                                    window.close()
                                    sg.popup_no_buttons("You partially win!", no_titlebar=True, auto_close=True, auto_close_duration=2)  
                                    break

                        break
                        
                break   
                
            else:
                sg.popup_ok(f"Transaction declined. You do not have sufficient funds.\n\n"
                            f"Current Balance: ${pay}\n"
                            f"Helicopter Pilot Service: ${pilot_price}",
                            title="Transaction Declined", no_titlebar=True, keep_on_top=True
                )
                continue

        elif(mission2 == "3.) Sneak into the office building"):
            window.close()
            sg.popup_no_buttons("You attempt to sneak into the building to eliminate the target.", no_titlebar=True, auto_close=True, auto_close_duration=2)
            sg.popup_no_buttons("A security guard spots you and shoots you on the spot.", no_titlebar=True, auto_close=True, auto_close_duration=2)

            for _ in range(2):
                enemy_sfx2.play()
                time.sleep(0.25)

            health -= 100
            if health <= 0:
                health = 0
            
            injury_notification()
            mission2_death = [
                [sg.Text("You have died. Mission failed.")],
                [sg.Frame("Status", get_status(), key='-STATUS-')]
            ]

            window = sg.Window("Death Window", mission2_death, no_titlebar=True, auto_close=True, auto_close_duration=4)
            window.read()
            window.close()
            sys.exit()
        elif(mission2 == sg.WIN_CLOSED):
            sg.popup_no_buttons("See you!", no_titlebar=True, auto_close=True, auto_close_duration=2)
            sys.exit()

    sg.popup_no_buttons("You successfully eliminated the second target.", no_titlebar=True, auto_close=True, auto_close_duration=2)
    sg.popup_no_buttons("You are ready for the final target.", no_titlebar=True, auto_close=True, auto_close_duration=2)

main()