import io
import enum
import os
from typing import Optional


class RomWriterType(enum.IntEnum):
    null = 0
    file = 1
    ipsblob = 2


class RomWriter:
    romWriterType: RomWriterType
    romFile: Optional[io.BufferedIOBase]
    ipsblob: bytearray
    baseFilename: str

    def __init__(self) -> None:
        self.romWriterType = RomWriterType.null
        self.romFile = None
        self.ipsblob = bytearray()
        self.baseFilename = ''

    @classmethod
    def fromFilePaths(cls, origRomPath: str, newRomPath: str) -> "RomWriter":
        instance = cls()
        instance.romWriterType = RomWriterType.file
        instance.romFile = RomWriter.createWorkingFileCopy(origRomPath, newRomPath)
        return instance

    @classmethod
    def fromBlankIps(cls) -> "RomWriter":
        instance = cls()
        instance.romWriterType = RomWriterType.ipsblob
        instance.ipsblob = bytearray(b'PATCH')
        return instance

    @staticmethod
    def createWorkingFileCopy(origFile: str, newFile: str) -> io.BufferedIOBase:
        if not os.path.exists(origFile):
            raise Exception(f'origFile not found: {origFile}')
        with open(origFile, 'rb') as orig:
            romFile = open(newFile, 'wb')  # wb = write, binary
            # copy original to new before we edit new
            while True:
                chunk = orig.read(16384)  # or any amount
                if chunk == b"":
                    break
                romFile.write(chunk)
            return romFile

    @staticmethod
    def isAllRepeatedBytes(data: bytes) -> bool:
        if len(data) < 2:
            return False
        byte = data[0]
        for i in range(1, len(data)):
            if data[i] != byte:
                return False
        return True

    def writeBytes(self, address: int, data: bytes) -> None:
        if self.romWriterType == RomWriterType.file:
            assert self.romFile
            self.romFile.seek(address)
            self.romFile.write(data)
        elif self.romWriterType == RomWriterType.ipsblob:
            if len(data) >= 65536:
                raise Exception(f'data length {len(data)} exceeds max IPS len of 65536')
            self.ipsblob.extend(address.to_bytes(3, 'big'))
            if len(data) > 10 and RomWriter.isAllRepeatedBytes(data):
                # RLE encode
                self.ipsblob.extend(b'\x00\x00')
                self.ipsblob.extend(len(data).to_bytes(2, 'big'))
                self.ipsblob.append(data[0])
            else:
                # normal patch data
                self.ipsblob.extend(len(data).to_bytes(2, 'big'))
                self.ipsblob.extend(data)

    def writeItem(self, address: int, plmid: bytes, ammoAmount: bytes = b"\x00") -> None:
        if len(plmid) != 2 or len(ammoAmount) != 1:
            raise Exception(f'plmid length ({len(plmid)}) must be 2 and ammoAmount '
                            f'length ({len(ammoAmount)}) must be 1')
        self.writeBytes(address, plmid)
        self.writeBytes(address+5, ammoAmount)

    def finalizeRom(self) -> None:
        if self.romWriterType == RomWriterType.file:
            if self.romFile:
                self.romFile.close()
                self.romFile = None
        elif self.romWriterType == RomWriterType.ipsblob:
            self.ipsblob.extend(b'EOF')

    def getFinalIps(self) -> bytearray:
        if self.romWriterType != RomWriterType.ipsblob:
            raise Exception('getFinalIps() called on non-ipsblob-typed RomWriter')
        if bytes(self.ipsblob[-3:]) != b'EOF':
            raise Exception('getFinalIps() called before finalizeRom()')
        return self.ipsblob

    def setBaseFilename(self, baseFilename: str) -> None:
        self.baseFilename = baseFilename

    def getBaseFilename(self) -> str:
        return self.baseFilename
