# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014 Regents of the University of California.
# Author: Jeff Thompson <jefft0@remap.ucla.edu>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# A copy of the GNU General Public License is in the file COPYING.

"""
This module defines the NfdCommandInterestGenerator class which keeps track of a 
timestamp and generates command interests according to the NFD Signed Command 
Interests protocol:
http://redmine.named-data.net/projects/nfd/wiki/Command_Interests
"""

from random import SystemRandom
from pyndn.name import Name
from pyndn.util.blob import Blob
from pyndn.util.common import Common

# The Python documentation says "Use SystemRandom if you require a 
#   cryptographically secure pseudo-random number generator."
# http://docs.python.org/2/library/random.html
_systemRandom = SystemRandom()

class NfdCommandInterestGenerator(object):
    """
    Create a new NfdCommandInterestGenerator and initialize the timestamp to now.
    """
    def __init__(self):
        self._lastTimestamp = round(Common.getNowMilliseconds())
        
    def generate(self, interest, keyChain, certificateName, wireFormat = None):
        """
        Append a timestamp component and a random value component to interest's
        name. This ensures that the timestamp is greater than the timestamp used 
        in the previous call. Then use keyChain to sign the interest which 
        appends a SignatureInfo component and a component with the signature 
        bits. If the interest lifetime is not set, this sets it.

        :param Interest interest: The interest whose name is append with 
          components.
        :param KeyChain keyChain: The KeyChain for calling sign.
        :param Name certificateName: The certificate name of the key to use for 
          signing.
        :param wireFormat: (optional) A WireFormat object used to encode this 
           ControlParameters. If omitted, use WireFormat.getDefaultWireFormat().
        :type wireFormat: A subclass of WireFormat
        """
        if wireFormat == None:
            # Don't use a default argument since getDefaultWireFormat can change.
            wireFormat = WireFormat.getDefaultWireFormat()

        timestamp =  round(Common.getNowMilliseconds())
        while timestamp <= self._lastTimestamp:
          timestamp += 1.0

        interest.getName().append(Name.Component.fromNumber(int(timestamp)))
        randomBuffer = bytearray(8)
        for i in range(len(randomBuffer)):
            randomBuffer[i] = _systemRandom.randint(0, 0xff)                
        interest.getName().append(Blob(randomBuffer, False))

        keyChain.sign(interest, certificateName)

        if (interest.getInterestLifetimeMilliseconds() == None or
            interest.getInterestLifetimeMilliseconds()< 0):
          # The caller has not set the interest lifetime, so set it here.
          interest.setInterestLifetimeMilliseconds(1000.0)

        # We successfully signed the interest, so update the timestamp.
        self._lastTimestamp = timestamp
        