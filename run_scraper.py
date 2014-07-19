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

import os
import yahooscraper
import sendemail
import ticker_lists


DATA_DIR = 'data'

LISTS = [
    (ticker_lists.STO_MID_CAP, 1),
    (ticker_lists.STO_SMALL_CAP, 1),
    (ticker_lists.WORLD_INDICES, 200),
    (ticker_lists.OMXS30, 200),
    ]


def appendToFile(ticker, data):
    ticker = ticker.replace('^', '_')
    fname = os.path.join(DATA_DIR, ticker + '.csv')
    with open(fname, 'wa') as f:
        for line in data:
            f.write(line + '\n')


if __name__ == '__main__':

    for tlist, minsamples in LISTS:
        for ticker in tlist:
            try:
                #print 'Fetching {}'.format(ticker)
                data = yahooscraper.get_intraday(ticker, minsamples)
                appendToFile(ticker, data)
            except Exception as e:
                subject = 'Error parsing ticker {}'.format(ticker)
                msg = sendemail.formatExceptionMsg(e)
                sendemail.sendEmail('anders@bennehag.com', subject, msg)
            else:
                pass
