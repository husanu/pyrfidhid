# Copyright (c) 2018 charlysan

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


r"""Example script to write a tag with custom Customer ID and UID

Flow:
    - Try to read a tag within an infinite loop.
    - If a tag is found then try to write it using CID and UID.
    - Verify if the tag has been successfully written.
    - If the write operation succeeds then beep twice and output CID, UID and CRC value
    - If the write operation fails then beep three times and output error message.


Note: extra check has been added to avoid processing the same tag (CID/UID) more than once in a row.
"""

from __future__ import print_function
from time import sleep
from rfidhid.core import RfidHid

def main():
    """Main Write Tag Function"""

    # CID and UID to be written
    CID = 77
    UID = 1234567890

    try:
        # Try to open RFID device using default vid:pid (ffff:0035)
        rfid = RfidHid()
    except Exception as e:
        print(e)
        exit()

    # Initialize device
    print('Initializing device...')
    rfid.init()
    sleep(2)
    print('Done!')
    print('CID:UID to be written: %s:%s' % (CID, UID))
    print ('Please hold a tag to the reader until you hear two beeps...\n')


    uid_temp = None

    while True:
        payload_response = rfid.read_tag()
        if payload_response.has_id_data():
            uid = payload_response.get_tag_uid()
            # Avoid processing the same tag (CID/UID) more than once in a row
            if uid != uid_temp:
                uid_temp = uid

                rfid.write_tag_from_cid_and_uid(CID, UID)
                sleep(0.1) # you cannot immediately read after a write operation

                payload_response_w = rfid.read_tag()
                # Write verification
                if payload_response_w.get_tag_cid() == CID and payload_response_w.get_tag_uid() == UID:
                    print('Write OK!')
                    print('uid: %s' % payload_response_w.get_tag_uid())
                    print('customer_id: %s' % payload_response.get_tag_cid())
                    print('CRC Sum: %s' % hex(payload_response.get_crc_sum()))
                    rfid.beep(2)
                else:
                    print('Write ERROR!')
                    rfid.beep(3)
        else:
            uid_temp = None
        sleep(0.1)


if __name__ == "__main__": 
    main()
