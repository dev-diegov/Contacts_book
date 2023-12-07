from db import connect
from models import Contact, BelongsTo

def selectContacts(user_id, field, order):
    """
    Retrieve a list of contacts for a given user, sorted based on specified field and order.

    Parameters:
    - user_id (int): The unique identifier for the user.
    - field (str): The field by which contacts should be sorted ('ID' or 'NAME').
    - order (str): The order in which contacts should be sorted ('ASC' for ascending, 'DESC' for descending).

    Returns:
    - contacts (list): A list of Contact objects sorted according to the specified field and order.
    """
    try:
        session = connect()

        if field == 'ID' and order == 'ASC':
            contacts = session.query(Contact).join(BelongsTo, Contact.id == BelongsTo.contact_id).filter(BelongsTo.user_app_id == user_id).order_by(Contact.id).all()
        elif field == 'ID' and order == 'DESC':
            contacts = session.query(Contact).join(BelongsTo, Contact.id == BelongsTo.contact_id).filter(BelongsTo.user_app_id == user_id).order_by(Contact.id.desc()).all()
        elif field == 'NAME' and order == 'ASC':
            contacts = session.query(Contact).join(BelongsTo, Contact.id == BelongsTo.contact_id).filter(BelongsTo.user_app_id == user_id).order_by(Contact.name).all()
        elif field == 'NAME' and order == 'DESC':
            contacts = session.query(Contact).join(BelongsTo, Contact.id == BelongsTo.contact_id).filter(BelongsTo.user_app_id == user_id).order_by(Contact.name.desc()).all()
    except Exception as e:
        print(e)
    finally:
        session.close()

    return contacts

def selectContact(contact_id):
    """
    Retrieve a specific contact based on the provided contact ID.

    Parameters:
    - contact_id (int): The unique identifier of the contact to be retrieved.

    Returns:
    - contact (Contact): The contact information if found, or None if the contact is not found.
    """
    try:
        session = connect()
        contact = session.query(Contact).filter(Contact.id == contact_id).all()[0]
    except Exception as e:
        print(e)
    finally:
        session.close()

    return contact

def search_contacts(user_id, value):
    """
    Search for contacts associated with a specific user based on a provided search value.

    Parameters:
    - user_id (int): The unique identifier of the user for whom contacts are searched.
    - value (str): The search value to be matched against contact names, last names, addresses, and emails.

    Returns:
    - contacts (list): A list of Contact objects that match the search criteria.

    Note:
    - The search is case-insensitive and looks for partial matches in the name, last name, address, and email fields.
    - The results are ordered by contact name.

    Example Usage:
    - search_contacts(user_id=1, value='John')

    Example Response:
    - [{'id': 1, 'name': 'John Doe', 'last_name': 'Smith', 'address': '123 Main St', 'email': 'john@example.com'}, ...]
    """
    try:
        session = connect()
        contacts = session.query(Contact).join(BelongsTo, Contact.id == BelongsTo.contact_id).filter(BelongsTo.user_app_id == user_id).filter((Contact.name.ilike('%' + value + '%')) | (Contact.last_name.ilike('%'+ value + '%')) | (Contact.address.ilike('%' + value + '%') | (Contact.email.ilike('%' + value + '%')))).order_by(Contact.name).all()
    except Exception as e:
        print(e)
    finally:
        session.close()
    
    return contacts