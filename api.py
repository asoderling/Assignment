from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import json

from db import DB

class User(BaseModel): 
    id: int = None
    first_name: str
    last_name: str
    age: int
    gender: str
    title: str

app = FastAPI()

db = DB("users.db")

app.curr_id = 1
app.userdata: List[User] = []
## två variabler skapas. Sen sista skapar en tom lista av användare


@app.get("/")
def root(): 
    return "Hello, Api is up and running. Please check: http://localhost:8000/docs"
## en route med roten"/". localhost:8000


################################# GET ROUTES
@app.get("/api/users") #  definierar en HTTP GET-request hanterare för endpoint "/api/users"
def get_users(): #funktionen för GET anropet till "/api/users"
    get_users = """
    SELECT * FROM users
    """
    # SQL query som hämtar all information från tabellen "users"
    
    data = db.call_db(get_users) # utför SQL-queryn genom att använda databas-objektet "db" och lagrar resultatet i "data"
    users = [] # skapar en tom lista
    for user in data: # loopar igenom varje rad i "data"
        id, first_name, last_name, age, gender, title = user #packar upp datan i varje rad till separata variabler
        users.append(User(id=id,first_name=first_name,last_name=last_name, age=age, gender=gender, title=title))
        #  skapar en User-objekt för varje rad och lägger till objektet till "users"-listan
        print(data)
    return users
#### Sammanfattat: en route där vi hämtar alla användare. En loop som går igenom, och hämtar, samtliga "objekt/användare" som finns.


@app.get("/api/user/{id}")
def get_user(id: int):
    insert_query = """
    SELECT * FROM users WHERE id = ?
    """
    data = db.call_db(insert_query, id)
    return data
##samma som ovan, ej loop då vi vill ha en specifik användare baserat på id.


################################# POST ROUTES
@app.post("/api/createUser")
def create_user(user: User):
    insert_query = """
    INSERT INTO users (first_name, last_name, age, gender, title)
    VALUES ( ?, ?, ?, ?, ? )
    """
    db.call_db(insert_query, user.first_name, user.last_name, user.age, user.gender, user.title)

    return "User has been created!"
# här skapas en route där vi skapar en ny användare och lägger till den.


@app.post("/api/seedData") # POST request med endpoint: "/api/seedData"
def create_dummy_data(): # funktion som exekveras när request skickas till ovan endpoint
    seed_data = """
        INSERT INTO users (
        first_name,
        last_name,
        age,
        gender,
        title 
        ) VALUES (
        ?, ?, ?, ?, ?
        )
        """
    # lägger till data i users-tabellen i databasen. "?" är placeholders som ersätts med data(variabler) i en for-loop
        
    with open("seed.json", "r") as seed:
        data = json.load(seed)
    ## öppnar en JSON fil med dummydata (seed data) och läser innehållet i varabeln "data"
            
    for user in data: #itererar över varje objekt i listan "data", där varje objekt har nedanstående "variabler"
        db.call_db(seed_data, user["first_name"], user["last_name"],user["age"],user["gender"],user["title"])
        # Använder "db.call_db()" för att köra SQL-queryn "seed_data" för att lägga till en användare i users-tabellen. 
        # För varje iteration av for-loopen, läggs användarens data till i queryn som argument.
        
    return "dummy data has been created"
### vår andra "POST", där vi lägger till dummy data.


################################# UPDATE ROUTE
@app.put("/api/updateUser/{id}") # skapar en PUT request route till /api/updateUser/{id}
def update_user(id: int, updatedUser: User):
# definierar en funktion (update_user), som tar två parametrar: "id" (int) & updatedUser (User)    
    update_user_query = """
    UPDATE users
    SET first_name = ?, last_name = ?, age = ?, gender = ?, title = ?
    WHERE id = ?
    """
    # definierar en sträng som innehåller en SQL fråga, som ska uptadera användardata med ett visst id.

    db.call_db(update_user_query, 
               updatedUser.first_name,
               updatedUser.last_name,
               updatedUser.age,
               updatedUser.gender,
               updatedUser.title, id)
    # anropar funktionen "call_db" i "db" objektet och skickar "update_user_query" stängen 
    # och värden från "updatedUser" och "id" som parametrar. 
    # detta uppdaterar användardata för en användare med ett visst ID i databasen.
    
    return "User has now been updated"
### vi updaterar en befintlig användare, baserat på användarens id. 


################################# DELETE ROUTE
@app.delete("/delete_user/{id}")
def delete_todo(id: int):
    delete_query = """
    DELETE FROM users WHERE id = ?
    """
    db.call_db(delete_query, id)
    # app.todos = list(filter(lambda todo: todo.id != id, app.todos))
    return "User has been deleted!"
# vi tar bort en användare baserat på id.


# ## vi tar bort alla användare 



#
