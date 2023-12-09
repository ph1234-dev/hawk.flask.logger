# you need to import app instance found index 
# instead of the app intsance found in the confi
from config import db
from index import app

if __name__ == "__main__":
    db.create_all()
    app.run()   
