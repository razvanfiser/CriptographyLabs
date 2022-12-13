import SignUp
class SignUpForm:
    def __init__(self):
        pass

    def sign_up_form(self):
        username = input()
        password = input()
        sign_up = SignUp(username, password)
        sign_up.send_data()

    def print_entries


