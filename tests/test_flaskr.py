import os 
import tempfile

import pytest

from flaskr import create_app

@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            flaskr.init_db()
        yield client
    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])    

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data 

def login(client, username, password):
    return client.post('/login',data=dict(
        username=username, 
        password=password
    ),follow_redirects=True)   

def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_login_logout(client):
    """Make sure login and logout works."""

    username = flaskr.app.config["USERNAME"]
    password = flaskr.app.config["PASSWORD"]

    rv = login(client, username, password)
    assert b'You were logged in' in rv.data

    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client, f"{username}x", password)
    assert b'Invalid username' in rv.data

    rv = login(client, username, f'{password}x')
    assert b'Invalid password' in rv.data

def test_messages(client):
    """Test that message work"""

    login(client, flaskr.app.config['USERNAME'],flaskr.app.config['PASSWORD'])
    rv = client.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data    