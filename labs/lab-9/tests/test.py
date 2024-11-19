import pytest

from sqlalchemy import insert, select, text
from models import User

# test db connection
def test_db_connection(db_session):
    # Use db_session to interact with the database
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

# test to insert a user
# you can count this as one of your 5 test cases :)
def test_insert_user(db_session, sample_signup_input):
    insert_stmt = insert(User).values(sample_signup_input)

    # execute insert query
    db_session.execute(insert_stmt)
    # commit the changes to the db
    db_session.commit()

    # not part of the app.py code, just being used to get the inserted data
    selected_user = db_session.query(User).filter_by(FirstName="Calista").first()

    assert selected_user is not None
    assert selected_user.LastName == "Phippen"

# 3. Test invalid user signup (missing required fields)
def test_invalid_signup(db_session):
    """Test signup with missing required fields."""
    incomplete_user = {'FirstName': '', 'LastName': 'Phippen', 'Email': '', 'Password': 'mypassword'}
    with pytest.raises(Exception):
        db_session.execute(insert(User).values(incomplete_user))

# 4. Test valid login
def test_valid_login(db_session, sample_signup_input, sample_login_input):
    """Ensure a user can log in with valid credentials."""
    
    insert_stmt = insert(User).values(sample_signup_input)
    db_session.execute(insert_stmt)
    db_session.commit()

   
    query = text(f"SELECT Password FROM users WHERE Email = '{sample_login_input['Email']}'")
    result = db_session.execute(query).fetchone()

    
    assert result is not None
    assert result[0] == sample_login_input['Password']

# 5. Test login with incorrect password (expected to fail)
def test_invalid_login(db_session, sample_signup_input, sample_login_input):
    """Ensure login fails with incorrect credentials."""
    
    insert_stmt = insert(User).values(sample_signup_input)
    db_session.execute(insert_stmt)
    db_session.commit()

    
    invalid_login_input = sample_login_input.copy()
    invalid_login_input['Password'] = 'wrongpassword'

    
    query = text(f"SELECT Password FROM users WHERE Email = '{invalid_login_input['Email']}'")
    result = db_session.execute(query).fetchone()

    
    assert result is not None
    assert result[0] != invalid_login_input['Password']
