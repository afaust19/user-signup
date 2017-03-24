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

header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
</head>
<body>
"""

footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        form = """
            <h1>Signup</h1>
            <form action="/welcome" method="post">
                <br>
                <label>Username<input type="text" name="username"></label><br>
                <label>Password<input type="text" name="password"></label><br>
                <label>Verify Password<input type="text" name="verify_password"></label><br>
                <label>Email (optional)<input type="text" name="email"></label><br>
                <input type="submit">
            </form>
        """

        self.response.write(header + form + footer)

class Welcome(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("username")
        successmessage = "<h1><strong>" + "Welcome, " + username + "!" + "</strong></h1>"
        self.response.write(header + successmessage + footer)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
