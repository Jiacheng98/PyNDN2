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
This module defines the Signature class which is an abstract base class 
providing methods to work with the signature information in an NDN Data packet.
You must use an object of a subclass, for example Sha256WithRsaSignature.
"""

class Signature(object):
    def clone(self):
        """
        Create a new Signature which is a copy of this signature.
        Your derived class should override.

        :return: A new object which is a copy of this object.
        :rtype: A subclass of Signature
        :raises RuntimeError: for unimplemented if the derived class does not 
          override.
        """
        raise RuntimeError("Signature.clone is not implemented")

    def getChangeCount(self):
        """
        Get the change count, which is incremented each time this object 
        (or a child object) is changed.
        Your derived class should override.

        :return: The change count.
        :rtype: int
        :raises RuntimeError: for unimplemented if the derived class does not 
          override.
        """
        raise RuntimeError("Signature.getChangeCount is not implemented")
