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

import re
import urllib2
import time

FORMAT_URL = ('http://chartapi.finance.yahoo.com/instrument/1.0/' +
              '{ticker}/chartdata;type=quote;range=1d/csv')
RE_VALID_LINE = r'^\d{5,15}'
CACHE = '.cache/cache_{ticker}'
MIN_SAMPLES = 100


class ScraperError(Exception):
    pass


def get_intraday(ticker, min_samples=MIN_SAMPLES):
    """ Return latest intraday data of ticker """
    ret = urllib2.urlopen(FORMAT_URL.format(ticker=ticker))
    if ret.getcode() != 200:
        raise ScraperError('urlopen returned {} for ticker {}'.format(
            ret.getcode(), ticker))
    contents = ret.read()
    with open(CACHE.format(ticker=ticker), 'wb') as f:
        f.write(contents)

    valid_lines = []
    for i, line in enumerate(contents.split()):
        if re.search(RE_VALID_LINE, line) is not None:
            valid_lines.append(line)
        elif len(valid_lines) > 0:
            raise ScraperError('Trouble parsing line {} in {}'.format(
                i, CACHE.format(ticker)))
    if len(valid_lines) < min_samples:
        raise ScraperError('Only {} lines parsed for ticker {}'.format(
            len(valid_lines), ticker))
    return valid_lines


if __name__ == '__main__':

    data = get_intraday('^OMX')
    for l in data:
        p = l.split(',')
        print time.asctime(time.gmtime(float(p[0])))
