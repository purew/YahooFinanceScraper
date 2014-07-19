# The MIT License (MIT)
#
# Copyright (c) 2014 Anders Bennehag
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import smtplib
import string
import traceback


def sendEmail(to, subject, msg):
    import google
    frm = google.USER
    BODY = string.join((
        "From: %s" % frm,
        "To: %s" % to,
        "Subject: %s" % subject,
        "",
        msg
        ), "\r\n")

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(google.USER, google.PASS)
    server.sendmail(frm, to, BODY)
    server.quit()


def formatExceptionMsg(e):
    return ('Caught exception: {}\n\n'.format(str(e)) +
            'Full stacktrace:\n' + traceback.format_exc())


def emailException(to, fname, e):
    subject = 'ERROR: Exception in {}'.format(fname)
    msg = formatExceptionMsg(e)
    sendEmail(to, subject, msg)
