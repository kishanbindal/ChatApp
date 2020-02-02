class UserFunctions:

    def __init__(self, request):
        self.request = request


    def get_reg_data(self):
        username = self.request.data.get('username')
        email = self.request.data.get('email')
        password = self.request.data.get('password')
        return self._validate_reg_request_data(username, email, password)

    def _validate_reg_request_data(self, username, email, password):

        if {username, email, password} is None:
            raise TypeError("INPUT VALUE CANNOT BE NONE")
        elif {username, email, password} == '':
            raise ValueError("Input Value cannot be empty")
        else:
            return username, email, password

    def get_login_data(self):

        email = self.request.data.get('email')
        password = self.request.data.get('password')
        return self._validate_login_request_data(email, password)

    def _validate_login_request_data(self, email, password):

        if {email, password} is None:
            raise TypeError("INPUT VALUES CANNOT BE None")
        elif {email, password} == '':
            raise ValueError("Input Value cannot be empty")
        else:
            return email, password

    def get_forgot_password_data(self):

        email = self.request.data.get('email')
        return self._validate_forgot_data(email)

    def _validate_forgot_data(self, email):

        if email is None:
            return TypeError("INPUT VALUE CANNT BE NONE")
        else:
            return email
