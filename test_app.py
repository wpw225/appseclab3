import unittest
import requests
from bs4 import BeautifulSoup

server_address="http://127.0.0.1:5000"
server_login=server_address + "/login"
user_register = server_address + "/register"
spell_check = server_address + "/spell_check"

def getElementById(text, eid):
    soup = BeautifulSoup(text, "html.parser")
    result = soup.find(id=eid)
    return result

def login(uname, pword, twofactor, session=None):
    if session is None:
        session = requests.Session()
    soup = BeautifulSoup(session.get(server_login).content, "html.parser")
    csrftoken = soup.find('input', dict(name='csrf_token'))['value']
    test_creds = {"uname": uname, "pword": pword, "pword2": twofactor, "csrf_token": csrftoken}
    r = session.post(server_login, data=test_creds)
    success = getElementById(r.text, "result")
    assert success != None, "Missing id='result' in your login respons"
    return "Success" in success.text

def register(uname, pword, twofactor, session=None):
    if session is None:
        session = requests.Session()
    soup = BeautifulSoup(session.get(user_register).content, "html.parser")
    csrftoken = soup.find('input', dict(name='csrf_token'))['value']
    test_creds = {"uname": uname, "pword": pword, "pword2": twofactor, "csrf_token": csrftoken}
    r = session.post(user_register, data=test_creds)
    success = getElementById(r.text, "success")
    if success is None:
        return False
    return "Success" in success.text

class FeatureTest(unittest.TestCase):

    def test_page_exists(self):

        PAGES = ["/","/register","/login","/spell_check"]
        for page in PAGES:
            req = requests.get(server_address + page)
            self.assertEqual(req.status_code, 200)

    def test_valid_login(self):
        #login_addr = server_address + "/login"
        resp = login("test30","test30","")
        self.assertTrue(resp, "success! you are logged in")

    def test_valid_2fa_login(self):
        #login_addr = server_address + "/login"
        resp = login("test31","test31","1111111111")
        self.assertTrue(resp, "success! you are logged in with 2fa")


    def test_invalid_login(self):
        #login_addr = server_address + "/login"
        resp = login("test30","badpass","")
        self.assertFalse(resp, "Login authenticated an invalid uname/password")

    def test_invalid_2fa_login(self):
        #login_addr = server_address + "/login"
        resp = login("test31","test31","2222222222")
        self.assertFalse(resp, "Login authenticated an invalid 2fa")

#    def test_registration(self):
#        resp = register("test50","test50","")
#        self.assertTrue(resp, "Registration successful")
#
#    def test_2fa_registration(self):
#        resp = register("test51","test51","0123456789")
#        self.assertTrue(resp, "2FA Registration successful")
#
    def test_invalid_registration(self):
        resp = register("test30","test30","") #Duplicate ID
        self.assertFalse(resp, "Duplicate registration successful")

    def test_invalid_2fa_registration(self):
        resp = register("test31","test31","0123456789")
        self.assertFalse(resp, "Duplicate 2FA registration successful")


if __name__ == '__main__':
    unittest.main()

