from flask import request, jsonify
from config import app,db
from models import Contact


@app.route("/contacts",methods=["GET"])
def get_contacts():
    contacts=Contact.query.all()
    json_contacts=list(map(lambda x:x.to_json(),contacts))
    return jsonify(json_contacts)

@app.route("/create_contact",methods=["POST"])
def create_contact():
    first_name=request.json.get("firstName")
    last_name=request.json.get("lastName")
    email=request.json.get("email")

    if not first_name or not last_name or not email:
        return (jsonify({"message":"Oops you're missing some fields"}),400,)

    new_contact=Contact(first_name=first_name,last_name=last_name,email=email) 
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return (jsonify({"message":str(e)}),500,)

#only if you run the file directly do this, if import don't execute
if __name__=="__main__":
    with app.app_context():
        #creates the database tables, if it doesn't exist
        db.create_all()

    app.run(debug=True)
