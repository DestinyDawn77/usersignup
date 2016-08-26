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
import cgi
import re

form = """
    <form method = "post">
        <div style = "font-size:16pt"><b>SignUp</b></div>
        <div style = "text-align:justify">
            <label> Username
                <input type = "text" name = "username"  value = "%(username)s">
                <div style = "color:red">%(usererror)s</div>
            </label>

            <br>
            <label> Password
                <input type = "password" name = "password" value = "">
                <div style = "color:red">%(passerror)s</div>
            </label>

            <br>
            <label> Verify Password
                <input type = "password" name = "verify" value = "">
                <div style = "color:red">%(verifyerror)s</div>
            </label>

            <br>
            <label> Email (optional)
                <input type = "text" name = "user_email" value = "%(user_email)s">
                <div style = "color:red">%(emailerror)s</div>
            </label>

        </div>
        <br>
        <input type = "submit">
    </form>
"""


#checking the input to verify it is valid

#checking user for only characters a-z, cap a-z, and that it is atleast 3-20 characters
USER = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_user(userName):
    return userName and USER.match(userName)

#password should be 3-20 characters
PASS= re.compile(r"^.{3,20}$")
def valid_pass(passWord):
    return passWord and PASS.match(passWord)

EMAIL = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL.match(email)

def escape_html(s):
    return cgi.escape(s, quote = True)


class MainHandler(webapp2.RequestHandler):

    def display_form(self, usererror = "", passerror = "", verifyerror = "", emailerror = "", username = "", user_email = ""):
    #def display_form(self, usererror, passerror,verifyerror, emailerror, username, user_email)
    #def display_form(self, usererror, passerror, verifyerror, emailerror, username, user_email)
        self.response.out.write(form % {"usererror":usererror,"passerror": passerror, "verifyerror": verifyerror, "emailerror":emailerror, "username":escape_html(username), "user_email":escape_html(user_email)})


    def get(self):
        self.display_form()
    def post(self):
        isAnError = False
        userName = self.request.get("username")
        passWord = self.request.get("password")
        verifyPass = self.request.get("verify")
        email = self.request.get("user_email")



        usererror = ""
        passerror = ""
        verifyerror = ""
        emailerror = ""



        if not (valid_user(userName)):
            isAnError = True
            usererror = "That's not a valid username!"


        if not(valid_pass(passWord)):
            isAnError = True
            passerror = "That's not a valid password"


        if not (passWord == verifyPass):
            isAnError = True
            verifyerror = "Passwords do not match"

        if not(valid_email(email)):
            isAnError = True
            emailerror = "That's not a valid email address"


            #self.response.out.write(usererror)
            #self.response.out.write(passerror)
            #self.response.out.write(emailerror)

            #self.response.out.write(email)

        if isAnError:
            self.display_form(usererror, passerror, verifyerror, emailerror, userName, email)
        else:
            user = self.request.get("username")
            self.redirect("/thanks?username=" + user)







class ThanksHandler(webapp2.RequestHandler):

    def get(self):
        user = self.request.get("username")
        self.response.out.write("Welcome {0} !".format(user))
        #self.response.write(inputFields%('Programming') + '<hr />' + blah)












app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler)

], debug=True)
