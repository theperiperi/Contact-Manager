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
    
    return (jsonify({"message":"Contact created"}),201,)

@app.route("/update_contact/<int:user_id>",methods=["PUT"])
def update_contact(user_id):
    contact=Contact.query.filter_by(id=user_id)

    if not contact:
        return jsonify({"message":"Contact not found"}),404
    
    data=request.json
    #if first name exists in the data, update the contact's first name, else keep what u have
    contact.first_name=data.get("firstName",contact.first_name)
    contact.last_name=data.get("lastName",contact.last_name)
    contact.email=data.get("email",contact.email)

    db.session.commit()
    return (jsonify({"message":"Contact updated"}),200)

@app.route("/delete_contact/<int:user_id>",methods=["DELETE"])
def delete_contact(user_id):
    contact=Contact.query.filter_by(id=user_id)

    if not contact:
        return jsonify({"message":"Contact not found"}),404
    
    db.session.delete(contact)
    db.session.commit()

    return (jsonify({"message":"Contact deleted"}),200)

#only if you run the file directly do this, if import don't execute
if __name__=="__main__":
    with app.app_context():
        #creates the database tables, if it doesn't exist
        db.create_all()

    app.run(debug=True)
