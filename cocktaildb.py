import requests
import json
from string import ascii_lowercase as INITIALS

import sys
import os

#OS CHECK
os_ = sys.platform
if os_ == "win32":
    pass
else:
    print("#@#LINUX DETECTED, CORRECT FUNCTIONING OF THIS PROGRAM IS NOT GUARANTEED (TESTED FOR WINDOWS ONLY)#@#")

#COLOR FOR COMMAND PROMPT
class Colors:
    def r():
        os.system("color 4")
    def b():
        os.system("color 3")
    def y():
        os.system("color E")


c = Colors

def logo():
    LOGO = """
   _____                  _      _             _   _   _____    ____  
  / ____|                | |    | |           (_) | | |  __ \  |  _ \ 
 | |        ___     ___  | | __ | |_    __ _   _  | | | |  | | | |_) |
 | |       / _ \   / __| | |/ / | __|  / _` | | | | | | |  | | |  _ < 
 | |____  | (_) | | (__  |   <  | |_  | (_| | | | | | | |__| | | |_) |
  \_____|  \___/   \___| |_|\_\  \__|  \__,_| |_| |_| |_____/  |____/                                                                                                                                           
"""
    print(LOGO)
    
HELP = """[INTRO]
-h OR --help: Show this menu.

[COCKTAIL DATABASE]
--search: Search cocktail by name.
--random: Returns information for a random cocktail!
--searchby INITIAL: Returns a list of cocktails starting by a letter (example: --searchby a)
"""

LOGO = r"""
()   ()      ()    /
  ()      ()  ()  /
   ______________/___
   \            /   /  Pythonic
    \^^^^^^^^^^/^^^/
     \     ___/   /
      \   (   )  /  
       \  (___) /        Cocktails...
        \ /    /        
         \    /
          \  /
           \/
           ||
           ||
           ||
           ||
           ||
           /\
          /;;\
     ==============
"""

#Functions for each api request and information choice
def search_cocktail(name:str, random:bool = False) -> str:
    if not random:
        URL = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}"
    else:
        URL = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
        
    try:
        req = requests.get(URL)
        content = json.loads(req.text)

        #Access stuff
        content = content["drinks"]
    except Exception as ex:
        c.r()
        return print(f"\nUh Oh, something was done wrong!\nDetails: {ex}")

    #print(content)

    #Access every dictionary in list and gather values
    for c,element in enumerate(content,start=1):
        print(f"\n\n===COCKTAIL VARIATION {c}===\n" if len(content) > 1 else "")
        #strIngredients and strMeasures
        ing = [f"strIngredient{x}" for x in range(1, 21)]
        msr = [f"strMeasure{x}" for x in range(1, 21)]
        ingredients = []
        measures = []

        #Get all possible existing ingredients in a range from 1 to 20
        for n in ing:
            try:
                current_ingredient = element[n]
                ingredients.append(current_ingredient)
            except:
                continue
        for n in msr:
            try:
                current_measure = element[n]
                measures.append(current_measure)
            except:
                continue
            
        #Remove NoneType values
        ingredients = list(filter(lambda x: x is not None, ingredients))
        measures = list(filter(lambda x: x is not None, measures))

        #Assign number on each elemnt
        for i in range(len(measures)):
            measures[i] = f"[{str(i+1)}] {measures[i]}" #Assign the number i that takes the value of each list's index and format it to the ingredients name (weird to explain)

        m_i = list(zip(measures,ingredients))
        
        #Get info
        name = element["strDrink"]
        category = element["strCategory"]
        glass:str = element["strGlass"]
        alcohol: str = ["Yes" if element["strAlcoholic"] == "Alcoholic" else "No"]
        instructions: str = element["strInstructions"]
        
        #PRINTING
        print(f"#Cocktail name: {name.title()}")
        print(f"#Category: {category}")
        print(f"#Glass: {glass}")
        print(f"#Alcoholic: {alcohol[0]}")
        print("\n###INGREDIENTS###")
        for x in m_i:
            print(f"{x[0]}-> {x[1]}")
        print(f"\n###INSTRUCTIONS###\n{instructions}")
    

#Search by initial
def search_by_initial(initial:str) -> str:
    URL = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={initial}"

    try:
        req = requests.get(URL)
        content = json.loads(req.text)

        #Access stuff
        content = content["drinks"]
    except Exception as ex:
        c.r()
        return print(f"\nUh Oh, something was done wrong!\nDetails: {ex}")

    #Get list of values for key -> "strDrink" from json
    drinks = [dic["strDrink"] for dic in content]

    print(f"Found {len(drinks)} cocktails!\n")
    for count, cocktail in enumerate(drinks,start=1):
        print(f"[{count}] {cocktail}")
    
def main():
    if len(sys.argv) == 2:
        
        #Commands here
        cmd = sys.argv[1]

        match cmd:

            #COMMANDS MENU
            case "-h":
                print(HELP)
                return

            case "--help":
                print(HELP)
                return

            #Search for cocktail by name
            case "--search":
                #Question and "left-blank" check
                while True:
                    n = input("Enter a cocktail to seach: ")

                    if not n:
                        c.y()
                        print("\nYou can't leave this field empty!\n")
                        continue
                    break

                c.b()
                
                search_cocktail(n)
                return

            case "--random":
                search_cocktail("",True)
                return

            case _:
                c.r()
                print("This command does nothing!\n".upper())
                return
            
    #EXAMPLE: cocktaildb.py --command 3rd_argument
    elif len(sys.argv) == 3:
        cmd1 = sys.argv[1]
        cmd2 = sys.argv[2]

        #Get list of cocktails by initial ^_^
        if cmd1 == "--searchby" and cmd2:
            cmd2 = cmd2.lower()

            #Error handling
            if not cmd2 in INITIALS:
                c.r()
                print("\nPlease enter a valid letter! (Example: \"a\")\n")
                return

            search_by_initial(cmd2)
            return


        

    #No command given
    else:
        c.y()
        print("Type --help or -h for a list of commands!\n")
        return

if __name__ == "__main__":
    #DEFAULT COLOR and clear screen
    if os_ == "linux":
        os.system("clear")
    else:
        os.system("cls")
    c.b()
    
    NAME = sys.argv[0].split("\\")[-1]
    logo()
    print(f"WELCOME TO {NAME.upper()}!\nAPI: https://www.thecocktaildb.com/api.php\n")
    
    main()
    print("\n" + LOGO)
