from typing import List
import requests
from api import User

def api_url(route: str):
    return f"http://localhost:8000/{route}"
# definierar en route, datatyp = string. Med Url

def print_menu():
    print(
        """
    1: Create A User 
    2: Get All Users
    3: Get A User
    4: Update User
    5: Delete User
    6: Create dummy data
    7: Close Program
    """
    )
    pass
## då uppgiften vill ha 2 GET, 2 POST, 1 PUT och 1 DELETE
# Post
# get
# get
# update (put)
# delete
# post
#  close

def create_user():
    print("Create User: ")
    fName = input("First Name: ") # inputen tilldelas till variablen FName
    lName = input("Last Name: ")
    age = input("Age: ")
    gender = input("Gender: ")
    title = input("Title: ")
    new_user = User(first_name=fName, last_name=lName, age=age, gender=gender, title=title)
    # ovan, skapas en ny användare med inmatade (inputs) värden
    response = requests.post(api_url("api/createUser"), json=new_user.dict())
    # ovan skicakr vi en pOST förfrågan till API:et för att skapa en användare med JSON-data vi 
    # # skickade med i koden innan (med alla inputs som sparades i new_user)
    print(response)
    
def create_dummy_data():
    print("creating dummy data")
    response = requests.post(api_url("api/seedData"))
    # POST request till endpoint "api/seedData" (med library 'requests')
    ## som sparas i en ny variabel 'responde'
    return print(response.json())
    # returnerar datan från servern i JSON format, printar ut det, 
 ##### NOTERA, att werbläsare enbart kan 'hämta' GET, inte resperande
 # vi kan dock gå in på vanliga http://localhost:8000/api/users och se att dummy datan nu finns där   
    
def get_users():
    users = []
    print("Here is a list of all our users")
    response = requests.get(api_url("api/users"))
    ## GET request skickas till API:et, med URL för att hämta alla användare. 
    # svaret lagras i 'resonse' variabeln
    if not response.status_code == 200:
        return
    # om vi INTE får status 200, (200= OK) så avslutas funktionen
    
    data = response.json() # hämtar lagrade datan i 'response' och konverterar till JSON format
    for user in data: # varje användare loopas igenom
        user = User(**user) # JSON-datan konvereras till User objekt
        print("_________")
        print(f"ID: {user.id}")
        print(f"First Name: {user.first_name}")
        print(f"Last Name: {user.last_name}")
        print(f"Age: {user.age}")
        print(f"Gender: {user.gender}")
        print(f"Title: {user.title}")
        users.append(user) # append för att lägga till användaren i listan för samtliga användare
    return users

def get_user():
    print("Here is the info of the users you are looking for")
    user_id = input("What is the id of the user? ")
    response = requests.get(api_url(f"api/user/{user_id}"))
    # ovan, skickar en GET-förfrågan till en viss URL (som skapats av api_url funktionen) som innehåller användarens ID.
    if not response.status_code == 200:
        return
    
    data = print(f"Here is your user: {response.json()}")
    # Skriver ut informationen om användaren som returneras från API:et.
    return print(data)
    # Variabeln 'data' innehåller inte data, utan en sträng med informationen.



def update_user(users: List[User]): # tar in en lista av användare
    user_to_update = input("Id of User you wish to update: ")
    
    if not str.isdigit(user_to_update):
        print("Ids are integers")
        return
    # OM användaren inte skickar ett heltal (INT) som id, --> flemeddelande och funktionen avslutas
    
    index = None
    for i, user in enumerate(users):
        print(user.id)
        
        if user.id == int(user_to_update):
            index = i
            break

    if index == None:
        print("No such user")
        return
    ## loopar igenom listan av användare och kollar om användaresn id finns.
    # om det finns så sparas index för den användaren, 
    # om INTE, så avslutas funktionen
    
    user = users[index]

    fName = input("First Name (leave blank if same): ")
    lName = input("Last Name (leave blank if same): ")
    age = input("Age (leave blank if same): ")
    gender = input("Gender (leave blank if same): ")
    title = input("Title (leave blank if same): ")
    # användare från listan sparas med index. Samtliga frågor i form av
    # 'variabler/ chracteristics' efterfrågas och läggs till i repsektive variabler.

    if not fName:
        fName = user.first_name
    if not lName:
        lName = user.last_name
    if not age:
        age = user.age
    if not gender:
        gender = user.gender
    if not title:
        title = user.title
    # om de nya värdena från tidigare kod(rader) är tomma, så
    # sparas de befinliga/ tidigare värdena
    
    new_user = User(first_name=fName, last_name=lName, age=age, gender=gender, title=title)
    response = requests.put(api_url(f"api/updateUser/{user_to_update}"), json=new_user.dict())
    print(response.json())
    # Skapar en ny 'User' instans med de nya uppdaterade värdena vi 'lagt in'.
    # PUT anropas på API:et och upptaderar användarinstansen. Slutligen printas API responsen.
    
    
def delete_user():
    print("Delete User")
    user_to_delete = input("Id of User you wish to delete: ")
    if not str.isdigit(user_to_delete): # kollar om inputen är INTEGER
        print("Ids are integers") # felmeddelande om input =/= INT
        return # isf avslutas funktionen
    response = requests.delete(api_url(f"delete_user/{user_to_delete}"))
    # Skickar en delete-förfrågan till API med URL till användaren som ska raderas
    print(response.json())
    # Skriver ut API: svar i JSON-format

def main():
    print_menu() # skirver ut huvudmenyn 
    choice = input("Please choose your action: ")
    choice = choice.strip()
    if not str.isdigit(choice):
        print("Please enter a valid option")
        return
    ## om input inte är iNT, avslutas funktionen
    
    match int(choice): # match, mathcar inputen med respektive användares id
        case 1:
            create_user() # lägger till användare
        case 2:
            users = get_users() # hämtar en lista över alla användare
        case 3:
            get_user() # hämtar info om en specifik användare
        case 4:
            users = get_users()
            update_user(users) # uppdaterar info en en användare
        case 5:
            delete_user() # tar bort en användare
        case 6: 
            create_dummy_data() # skapar testdata för användare
        case 7:
            exit() # avslutar programmet
        case _:
            print("Please enter a valid choice") #ifall input inte matchar med något av 'cases'


while __name__ == "__main__":
    main() # startar huvudprogrammet