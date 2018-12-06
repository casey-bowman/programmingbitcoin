from io import BytesIO
from unittest import TestCase

import op

from ecc import S256Point, Signature
from helper import hash160
from op import encode_num
from script import Script


"""
# tag::exercise1[]
==== Exercise 1

Write the `op_hash160` function.
# end::exercise1[]
"""

# tag::answer1[]
def op_hash160(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    h160 = hash160(element)
    stack.append(h160)
    return True
# end::answer1[]

"""
# tag::exercise2[]
==== Exercise 2

Write the `op_checksig` function in `op.py`
# end::exercise2[]
"""

# tag::answer2[]
def op_checksig(stack, z):
    if len(stack) < 2:
        return False
    sec_pubkey = stack.pop()
    der_signature = stack.pop()[:-1]
    try:
        point = S256Point.parse(sec_pubkey)
        sig = Signature.parse(der_signature)
    except (ValueError, SyntaxError) as e:
        return False
    if point.verify(z, sig):
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True
# end::answer2[]


"""
# tag::exercise3[]
==== Exercise 3

Create a ScriptSig that can unlock this ScriptPubKey. Note `OP_MUL` multiplies the top two elements of the stack.

`767695935687`

* `56 = OP_6`
* `76 = OP_DUP`
* `87 = OP_EQUAL`
* `93 = OP_ADD`
* `95 = OP_MUL`
# end::exercise3[]
# tag::answer3[]
>>> from script import Script
>>> script_pubkey = Script(0x76, 0x76, 0x95, 0x93, 0x56, 0x87)
>>> script_sig = Script([0x52])
>>> combined_script = script_sig + script_pubkey
>>> print(combined_script.evaluate(0))
True

# end::answer3[]
# tag::exercise4[]
==== Exercise 4

Figure out what this Script is doing:

`6e879169a77ca787`

* `69 = OP_VERIFY`
* `6e = OP_2DUP`
* `7c = OP_SWAP`
* `87 = OP_EQUAL`
* `91 = OP_NOT`
* `a7 = OP_SHA1`

Use the `Script.parse` method and look up what various opcodes do at https://en.bitcoin.it/wiki/Script

# end::exercise4[]
# tag::answer4[]
>>> from script import Script
>>> script_pubkey = Script(0x6e, 0x87, 0x91, 0x91, 0x69, 0xa7, 0x7c, 0xa7, 0x87)
>>> c1 = '255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3' + \
...     'c3c2f57696474682032203020522f48656967687420332030205' + \
...     '22f547970652034203020522f537562747970652035203020522' + \
...     'f46696c7465722036203020522f436f6c6f72537061636520372' + \
...     '03020522f4c656e6774682038203020522f42697473506572436' + \
...     'f6d706f6e656e7420383e3e0a73747265616d0affd8fffe00245' + \
...     '348412d3120697320646561642121212121852fec092339759c3' + \
...     '9b1a1c63c4c97e1fffe017f46dc93a6b67e013b029aaa1db2560' + \
...     'b45ca67d688c7f84b8c4c791fe02b3df614f86db1690901c56b4' + \
...     '5c1530afedfb76038e972722fe7ad728f0e4904e046c230570fe' + \
...     '9d41398abe12ef5bc942be33542a4802d98b5d70f2a332ec37fa' + \
...     'c3514e74ddc0f2cc1a874cd0c78305a21566461309789606bd0b' + \
...     'f3f98cda8044629a1'
>>> c2 = '255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3' + \
...     'c3c2f57696474682032203020522f48656967687420332030205' + \
...     '22f547970652034203020522f537562747970652035203020522' + \
...     'f46696c7465722036203020522f436f6c6f72537061636520372' + \
...     '03020522f4c656e6774682038203020522f42697473506572436' + \
...     'f6d706f6e656e7420383e3e0a73747265616d0affd8fffe00245' + \
...     '348412d3120697320646561642121212121852fec092339759c3' + \
...     '9b1a1c63c4c97e1fffe017346dc9166b67e118f029ab621b2560' + \
...     'ff9ca67cca8c7f85ba84c79030c2b3de218f86db3a90901d5df4' + \
...     '5c14f26fedfb3dc38e96ac22fe7bd728f0e45bce046d23c570fe' + \
...     'b141398bb552ef5a0a82be331fea48037b8b5d71f0e332edf93a' + \
...     'c3500eb4ddc0decc1a864790c782c76215660dd309791d06bd0a' + \
...     'f3f98cda4bc4629b1'
>>> collision1 = bytes.fromhex(c1)  # <1>
>>> collision2 = bytes.fromhex(c2)
>>> script_sig = Script([collision1, collision2])
>>> combined_script = script_sig + script_pubkey
>>> print(combined_script.evaluate(0))
True

# end::answer4[]
"""


class Chapter6Test(TestCase):

    def test_apply(self):

        op.op_hash160 = op_hash160
        op.op_checksig = op_checksig
        op.OP_CODE_FUNCTIONS[0xa9] = op_hash160
        op.OP_CODE_FUNCTIONS[0xac] = op_checksig
