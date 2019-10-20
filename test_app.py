import unittest
import requests
from bs4 import BeautifulSoup

server_address="http://127.0.0.1:5000"
server_login=server_address + "/login"

def getElementById(text, eid):
    soup = BeautifulSoup(text, "html.parser")
    result = soup.find(id=eid)
    return result

def login(uname, pword, twofactor, session=None):
    addr = server_address + "/login"
    if session is None:
        session = requests.Session()
#    test_creds = {"Username": uname, "Password": pword, "2FA": twofactor}
    test_creds = {"uname": uname, "pword": pword, "pword2": twofactor}
    r = session.post("http://127.0.0.1:5000/login", data=test_creds)
#    r = session.get(addr)
#    r = session.get("http://127.0.0.1:5000")
    print("h1")
    print(r)
    print("status_code")
    print(r.status_code)
    print("post.content")
    print(r.content)
    print("end post.content")
    print("h2")
    success = getElementById(r.text, "result")
    print("success")
    print(success)
    assert success != None, "Missing id='result' in your login respons"
    return "Success" in success.text


class FeatureTest(unittest.TestCase):

    def test_page_exists(self):

        PAGES = ["/","/register","/login","/spell_check"]
        for page in PAGES:
            req = requests.get(server_address + page)
            self.assertEqual(req.status_code, 200)

#    def test_valid_login(self):
#        login_addr = server_address + "/login"
#        resp = login("test30","test30","")
#        print("k1")
#        print(resp)
#        self.assertTrue(resp, "success! you are logged in")
#
#    def test_invalid_login(self):
#        login_addr = server_address + "/login"
#        resp = login("test30","badpass","")
#        self.assertFalse(resp, "Login authenticated an invalid uname/password/2fa")

if __name__ == '__main__':
    unittest.main()

