#! /usr/bin/env python3

"""Report on Unix error numbers, and also (if appropriate) what the error means
in KBUS.

    errno  99
    errno  EPERM
    errno  -2               # cope with negative values
    errno  0xffffffed       # cope with negative 32-bit hex values
    errno  -list            # to list all known errors

Use -h, -help, --help or help to get this text.

Add a -k or -kbus to the command line to get the KBUS interpretation of the
value as well.

More than one value will give more than one answer.
"""

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is the KBUS Lightweight Linux-kernel mediated
# message system
#
# The Initial Developer of the Original Code is Kynesim, Cambridge UK.
# Portions created by the Initial Developer are Copyright (C) 2009
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Kynesim, Cambridge UK
#   Tibs <tibs@tonyibbs.co.uk>
#
# ***** END LICENSE BLOCK *****

import sys
import os
import textwrap
import errno
from errno import errorcode


def __(text):
    return textwrap.dedent(text)


kbus_codes = {
        # Things cut-and-pasted (and mildly mangled) from the KBUS documentation
    'EADDRINUSE': __("""\
        On attempting to bind a message name as replier: There is already a
        replier bound for this message.
        """),

    'EADDRNOTAVAIL': __("""\
        On attempting to send a Request message: There is no replier bound for
        this message's name.

        On attempting to send a Reply message: The sender of the original
        request (i.e., the KSock mentioned as the ``to`` in the Reply) is no
        longer connected.
        """),

    'EALREADY': __("""\
        On attempting to write to a KSock, when a previous send has returned
        EAGAIN. Either DISCARD the message, or use select/poll to wait for the
        send to complete, and write to be allowed.
        """),

    'EBADMSG': __("""\
        On attempting to bind, unbind or send a message: The message name is
        not valid. On sending, this can also be because the message name is a
        wildcard.
        """),

    'EBUSY': __("""\
        On attempting to send, then:

        1. For a request, the replier's message queue is full.

        2. For any message, with ALL_OR_FAIL set, one of the targetted
           listener/replier queues was full.
        """),

    'ECONNREFUSED': __("""\
        On attempting to send a Reply, the intended recipient (the notional
        original sender of the Request) is not expecting a Reply with that
        message id in its 'in_reply_to'. Or, in other words, this appears to be
        an attempt to reply to the wrong message id or the wrong KSock.
        """),

    'EINVAL': __("""\
        Something went wrong (generic error).
        """),

    'EMSGSIZE': __("""\
        On attempting to write a message: Data was written after the end of the
        message (i.e., after the final end guard of the message).
        """),

    'ENAMETOOLONG': __("""\
        On attempting to bind, unbind or send a message: The message name is
        too long.
        """),

    'ENOENT': __("""\
        On attempting to open a KSock: There is no such device (normally
        because one has tried to open, for instance, '/dev/kbus9' when there
        are only 3 KBUS devices).
        """),

    'ENOLCK': __("""\
        On attempting to send a Request, when there is not enough room in the
        sender's message queue to guarantee that it can receive a reply for
        every Request already sent, *plus* this one. If there are oustanding
        messages in the sender's message queue, then the solution is to read
        some of them. Otherwise, the sender will have to wait until one of the
        Repliers replies to a previous Request (or goes away and KBUS replies
        for it).

        When this error is received, the send has failed (just as if the
        message was invalid). The sender is not left in "sending" state, nor
        has the message been assigned a message id.

        Note that this is *not* EAGAIN, since we do not want to block the
        sender (in the SEND) if it is up to the sender to perform a read to
        sort things out.
        """),

    'ENOMSG': __("""\
        On attempting to send, when there is no message waiting to be sent
        (either because there has been no write since the last send, or because
        the message being written has been discarded).
        """),

    'EPIPE': __("""\
        On attempting to send 'to' a specific replier, the replier with that id
        is no longer bound to the given message's name.
        """),

    # Things not explicit in the KBUS documentation
    'EFAULT': __("""\
            Memory allocation, copy from user space, or other such failed. This
            is normally very bad, it should not happen, UNLESS it is the result
            of calling an ioctl, when it indicates that the ioctl argument
            cannot be accessed.
            """),

    'ENOMEM': __("""\
            Memory allocation failed (return NULL). This is normally very bad,
            it should not happen.
            """),

    'EAGAIN': __("""\
            On attempting to send, the message being sent had ALL_OR_WAIT set,
            and one of the targetted listener/replier queues was full.

            On attempting to unbind when Replier Bind Events have been
            requested, one or more of the KSocks bound to receive
            "$.KBUS.ReplierBindEvent" messages has a full message queue,
            and thus cannot receive the unbind event. The unbind has not been
            done.
            """),
    }


def check_kbus(errname):
    if errname in kbus_codes:
        print()
        print('KBUS: %s' % errname)
        print(kbus_codes[errname])


def main(args):
    if len(args) == 0:
        print(__doc__)
        return

    want_kbus = False
    values = []

    while args:
        thing = args[0]
        args = args[1:]

        if thing == '-list':
            for key, value in errorcode.items():
                print('%3d: %-20s %s' % (key, value, os.strerror(key)))
            return
        elif thing in ('-h', '-help', '--help', 'help'):
            print(__doc__)
            return
        elif thing in ('-k', '-kbus'):
            want_kbus = True
        else:
            values.append(thing)

    for thing in values:
        try:
            errnum = int(thing, 0)
            if errnum < 0:
                # It was probably a negative error number
                # - we can be friendly and convert it for the user
                guess = -errnum
                print('Assuming %d means %d' % (errnum, guess))
                errnum = guess
            elif 0xffffffff >= errnum > 0xffff0000:
                # It was probably a negative error number as a 32-bit quantity
                # - we can be friendly and convert it for the user
                guess = 0x100000000 - errnum
                print('Assuming %#0x means -%d' % (errnum, guess))
                errnum = guess
            print('Error %d (0x%x) is %s: %s' % (errnum, errnum,
                                                 errorcode[errnum], os.strerror(errnum)))
            if want_kbus:
                check_kbus(errorcode[errnum])
            continue
        except KeyError:
            print('Unrecognised error code number %d' % errnum)
            continue
        except ValueError:
            # It wasn't a plausible number - fall through
            pass

        reverse = {}
        for key, value in errorcode.items():
            reverse[value] = key

        if thing in reverse:
            errnum = reverse[thing]
            print('%s is error %d (0x%x): %s' % (thing, errnum, errnum, os.strerror(errnum)))
        else:
            print('Unrecognised error code mnemonic %s' % thing)

        if want_kbus:
            check_kbus(thing)


if __name__ == "__main__":
    main(sys.argv[1:])

# vim: set tabstop=8 softtabstop=4 shiftwidth=4 expandtab:
