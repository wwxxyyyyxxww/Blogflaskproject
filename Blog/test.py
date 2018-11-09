# Dict = {[1,2]:'a'}

class A:
    password_hash=''
    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self,password):
        self.password_hash = password

class B:
    password_hash=''
    def password(self):
        return self.password_hash

    def password1(self,password):
        self.password_hash = password

a=B()
a.password1(1)
print(a.password())

a=A()
a.password = 1
print(a.password)