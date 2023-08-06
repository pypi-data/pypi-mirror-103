# Copyright (c) 2020 Emanuele Bellocchia
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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# Imports
from typing import Dict
from bip_utils.base58.base58 import Base58Alphabets, Base58Const, Base58Encoder, Base58Decoder


class CBase58Utils:
    """ Class container for CBase58 utility functions. """

    @staticmethod
    def ComputeChecksum(data_bytes: bytes) -> bytes:
        """ Compute CBase58 checksum.
        Similar to Base58 but it's the last 4 bytes of the single SHA256.

        Args:
            data_bytes (bytes): Data bytes

        Returns:
            bytes: Computed checksum
        """
        return CryptoUtils.Sha256(data_bytes)[-Base58Const.CHECKSUM_BYTE_LEN:]


class CBase58Encoder:
    """ CBase58 encoder class. Variation of the Base58 format with a different checksum computation. """

    @staticmethod
    def CheckEncode(data_bytes: bytes,
                    alph_idx: Base58Alphabets = Base58Alphabets.BITCOIN) -> str:
        """ Encode bytes into Base58 string with checksum.

        Args:
            data_bytes (bytes)                  : Data bytes
            alph_idx (Base58Alphabets, optional): Alphabet index, Bitcoin by default

        Returns:
            str: Base58 encoded string with checksum

        Raises:
            TypeError: If alphabet index is not a Base58Alphabets enumerative
        """

        # Append checksum and encode all together
        return Base58Encoder.Encode(data_bytes + CBase58Utils.ComputeChecksum(data_bytes), alph_idx)


class CBase58Decoder:
    """ CBase58 decoder class. Variation of the Base58 format with a different checksum computation. """

    @staticmethod
    def CheckDecode(data_str: str,
                    alph_idx: Base58Alphabets = Base58Alphabets.BITCOIN) -> bytes:
        """ Decode bytes from a Base58 string with checksum.

        Args:
            data_str (str)                      : Data string
            alph_idx (Base58Alphabets, optional): Alphabet index, Bitcoin by default

        Returns:
            bytes: Base58 decoded bytes (checksum removed)

        Raises:
            ValueError: If the string is not a valid Base58 format
            TypeError: If alphabet index is not a Base58Alphabets enumerative
            Base58ChecksumError: If checksum is not valid
        """

        # Decode string
        dec_bytes = Base58Decoder.Decode(data_str, alph_idx)
        # Get data and checksum bytes
        data_bytes = dec_bytes[:-Base58Const.CHECKSUM_BYTE_LEN]
        checksum_bytes = dec_bytes[-Base58Const.CHECKSUM_BYTE_LEN:]

        # Compute checksum
        comp_checksum = CBase58Utils.ComputeChecksum(data_bytes)

        # Verify checksum
        if checksum_bytes != comp_checksum:
            raise Base58ChecksumError("Invalid checksum (expected %s, got %s)" % (comp_checksum, checksum_bytes))

        return data_bytes
