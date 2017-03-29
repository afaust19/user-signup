#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

form = """<!DOCTYPE html>

<html>
    <head>
        <title>User Signup</title>
        <style type="text/css">
            .label {text-align: left}
            .error {color: red}
        </style>

    </head>
    <body>
        <h2>Signup</h2>
        <form method="post">
        <table>
            <tr>
                <td class="label">
                    Username
                </td>
                <td>
                    <input type="text" name="username" value="%(username)s">
                </td>
                <td class="error">
                    %(error_username)s
                </td>
            </tr>

                <tr>
                    <td class="label">
                        Password
                    </td>
                    <td>
                        <input type="password" name="password" value="%(password)s">
                    </td>
                    <td class="error">
                        %(error_password)s
                    </td>
                </tr>

                <tr>
                    <td class="label">
                        Verify Password
                    </td>
                    <td>
                        <input type="password" name="verify" value="%(verify)s">
                    </td>
                    <td class="error">
                        %(error_verify)s
                    </td>
                </tr>

                <tr>
                    <td class="label">
                        Email (optional)
                    </td>
                    <td>
                        <input type="text" name="email" value="%(email)s">
                    </td>
                    <td class="error">
                        %(error_email)s
                    </td>
                </tr>
            </table>
            <input type="submit">
            </form>
        </body>
</html>

"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

def equal_password(verify, password):
    if password == verify:
        return True
    else:
        return False

EMAIL_RE = re.compile(r'^[\S]+@[\S]+.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(webapp2.RequestHandler):

    def write_form(self, username="", error_username="", password="", error_password="",
                   verify="", error_verify="", email="", error_email=""):
        self.response.out.write(form %{"username": username,"error_username": error_username,
                                       "password": password,"error_password": error_password,
                                       "verify": verify,"error_verify": error_verify,
                                       "email": email,"error_email": error_email})

    def get(self):
        self.write_form()

    def post(self):

        input_username = self.request.get("username")
        input_password = self.request.get("password")
        input_verify = self.request.get("verify")
        input_email = self.request.get("email")

        if valid_username(input_username) and valid_password(input_password) and input_password == input_verify and valid_email(input_email):
            self.redirect("/welcome?username=" + input_username)

        if not valid_username(input_username):
            error_username = "That's not a valid username"   # Validate username
        else:
            error_username = ""


        if not valid_password(input_password):
            error_password = "That's not a valid password"   # Validate password
        else:
            error_password = ""


        if input_password != input_verify:                   # Validate verify password
            error_verify = "Passwords don't match"
        else:
            error_verify = ""


        if not valid_email(input_email):                     # Validate email
            error_email = "That's not a valid email"
        else:
            error_email = ""

        Signup.write_form(self, input_username, error_username, "", error_password,
                              "", error_verify, input_email, error_email)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.out.write("<h1>Welcome, " + username + "!</h1>")

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
