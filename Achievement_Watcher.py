## Oszust OS Achievement Watcher - Oszust Industries
## Created on: 7-16-21 - Last update: 6-02-24
## Achievement Notifications Library v1.5.1 - Oszust Industries
softwareVersion = "v1.0.0.002"
def clear(): return ("\n" * 70)
from datetime import datetime, timedelta
import AutoUpdater
import os
import json
import pathlib
import pickle

def softwareConfig():
## System Configures
    global appBuild, deactivateFileOpening, enableAccountSystem, enableAchievementThreading, exitSystem, overrideResetAchivements, resetSettings, systemName
    systemName, exitSystem = "Oszust OS Achievement Watcher", False
## Change Configures
    appBuild = "Dev"                 ## The build the app is running (Beta, Main)
    resetSettings = False             ## Reset account's settings on login
    deactivateFileOpening = False     ## Stops the program from reading/writing on files on PC
    enableAccountSystem = True        ## Enables the account system allowing multiple accounts
    pass

def softwareSetup():
## Setup Software
    global accountReady, restartNeed
    print("Loading...")
    accountReady = False
## Start Functions
    softwareConfig()
    print(clear() + "Welcome to Oszust OS Achievement Watcher. " + softwareVersion[:-4] + "\nCreated and published by Oszust Industries\n\n\nOszust Industries Login System:\n\n")
    accountLogin("setup")
    if exitSystem == False: startMenu("")

def crashMessage():
## Display Crash
    global Argument
    import webbrowser
    webbrowser.open("https://github.com/Oszust-Industries/" + systemName.replace(" ", "-"),  new = 2, autoraise = True)
    print(clear() + "Crash Log:\n" + ("-" * 50 + "\n") + str(Argument) + ("\n" + "-" * 50) + "\n")
    crash = input(systemName + " has crashed. Please report your crash to the issues tab in GitHub.\n\nPress enter to restart " + systemName + "...\n")
    if crash not in ["exit()", "exit", "quit"]:
        try: softwareSetup()
        except Exception as Argument: crashMessage()
    else: exit()

def accountLogin(accountAction):
## Save User Settings
    from random import randrange
    import math
    import shutil
    global account2Way, accountActiveOwnedDLC, accountEmail, accountInput, accountLanguage, accountOwnedDLC, accountPassword, availableAccounts, availablePossibleAnswers, currentAccountInfoPath, currentAccountPath, currentAccountUsername, deactivateFileOpening, emailCode, emailExpireTime, emailconfirmed, enableAccountSystem, exitSystem, expiredCodes, gameHintsActivated, lockDateTime, packedAccountGames, packedAccountInformation, packedSettings, passwordAttemptsLeft, punishmentMode, resetAchievements, smartWordDetector, startedCreateAccount, tempAvailableAccounts, win10ToastActive
    weakPasswords, badUsernames = ["1234", "password", "forgot password", "forgotpassword", "default", "incorrect", "back", "quit", "return", "logout"], ["disneyhockey40", "guest", "password", "forgot password", "forgotpassword", "default", "incorrect", "logout", ""]
## Account Setup
    if accountAction == "setup":
        lockDateTime, expiredCodes, emailconfirmed, passwordAttemptsLeft, currentAccountUsername = "", [], False, 5, ""
        if os.name != "nt": deactivateFileOpening = True ## Windows Detector
        accountLogin("createUserPath")
        if deactivateFileOpening == False:
            try:
                availableAccounts = pickle.load(open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Available Account.p"), "rb"))
                availableAccounts.sort()
            except OSError: availableAccounts = []
        else: availableAccounts, enableAccountSystem = [], False
        if enableAccountSystem == False:
            currentAccountUsername = "Default"
            if deactivateFileOpening == False: 
                currentAccountInfoPath = str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername)
                currentAccountPath = (currentAccountInfoPath + "\\" + systemName)
            else: currentAccountInfoPath, currentAccountPath = "", ""
            try: packedAccountGames = pickle.load(open(currentAccountInfoPath + "\\accountGames.p", "rb"))
            except OSError: accountLogin("createUserPath")
            accountLogin("readSettings")
            return
        tempAvailableAccounts = availableAccounts
        if "Default" in availableAccounts: tempAvailableAccounts = availableAccounts.remove("Default")
        else: tempAvailableAccounts = availableAccounts
        if len(tempAvailableAccounts) > 0:
            print("Available Accounts:")
            for i in tempAvailableAccounts: print(str(tempAvailableAccounts.index(i) + 1) + ". " + i)
        else: print("No Available Accounts.")
        print("\n" + str(len(tempAvailableAccounts) + 1) + ". Add account\n" + str(len(tempAvailableAccounts) + 2) + ". Login as guest")
        if len(tempAvailableAccounts) > 0: print(str(len(tempAvailableAccounts) + 3) + ". Remove account\n" + str(len(tempAvailableAccounts) + 4) + ". Quit")
        else: print(str(len(tempAvailableAccounts) + 3) + ". Quit")
        accountInput = input("\nType the account number to login. ").replace(" ", "")
        if accountInput.lower() in ["create", "add"] or (accountInput.isnumeric() and int(accountInput) == len(tempAvailableAccounts) + 1):
            print(clear())
            startedCreateAccount = False
            accountLogin("createAccount_1")
        elif accountInput.lower() in ["guest"] or (accountInput.isnumeric() and int(accountInput) == len(tempAvailableAccounts) + 2):
            print("\n\nLoading Account...")
            deactivateFileOpening, win10ToastActive, currentAccountUsername = True, False, "Guest"
            accountLogin("readOwnedDLC")
            print(clear())
        elif accountInput.lower() in ["delete", "remove"] or (accountInput.isnumeric() and int(accountInput) == len(tempAvailableAccounts) + 3 and len(tempAvailableAccounts) > 0):
            print(clear())
            accountLogin("deleteAccount")
        elif accountInput.isnumeric() or accountInput in availableAccounts:
            if accountInput.isdigit() == False:
                currentAccountUsername = accountInput
                currentAccountInfoPath = str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername)
                currentAccountPath = (currentAccountInfoPath + "\\" + systemName), (currentAccountInfoPath + "\\" + systemName)
                accountLogin("readSettings")
            elif (int(accountInput) == len(tempAvailableAccounts) + 3 and len(tempAvailableAccounts) <= 0) or (int(accountInput) == len(tempAvailableAccounts) + 4 and len(tempAvailableAccounts) > 0): accountLogin("quit")
            elif (int(accountInput) < len(tempAvailableAccounts) + 1 and int(accountInput) > 0):
                currentAccountUsername = availableAccounts[int(accountInput) - 1]
                currentAccountInfoPath = str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername)
                currentAccountPath = (currentAccountInfoPath + "\\" + systemName)
                accountLogin("readSettings")
            else:
                print(clear() + "You typed an unavailable account number.\n\n\n")
                accountLogin("setup")
        elif accountInput in ["quit", "exit"]: accountLogin("quit")
        else:
            print(clear() + "You typed an unavailable account number.\n\n\n")
            accountLogin("setup")
        return
## Account Logout
    elif accountAction == "logout":
        if exitSystem == False:
            exitSystem = True
            print("\n\n\nDo not close application.\nSaving and logging out...\n")
            softwareSetup()
## Account Quit
    elif accountAction == "quit":
        print("\n\n\nDo not close application.\nSaving and exiting...\n")
        exitSystem = True
## Email
    elif "emailAccount" in accountAction:
        print(clear() + "This account has 2 factor verification enabled. We are unable to securely send a code. Please try again in a little bit.\n\n\n")
        accountLogin("setup")
        return
## Create Account
    elif "createAccount" in accountAction:
        createAccountStep = int(accountAction.replace("createAccount_", ""))
        if createAccountStep == 1:
            if startedCreateAccount == False: print("Create Account:\n\nType 'back' to return to the previous prompt.\nType 'cancel' to cancel create account.")
            currentAccountUsername = input(str("\n\n\nA username is your name that you will select when logging into the server.\n\nWhat username would you like for your account? "))
            startedCreateAccount = True
            if currentAccountUsername.lower() in ["cancel", "quit", "exit", "back", "return"]: softwareSetup()
            elif currentAccountUsername not in availableAccounts and currentAccountUsername.lower().replace(" ", "") not in badUsernames: accountLogin("createAccount_2")
            elif currentAccountUsername in availableAccounts:
                print("\nThis username is already in use.")
                accountLogin("createAccount_1")
            else:
                print("\nThis username is unavailable.")
                accountLogin("createAccount_1")
        elif createAccountStep == 2:
            accountPassword, accountLanguage = "", "english"
            accountLogin("createAccount_3")
        elif createAccountStep == 3:
            accountEmail = input(str("\n\n\n\nAn email is required strictly for when you forget your password or a verification code needs to be sent.\n\nWhat email would you like to use for your account? ")).lower().replace(" ", "")
            if accountEmail in ["cancel", "quit", "exit"]: softwareSetup()
            elif accountEmail in ["back", "return"]: accountLogin("createAccount_1")
            elif "@" in accountEmail and "." in accountEmail: accountLogin("createAccount_4")
            else:
                print("\nThis email is not a valid email.")
                accountLogin("createAccount_3")
        elif createAccountStep == 4:
            if accountPassword == "": accountInput = input(str("\n\n\n\nA password will add more security to your account. The password will be required whenever an account action needs to take place.\n\nWould you like a password on your account? (yes/no) ")).replace(" ", "")
            else: accountInput = "yes"
            if accountInput.lower() in ["cancel", "quit", "exit"]: softwareSetup()
            elif accountInput.lower() in ["back", "return"]: accountLogin("createAccount_3")
            elif accountInput.lower() in ["y", "yes"]:
                accountLogin("createAccount_5")
            elif accountInput.lower() in ["n", "no"]:
                accountPassword = "none"
                accountLogin("createAccount_6")
            else:
                print("\nPlease type yes or no.")
                accountLogin("createAccount_4")
        elif createAccountStep == 5:
            accountPassword = input(str("\nWhat password would you like for your account? "))
            if accountPassword.lower() in ["cancel", "quit", "exit"]: softwareSetup()
            elif accountPassword.lower() in ["back", "return"]:
                accountPassword = ""
                accountLogin("createAccount_4")
            elif len(accountPassword) < 5:
                print("\n\n\nYour password needs to be at least five characters long.")
                accountLogin("createAccount_5")
            elif accountPassword.lower() in weakPasswords:
                print("\n\n\nYour password is too weak. Create a more unique password.")
                accountLogin("createAccount_5")
            else: accountLogin("createAccount_6")
        elif createAccountStep == 6:
            if accountPassword == "": print("\n\n\n\n2 factor verification will add more security to your account. This will be used whenever an account action needs to take place.")
            elif accountPassword != "": print("\n\n\n\n2 factor verification will add even more security to your account. This will be used with your password whenever an account action needs to take place.")
            accountInput = input(str("\n2 factor verification will email you a code to type in when it is required.\n\nWould you like 2 factor verification on your account? (yes/no) ")).replace(" ", "")
            if accountInput.lower() in ["cancel", "quit", "exit"]: softwareSetup()
            elif accountInput.lower() in ["back", "return"]:
                accountPassword = ""
                accountLogin("createAccount_4")
            elif accountInput.lower() in ["y", "yes"]:
                account2Way = "active"
                accountLogin("createAccount_7")
            elif accountInput.lower() in ["n", "no"]:
                account2Way = "none"
                accountLogin("createAccount_7")
            else:
                print("\nPlease type yes or no.")
                accountLogin("createAccount_6")
        elif createAccountStep == 7:
            print("\n\n\n\n\n" + ("-" * 50) + "\nAccount Confirmation:" + "\n\n\nAccount username: " + currentAccountUsername + "\nAccount language: " + accountLanguage + "\nAccount email: " + accountEmail)
            if accountPassword != "none": print("Account password: Active")
            else: print("Account password: Inactive")
            if account2Way != "none": print("Account 2 factor verification: Active")
            else: print("Account 2 factor verification: Inactive")
            accountInput = input(str("\nDo these account details look right? (yes/no) ")).replace(" ", "")
            if accountInput.lower() in ["back", "return"]: accountLogin("createAccount_6")
            elif accountInput.lower() in ["y", "yes"]:
                availableAccounts.append(currentAccountUsername)
                pickle.dump(availableAccounts, open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Available Account.p"), "wb"))
                packedAccountInformation = [currentAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way, lockDateTime]
                print(clear())
                accountLogin("createUserPath")
            elif accountInput.lower() in ["n", "no"]:
                print(clear())
                accountLogin("createAccount_1")
            else:
                print("\nPlease type yes or no.")
                accountLogin("createAccount_7")
        return
## Create Account Path
    elif accountAction == "createUserPath":
        if deactivateFileOpening == False:
            if currentAccountUsername != "": print("\n\nCreating Account...")
            try: pickle.load(open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Available Account.p"), "rb"))
            except OSError:
                try:
                    pathlib.Path(os.path.join(os.getenv('APPDATA'), "Oszust Industries", "Accounts")).mkdir(parents=True, exist_ok=True) ## Create cache folder in appdata
                    pickle.dump([], open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Available Account.p"), "wb"))
                except OSError:
                    shutil.rmtree(str(os.getenv('APPDATA') + "\\Oszust Industries"))
                    accountLogin("createUserPath")
            if currentAccountUsername != "":
                try:
                    currentAccountInfoPath = str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername)
                    os.mkdir(currentAccountInfoPath)
                except OSError: pass
                try:
                    currentAccountPath = str(currentAccountInfoPath + "\\" + systemName)
                    os.mkdir(currentAccountPath)
                except OSError: pass
                if currentAccountUsername.lower() == "default": packedAccountInformation = ["Default", "english", "Default", "none", "none", lockDateTime]
                pickle.dump(packedAccountInformation, open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
                print(clear())
        if currentAccountUsername != "": accountLogin("readSettings")
        return
## Delete Account
    elif accountAction == "deleteAccount":
        if currentAccountUsername == "":
            print("Delete Account:\n")
            for i in availableAccounts:
                if i != "Default": print(str(availableAccounts.index(i) + 1) + ". " + i)
            accountInput = input("\nType the account number to delete the account. ").replace(" ", "")
            if accountInput.isnumeric() or accountInput in availableAccounts:
                if accountInput.isdigit() == False:
                    currentAccountUsername = accountInput
                    currentAccountPath = str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername + "\\" + systemName)
                elif (int(accountInput) < len(tempAvailableAccounts) + 1 and int(accountInput) > 0):
                    currentAccountUsername = availableAccounts[int(accountInput) - 1]
                    currentAccountPath = str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername + "\\" + systemName)
                else: print(clear() + "You typed an unavailable account number.\n\n\n")
                accountLogin("deleteAccount")
            elif accountInput.lower() in ["cancel", "quit", "exit", "back", "return"] and accountReady == True: settingsMenu("", False)
            elif accountInput.lower() in ["cancel", "quit", "exit", "back", "return"] and accountReady == False: softwareSetup()
            else:
                print(clear() + "You typed an unavailable account number.\n\n\n")
                accountLogin("deleteAccount")
        else:
            accountLogin("readSettings")
            if exitSystem == True: return
            accountInput = input("Delete Account:\n\nAre you sure you would like to permanently delete " + currentAccountUsername + "'s account from all your games? (yes/no) ").replace(" ", "")
            if accountInput.lower() in ["y", "yes"]: accountLogin("deleteAccountForever")
            elif accountInput.lower() in ["cancel", "quit", "exit", "back", "return"] and accountReady == True: settingsMenu("", False)
            elif accountInput.lower() in ["cancel", "quit", "exit", "back", "return"] and accountReady == False: softwareSetup()
            elif accountInput.lower() in ["n", "no"] and accountReady == True: settingsMenu("", False)
            elif accountInput.lower() in ["n", "no"] and accountReady == False: softwareSetup()
            else: accountLogin("deleteAccount")
        return
## Delete Account Forever
    elif accountAction == "deleteAccountForever":
        if deactivateFileOpening == False:
            print("Deleting Account...")
            try: shutil.rmtree(str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername))
            except: pass
            if currentAccountUsername.lower() != "default": availableAccounts.remove(currentAccountUsername)
            pickle.dump(availableAccounts, open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Available Account.p"), "wb"))
            print(clear())
            print(currentAccountUsername + "'s account has been deleted.\n\n\n")
            currentAccountUsername = ""
            accountLogin("setup")
        else:
            print(clear() + "Deleting your account is not possible.\n\n\n")
            currentAccountUsername = ""
            accountLogin("setup")
        return
## Rename Account
    elif accountAction == "renameAccount":
        newAccountUsername = input(str("\nRename Account:\n\nWhat would you like to rename " + currentAccountUsername + "'s account to? "))
        if newAccountUsername.lower() in ["cancel", "quit", "exit", "back", "return"] and accountReady == True:
            print(clear())
            accountLogin("setup")
        elif newAccountUsername.lower() in ["cancel", "quit", "exit", "back", "return"] and accountReady == False: softwareSetup()
        elif newAccountUsername not in availableAccounts and newAccountUsername.lower() not in badUsernames:
                availableAccounts.remove(currentAccountUsername)
                availableAccounts.append(newAccountUsername)
                pickle.dump(availableAccounts, open(str(os.getenv('APPDATA') + "\\Oszust Industries\\Available Account.p"), "wb"))
                currentAccountUsername, packedAccountInformation = newAccountUsername, [newAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way, lockDateTime]
                pickle.dump(packedAccountInformation, open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
                try: accountOwnedDLC = pickle.load(open(currentAccountPath + "\\accountOwnedDLC.p", "rb"))
                except OSError: pickle.dump([currentAccountUsername], open(currentAccountPath + "\\accountOwnedDLC.p", "wb"))
                accountOwnedDLC[0] = currentAccountUsername
                pickle.dump(accountOwnedDLC, open(currentAccountPath + "\\accountOwnedDLC.p", "wb"))
                os.rename(currentAccountInfoPath, str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername))
                softwareSetup()
        elif newAccountUsername in availableAccounts:
            print("\nThis username is already in use.\n\n\n")
            accountLogin("renameAccount")
        else:
            print("\nThis username is unavailable.\n\n\n")
            accountLogin("renameAccount")
        return
## Change Password
    elif accountAction == "changeAccountPassword":
        if emailconfirmed == False: print(clear() + "Change Account Password:")
        if accountPassword == "none":
            print("\n\n1.Add password")
            accountInput = input(str("\nType the number of the action for " + currentAccountUsername + "'s password: ")).replace(" ", "")
            if accountInput == "1":
                accountPassword = input(str("\nWhat password would you like for your account? "))
                pickle.dump([currentAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way, lockDateTime], open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
                print("\n\nThe password has been added to your account.")
            elif accountInput.lower() in ["cancel", "quit", "exit", "back", "return"] and accountReady == True: settingsMenu("", False)
            elif accountInput.lower() in ["cancel", "quit", "exit", "back", "return"] and accountReady == False: softwareSetup()
            else:
                print(clear() + "Please type one of the following actions.\n\n\n")
                accountLogin("changeAccountPassword")
        else:
            if emailconfirmed == False:
                accountInput = input(str("\nType your email to confirm your identity: ")).lower().replace(" ", "")
                if accountInput == accountEmail:
                    emailCode = randrange(100000, 999999)
                    accountLogin("emailAccount_resetPasswordCode")
                    accountInput = input(str("\nA code has been sent to your email to manage your password. Type the code here: ")).replace(" ", "")
                elif accountInput in ["cancel", "quit", "exit", "back", "return"] and accountReady == True:
                    settingsMenu("", False)
                    return
                elif accountInput in ["cancel", "quit", "exit", "back", "return"] and accountReady == False:
                    softwareSetup()
                    return
                else:
                    print(clear() + "Email doesn't match " + currentAccountUsername + "'s email.\n\n\n")
                    accountLogin("setup")
            if emailconfirmed == True or (accountInput == str(emailCode) and datetime.now() < emailExpireTime):
                emailconfirmed = True
                print(clear() + "Change Account Password:\n\n1.Change password\n2.Remove password")
                accountInput = input(str("\nType the number of the action for " + currentAccountUsername + "'s password: ")).replace(" ", "")
                if accountInput == "1":
                    accountPassword = input(str("\nWhat new password would you like for your account? "))
                    if len(accountPassword) < 5:
                        print(clear() + "Change Account Password:\n\nYour password needs to be at least five characters long.")
                        accountLogin("changeAccountPassword")
                    elif accountPassword.lower() in weakPasswords:
                        print(clear() + "Change Account Password:\n\nYour password is too weak. Create a more unique password.")
                        accountLogin("changeAccountPassword")
                    else:
                        pickle.dump([currentAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way, lockDateTime], open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
                        print(clear() + "The password has been changed on your account.\n\n")
                        accountLogin("setup")
                elif accountInput == "2":
                    pickle.dump([currentAccountUsername, accountLanguage, accountEmail, "none", account2Way, lockDateTime], open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
                    print(clear() + "The password has been removed from your account.\n\n")
                    accountLogin("readSettings")
                elif accountInput.lower() in ["cancel", "quit", "exit", "back", "return"] and accountReady == True: settingsMenu("", False)
                elif accountInput.lower() in ["cancel", "quit", "exit", "back", "return"] and accountReady == False: softwareSetup()
                else:
                    print(clear() + "Change Account Password:\n\nPlease type one of the following actions.\n")
                    accountLogin("changeAccountPassword")
            elif accountInput.lower() in ["cancel", "quit", "exit", "back", "return"] and accountReady == True: settingsMenu("", False)
            elif accountInput.lower() in ["cancel", "quit", "exit", "back", "return"] and accountReady == False: softwareSetup()
            elif (accountInput == str(emailCode) and datetime.now() >= emailExpireTime) or int(accountInput) in expiredCodes:
                print("\n\nThis code has expired. A new code has been sent to your email.")
                expiredCodes, emailCode = expiredCodes.append(account2Way), randrange(100000, 999999)
                accountLogin("changeAccountPassword")
            else:
                print(clear() + "Incorrect verification code.\n\n\n")
                accountLogin("setup")
        return
## Corrupt Account
    elif accountAction == "corruptAccount":
        accountInput = input(str(clear() + "Corrupt Account:\n\n\n" + currentAccountUsername + "'s account is unreadable.\n\nWould you like to delete " + currentAccountUsername + "'s account? (yes/no) ")).lower().replace(" ", "")
        if accountInput in ["y", "yes"]: accountLogin("deleteAccountForever")
        elif accountInput in ["n", "no"]: softwareSetup()
        else:
            print(clear())
            accountLogin("corruptAccount")
        return
## Find Account Games
    elif accountAction == "accountGames":
        if os.path.isdir(currentAccountInfoPath) == False and deactivateFileOpening == False: accountLogin("corruptAccount")
        elif deactivateFileOpening == False:
            try: packedAccountGames = pickle.load(open(currentAccountInfoPath + "\\accountGames.p", "rb"))
            except OSError: packedAccountGames = []
            if systemName not in packedAccountGames:
                try:
                    currentAccountPath = str(currentAccountInfoPath + "\\" + systemName)
                    os.mkdir(currentAccountPath)
                except OSError: pass
                packedAccountGames.append(systemName)
            pickle.dump(packedAccountGames, open(currentAccountInfoPath + "\\accountGames.p", "wb"))
        return
## Read Game Settings
    elif accountAction == "readSettings":
        if currentAccountUsername != "Default": print("\n\nLoading Account...")
        if deactivateFileOpening == False:
            currentAccountInfoPath = str(os.getenv('APPDATA') + "\\Oszust Industries\\Accounts\\" + currentAccountUsername)
            currentAccountPath = (currentAccountInfoPath + "\\" + systemName)
        else: currentAccountInfoPath, currentAccountPath = "", ""
        accountLogin("accountGames")
        if deactivateFileOpening == False:
            try: packedAccountInformation = pickle.load(open(currentAccountInfoPath + "\\accountInformation.p", "rb"))
            except OSError: packedAccountInformation = ["N/A"]
            if resetSettings == True: packedSettings = [True, False]
            else:
                try: packedSettings = pickle.load(open(currentAccountPath + "\\settingsSave.p", "rb"))
                except OSError: packedSettings = [True, False]
        else: packedAccountInformation, packedSettings = ["N/A"], [True, False]
        if "N/A" not in packedAccountInformation: currentAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way, lockDateTime = packedAccountInformation[0], packedAccountInformation[1], packedAccountInformation[2], packedAccountInformation[3], packedAccountInformation[4], packedAccountInformation[5]
        elif deactivateFileOpening == False:
            accountLogin("corruptAccount")
            return
        elif deactivateFileOpening == True: accountPassword, account2Way = "none", "none"
        if lockDateTime != "" and datetime.now() < lockDateTime:
            timeLeftInLock = int(math.ceil((lockDateTime - datetime.now()).seconds / 60))
            if timeLeftInLock <= 1: print(clear() + "This account is still locked for " + str(timeLeftInLock) + " more minute.\n\n\n")
            else: print(clear() + "This account is still locked for " + str(timeLeftInLock) + " more minutes.\n\n\n")
            accountLogin("setup")
            return
        if accountPassword == "none" and account2Way == "none": print(clear())
        elif passwordAttemptsLeft <= 0:
            print(clear() + "Incorrect password.\nThe account has been locked for 5 minute.\n\n\n")
            lockDateTime = datetime.now() + timedelta(minutes=5)
            pickle.dump([currentAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way, lockDateTime], open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
            accountLogin("setup")
            return
        elif accountPassword != "none":
            accountInput = input(str("\n\n\nType 'forgot password' if you have forgotten your password.\n\nThis account has a password. What is your account password? "))
            if accountInput.lower() == "forgot password":
                accountLogin("changeAccountPassword")
                return
            elif accountInput == accountPassword: print(clear())
            elif accountInput.lower() in ["back", "quit", "return", "logout"]:
                softwareSetup()
                return
            else:
                print(clear() + "Incorrect password.\n\n\n")
                passwordAttemptsLeft -= 1
                accountLogin("readSettings")
        if deactivateFileOpening == False and account2Way != "none":
            import socket
            try:
                sock = socket.create_connection(("www.google.com", 80))
                if sock is not None:
                    sock.close
                    pass
            except OSError: account2Way = "unavailable"
        if account2Way not in ["none", "unavailable"]:
            account2Way = randrange(100000, 999999)
            accountLogin("emailAccount_verificationCode")
            accountInput = input(str("\nThis account has 2 factor verification enabled. An email has been sent with the code. Type the code here: ")).replace(" ", "")
            if accountInput == str(account2Way) and datetime.now() < emailExpireTime: clear()
            elif accountInput.lower() in ["back", "quit", "return", "logout"]:
                softwareSetup()
                return
            elif (accountInput == str(account2Way) and datetime.now() >= emailExpireTime) or int(accountInput) in expiredCodes:
                print(clear() + "This code has expired. A new code has been sent to your email.")
                expiredCodes.append(account2Way)
                accountLogin("readSettings")
            else:
                print(clear() + "Incorrect verification code.\nThe account has been locked for 1 minute.\n\n\n")
                pickle.dump([currentAccountUsername, accountLanguage, accountEmail, accountPassword, account2Way, (datetime.now() + timedelta(minutes=1))], open(currentAccountInfoPath + "\\accountInformation.p", "wb"))
                accountLogin("setup")
        elif account2Way == "unavailable":
            print(clear() + "This account has 2 factor verification enabled. We are unable to securely send a code. Please try again in a little bit.\n\n\n")
            accountLogin("setup")
        if len(packedSettings) >= 1: win10ToastActive = packedSettings[0]
        else: win10ToastActive = True
        if len(packedSettings) >= 2: resetAchievements = packedSettings[1]
        else: resetAchievements = False
        accountLogin("saveSettings")
        accountLogin("readOwnedDLC")
        return
## Save Settings
    elif accountAction == "saveSettings": pass
## Read Owned DLC
    elif accountAction == "readOwnedDLC": pass

def startMenu(menuOption):
## Achievement Watcher Start Menu
    if menuOption == "Access" and currentAccountUsername == "Guest": print(systemName + " doesn't allow guest to view achievements.\n\n\n")
    elif menuOption == "Access": print(systemName + " requires deactivateFileOpening to be set to False.\n\n\n")
    if menuOption == "" or menuOption == "Access": print("Welcome to " + systemName + ". " + softwareVersion[:-4] + "\nCreated and published by Oszust Industries\n\n\n")
    if deactivateFileOpening == False: print("1 - Game Library\n2 - Achievement Watcher Help\n3 - Account Settings")
    elif currentAccountUsername == "Guest": print("1 - Guest accounts can't view achievements\n2 - Achievement Watcher Help\n3 - Account Settings")
    else: print("1 - deactivateFileOpening must be set to False\n2 - Achievement Watcher Help\n3 - Account Settings")
    if (deactivateFileOpening == True or enableAccountSystem == False) and currentAccountUsername != "Guest": print("4 - Quit Software")
    else: print("4 - Logout of Account\n5 - Quit Software")
    if (deactivateFileOpening == True or enableAccountSystem == False) and currentAccountUsername != "Guest": menuOption = input(str("\nType a number. (1/2/3/4) ")).replace(" ", "")
    else: menuOption = input(str("\nType a number. (1/2/3/4/5) ")).replace(" ", "")
    if menuOption.lower() in ["1", "start", "games", "library"]:
        print(clear())
        displayAccountGames("")
    elif menuOption.lower() in ["2", "help", "tips"]:
        print(clear() + "Achievement Watcher Help:\n\nThe Game Library will show you your owned games and the completion percentage.\nType the number of the game you would like, and it will show you the game's achievements.\n\nYou can find the number of earned achievements and the number of total achievements."
            "\nIt will also show you the number of each type of achievement you have.\nNext, your most recently earned achievement will be displayed.\nFinally, All of the game's achievements will be shown.\n\nThe Achievements will show if locked or earned and the achievement's name."
            "\nMost achievements will show a description, but some locked achievements will have a hidden description.\nThe bottom of the list will show achievements from the game's DLCs.\n\n\n")
        startMenu("")
    elif menuOption.lower() in ["3", "settings"]: settingsMenu("", False)
    elif menuOption.lower() in ["4", "logout", "back"] and (deactivateFileOpening == False or currentAccountUsername == "Guest") and enableAccountSystem == True: accountLogin("logout")
    elif menuOption.lower() in ["4", "quit", "exit"] and (deactivateFileOpening == True or enableAccountSystem == False): accountLogin("quit")
    elif menuOption.lower() in ["5", "quit", "exit"] and (deactivateFileOpening == False or currentAccountUsername == "Guest") and enableAccountSystem == True: accountLogin("quit")
    else:
        print(clear())
        if (deactivateFileOpening == True or enableAccountSystem == False) and currentAccountUsername != "Guest": print("\n\nPlease type a number. (1/2/3/4)\n\n\n")
        else: menuOption = print("\n\nPlease type a number. (1/2/3/4/5)\n\n\n")
        startMenu("")

def settingsMenu(settingsChange, showSettingsError):
## Settings Menu
    if settingsChange == "":
        if showSettingsError == True: print(clear() + "Please type one of the following options.\n\n")
        print(clear() + "Settings Menu:\n\nType the number of the setting to change.\nType 'save' to return to the menu.")
        if deactivateFileOpening == False: print("\n\nAccount Settings:\n1. Rename Account\n2. Manage Account Password\n3. Delete Account")
        else: print("\n\nAccount settings can't be changed while deactivateFileOpening is set to True.")
        settingsChange = input(str("\nWhat setting would you like to change? ")).lower().replace(" ", "")
    if settingsChange in ["done", "back", "mainmenu", "menu", "save", "game", "exit"]:
        accountLogin("saveSettings")
        print(clear())
        startMenu("")
    elif settingsChange in ["1", "rename"] and deactivateFileOpening == False: accountLogin("renameAccount")
    elif settingsChange in ["2", "password"] and deactivateFileOpening == False: accountLogin("changeAccountPassword")
    elif settingsChange in ["3", "delete"] and deactivateFileOpening == False:
        accountLogin("deleteAccount")
        return
    else: settingsMenu("", True)

def displayAccountGames(selectedGame):
    ## Account Games Setup
    global goodPackedAccountGames
    goodPackedAccountGames = []
    if selectedGame == "error": print("You must run the game once on your account.\n\n\n\n" + currentAccountUsername + "'s Game Library:\n\n")
    if deactivateFileOpening == False:
        try: packedAccountGames = pickle.load(open(currentAccountInfoPath + "\\accountGames.p", "rb"))
        except OSError:
            startMenu("Access")
            return
        for i in packedAccountGames:
            if "Oszust OS" not in i and i != "Achievement Notifications Library": goodPackedAccountGames.append(i)
    else:
        startMenu("Access")
        return
## Display Game Library
    if selectedGame != "error": print("Run the game once on your account for it to be here.\n\n" + currentAccountUsername + "'s Game Library:\n\n")
    if len(goodPackedAccountGames) == 0: print("No owned games.")
    else:
        for i in goodPackedAccountGames: print(str(goodPackedAccountGames.index(i) + 1) + ". " + i)
    if selectedGame in ["", "error"]:
        print("\n\nType 'menu' to return to the main menu.\n")
        if len(goodPackedAccountGames) > 1: menuOption = input(str("Type a game number. (1-" + str(len(goodPackedAccountGames)) + ") ")).replace(" ", "")
        elif len(goodPackedAccountGames) == 1: menuOption = input(str("Type a game number. (1) ")).replace(" ", "")
        else: menuOption = input("Type menu. (menu) ").replace(" ", "")
    if menuOption.lower() in ["m", "menu", "back", "exit", "return", "quit"]:
        print(clear())
        startMenu("")
    elif menuOption.isnumeric() and (int(menuOption) < len(goodPackedAccountGames) + 1 and int(menuOption) > 0): achievementDisplaySystem(menuOption)
    else:
        print(clear() + "Type the game's number to see the achievements.\n\n\n")
        displayAccountGames("")

def achievementDisplaySystem(selectedGame):
    ## Show Hangman Achievements
    global achievementTotal, availableAchievements, earnedBronze, earnedGold, earnedPlatinum, earnedSilver, gameAchievementProgressSave, gameAchievementSave, percentComplete
    achievementTotal = 1
    print(clear())
    if deactivateFileOpening == False:
        try:
            gameAchievementSave = pickle.load(open(currentAccountInfoPath + "\\" + goodPackedAccountGames[int(selectedGame) - 1] + "\\achievementSave.p", "rb"))
            gameAchievementProgressSave = pickle.load(open(currentAccountInfoPath + "\\" + goodPackedAccountGames[int(selectedGame) - 1] + "\\achievementProgressTracker.p", "rb"))
            AchievementFile = open(currentAccountInfoPath + "\\" + goodPackedAccountGames[int(selectedGame) - 1] + "\\Achievements.json",)
            data = json.load(AchievementFile)
        except OSError:
            displayAccountGames("error")
            return
    else:
        displayAccountGames("error")
        return
    if len(gameAchievementSave) > 0:
        achievementVersion = gameAchievementSave[0]
        if "v" not in achievementVersion:
            if ("v1" not in str(achievementVersion)) and (len(gameAchievementSave) >= 7) and ("Achievement" not in str(gameAchievementSave[6])): achievementVersion = "v1.2.0"
            elif str(achievementVersion) == "0" or str(achievementVersion) == str(availableAchievements): achievementVersion = "v1.1.0"
            elif "v1" not in str(achievementVersion): achievementVersion = "v1.0.0"
    else: achievementVersion = "v1.0.0"
    if achievementVersion not in ["v1.0.0", "v1.1.0", "v1.2.0"]:
        earnedBronze, earnedSilver, earnedGold, earnedPlatinum, availableAchievements = gameAchievementSave[4], gameAchievementSave[5], gameAchievementSave[6], gameAchievementSave[7], gameAchievementSave[3]
        totalEarned = int(earnedBronze) + int(earnedSilver) + int(earnedGold) + int(earnedPlatinum)
        gamePlaytime = float(gameAchievementSave[2]) / 60
        if gamePlaytime == 1: gamePlaytime = str(float(round(gamePlaytime, 2))) + " Minute"
        elif gamePlaytime < 60: gamePlaytime = str(float(round(gamePlaytime, 2))) + " Minutes"
        elif gamePlaytime == 60: gamePlaytime = str(float(round(gamePlaytime / 60, 1))) + " Hour"
        elif gamePlaytime > 60: gamePlaytime = str(float(round(gamePlaytime / 60, 1))) + " Hours"
        lastDate = gameAchievementSave[1]
    elif achievementVersion not in ["v1.0.0"]:
        earnedBronze, earnedSilver, earnedGold, earnedPlatinum, availableAchievements = gameAchievementSave[1], gameAchievementSave[2], gameAchievementSave[3], gameAchievementSave[4], gameAchievementSave[0]
        totalEarned = int(earnedBronze) + int(earnedSilver) + int(earnedGold) + int(earnedPlatinum)
    if achievementVersion not in ["v1.0.0"]:
        if availableAchievements == 0 or totalEarned == 0: print(goodPackedAccountGames[int(selectedGame) - 1] + " - 0%")
        else:
            percentComplete = float(round(float(totalEarned) / float(availableAchievements) * 100, 2))
            print(goodPackedAccountGames[int(selectedGame) - 1] + " - " + str(percentComplete) + "%")
        print("Game Playtime: " + str(gamePlaytime))
        todayDate = datetime.today()
        if todayDate.strftime("%m/%d/%y") == lastDate: print("Date Last Played: Today")
        elif((todayDate - timedelta(days=1)).strftime("%m/%d/%y")) == lastDate: print("Date Last Played: Yesterday")
        else: print("Date Last Played: " + str(lastDate))
    else: print(goodPackedAccountGames[int(selectedGame) - 1])
    print("\nAchievement Version: " + str(achievementVersion) + ("\n" + "-" * 30))
    if achievementVersion not in ["v1.0.0"]:
        print("\nEarned: " + str(totalEarned) + " out of " + str(availableAchievements) + " Achievements")
        if int(earnedBronze) != 1: print("\n" + str(earnedBronze) + " - Bronze Achievements")
        else: print("\n" + str(earnedBronze) + " - Bronze Achievement")
        if int(earnedSilver) != 1: print(str(earnedSilver) + " - Silver Achievements")
        else: print(str(earnedSilver) + " - Silver Achievement")
        if int(earnedGold) != 1: print(str(earnedGold) + " - Gold Achievements")
        else: print(str(earnedGold) + " - Gold Achievement")
        if int(earnedPlatinum) != 1: print(str(earnedPlatinum) + " - Platinum Achievements")
        else: print(str(earnedPlatinum) + " - Platinum Achievement")
    if achievementVersion not in ["v1.0.0", "v1.1.0", "v1.2.0"] and len(gameAchievementSave) > 8: print("-" * 50 + "\nMost Recent Achievement Earned:\n\n" + data[gameAchievementSave[len(gameAchievementSave) - 2]][0]["Name"] + " | Level - " + data[gameAchievementSave[len(gameAchievementSave) - 2]][0]["Level"] + "\nTime Earned: " + str(gameAchievementSave[gameAchievementSave.index(gameAchievementSave[len(gameAchievementSave) - 1])]) + "\n\n" + data[gameAchievementSave[len(gameAchievementSave) - 2]][0]["Description"] + "\n")
    elif achievementVersion in ["v1.1.0", "v1.2.0"] and len(gameAchievementSave) > 5: print("-" * 50 + "\nMost Recent Achievement Earned:\n\n" + data[gameAchievementSave[len(gameAchievementSave) - 2]][0]["Name"] + " | Level - " + data[gameAchievementSave[len(gameAchievementSave) - 2]][0]["Level"] + "\nTime Earned: " + str(gameAchievementSave[gameAchievementSave.index(gameAchievementSave[len(gameAchievementSave) - 1])]) + "\n\n" + data[gameAchievementSave[len(gameAchievementSave) - 2]][0]["Description"] + "\n")
    elif achievementVersion in ["v1.0.0"] and len(gameAchievementSave) > 0: print("-" * 50 + "\nMost Recent Achievement Earned:\n\n" + data[gameAchievementSave[len(gameAchievementSave) - 2]][0]["Name"] + " | Level - " + data[gameAchievementSave[len(gameAchievementSave) - 2]][0]["Level"] + "\n\n" + data[gameAchievementSave[len(gameAchievementSave) - 2]][0]["Description"] + "\n")
    for i in data:
        print("-" * 80)
        if data[i][0]["DLC"] != "Base": print("DLC - " + data[i][0]["DLC"] + ":")
        else: print("")
        if i in gameAchievementSave:
            if data[i][0]["Description"] == "PlatinumTrophy": print("Earned  -  " + data[i][0]["Name"])
            else: print(str(achievementTotal) + ". Earned  -  " + data[i][0]["Name"])
            if achievementVersion not in ["v1.0.0", "v1.1.0"]: print("Time Earned: " + str(gameAchievementSave[gameAchievementSave.index(i) + 1]))
        elif data[i][0]["Description"] == "PlatinumTrophy": print("Locked  -  " + data[i][0]["Name"])
        else: print(str(achievementTotal) + ". Locked  -  " + data[i][0]["Name"])
        if data[i][0]["Name"] in gameAchievementSave: print("Time Earned: N/A")
        if data[i][0]["AchievementProgressTracker"] != "None" and i not in gameAchievementSave:
            progressPercent10 = int(round(gameAchievementProgressSave[data[i][0]["AchievementProgressTracker"] - 1] / gameAchievementProgressSave[data[i][0]["AchievementProgressTracker"]] * 10, 0))
            progressPercent100 = int(round(gameAchievementProgressSave[data[i][0]["AchievementProgressTracker"] - 1] / gameAchievementProgressSave[data[i][0]["AchievementProgressTracker"]] * 100, 0))
            print("\nProgress: [" + ("=" * progressPercent10) + (" " * int(10 - progressPercent10)) + "]          " + str(progressPercent100) + "%")
        if data[i][0]["Description"] != "PlatinumTrophy":
            if data[i][0]["Hidden"] == False or i in gameAchievementSave: print("\n" + data[i][0]["Description"] + "\n")
            else: print("\nHidden\n")
        elif achievementVersion not in ["v1.0.0"]: print("\nGet all " + str(int(availableAchievements) - 1) + " achievements in " + goodPackedAccountGames[int(selectedGame) - 1] + ".\n")
        else: print("\nGet all achievements in " + goodPackedAccountGames[int(selectedGame) - 1] + ".\n")
        if achievementVersion not in ["v1.0.0"]:
            if data[i][0]["Level"] == "Bronze": print("Level - Bronze    |  Rarity - " + data[i][0]["Rarity"] + "\n")
            elif data[i][0]["Level"] == "Silver": print("Level - Silver    |  Rarity - " + data[i][0]["Rarity"] + "\n")
            elif data[i][0]["Level"] == "Gold": print("Level - Gold      |  Rarity - " + data[i][0]["Rarity"] + "\n")
            elif data[i][0]["Level"] == "Platinum": print("Level - Platinum  |  Rarity - " + data[i][0]["Rarity"] + "\n")
        if data[i][0]["Description"] != "PlatinumTrophy": achievementTotal += 1
    AchievementFile.close()
    menuOption = input(str("-" * 100 + "\nType 'menu' to return to the menu. \nType 'refresh' to refresh earned achievements.\n\nWhat option would you like to perform. ")).replace(" ", "")
    if menuOption.lower() in ["m", "back", "exit", "return", "quit", "menu"]:
        print(clear())
        startMenu("")
    elif menuOption.lower() in ["r", "refresh", "restart"]: achievementDisplaySystem(selectedGame)
    else: achievementDisplaySystem(selectedGame)


## Start System
try: softwareSetup()
except Exception as Argument: crashMessage()