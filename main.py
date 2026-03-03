from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Contact

app = FastAPI()

@app.post("/identify")
def identify(payload: dict, db: Session = Depends(get_db)):

    req_email = payload.get("email")
    req_phone = payload.get("phone")

    # step 1: check for old records that match email or phone
    found = db.query(Contact).filter(
        (Contact.email == req_email) |
        (Contact.phone == req_phone)
    ).all()

    # step 2: if nothing found, make a new primary record
    if len(found) == 0:
        new_main = Contact(
            email=req_email,
            phone=req_phone,
            linkedId=None,
            linkPrecedence="primary"
        )
        db.add(new_main)
        db.commit()
        db.refresh(new_main)

        return {
            "contact": {
                "primaryContactId": new_main.id,
                "emails": [new_main.email] if new_main.email else [],
                "phoneNumbers": [new_main.phone] if new_main.phone else [],
                "secondaryContactIds": []
            }
        }

    # step 3: choose the smallest id record as primary
    primary_row = found[0]
    for item in found:
        if item.id < primary_row.id:
            primary_row = item

    # step 4: check if request brings new data
    email_ok = any(item.email == req_email for item in found)
    phone_ok = any(item.phone == req_phone for item in found)

    need_secondary = not (email_ok and phone_ok)

    # step 5: if we have more than one primary, fix them
    primary_list = [item for item in found if item.linkPrecedence == "primary"]

    if len(primary_list) > 1:
        real_main = primary_list[0]
        for item in primary_list:
            if item.id < real_main.id:
                real_main = item

        # update the other primary items to secondary
        for item in primary_list:
            if item.id != real_main.id:
                item.linkPrecedence = "secondary"
                item.linkedId = real_main.id
                db.commit()
                db.refresh(item)

        primary_row = real_main

    # step 6: make new secondary if new info came
    if need_secondary:
        new_sec = Contact(
            email=req_email,
            phone=req_phone,
            linkedId=primary_row.id,
            linkPrecedence="secondary"
        )
        db.add(new_sec)
        db.commit()
        db.refresh(new_sec)
        found.append(new_sec)

    # step 7: build the output lists
    email_list = list({item.email for item in found if item.email})
    phone_list = list({item.phone for item in found if item.phone})
    sec_ids = [item.id for item in found if item.linkPrecedence == "secondary"]

    return {
        "contact": {
            "primaryContactId": primary_row.id,
            "emails": email_list,
            "phoneNumbers": phone_list,
            "secondaryContactIds": sec_ids
        }
    }