import io
import enum
import os

class RomWriterType(enum.Enum):
    file = 1
    ipsblob = 2

class RomWriter:
    def __init__(self):
        self.romWriterType : RomWriterType = 0
        self.romFile : io.BufferedIOBase = None
        self.ipsblob : bytearray = None
        self.baseFilename : str = ''

    @classmethod
    def fromFilePaths(cls, origRomPath: str, newRomPath: str):
        instance = cls()
        instance.romWriterType = RomWriterType.file
        instance.romFile = RomWriter.createWorkingFileCopy(origRomPath, newRomPath)
        return instance

    @classmethod
    def fromBlankIps(cls):
        instance = cls()
        instance.romWriterType = RomWriterType.ipsblob
        instance.ipsblob = bytearray(b'PATCH')
        return instance


    def createWorkingFileCopy(origFile, newFile) -> io.BufferedIOBase:
        if not os.path.exists(origFile):
            raise Exception(f'origFile not found: {origFile}')
        with open(origFile, 'rb') as orig:
            romFile = open(newFile, 'wb') # wb = write, binary
            # copy original to new before we edit new
            while True:
                chunk = orig.read(16384) # or any amount
                if chunk == b"":
                    break
                romFile.write(chunk)
            return romFile


    def isAllRepeatedBytes(data):
        if len(data) < 2:
            return False
        byte = data[0]
        for i in range(1, len(data)):
            if data[i] != byte:
               return False
        return True


    def writeBytes(self, address : int, data):
        if self.romWriterType == RomWriterType.file:
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


    def writeItem(self, address : int, plmid, ammoAmount = b"\x00"):
        if len(plmid) != 2 or len(ammoAmount) != 1:
            raise Exception(f'plmid length ({len(plmid)}) must be 2 and ammoAmount length ({len(ammoAmount)}) must be 1')
        self.writeBytes(address, plmid)
        self.writeBytes(address+5, ammoAmount)


    def finalizeRom(self):
        if self.romWriterType == RomWriterType.file:
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

    def setBaseFilename(self, baseFilename : str):
        self.baseFilename = baseFilename

    def getBaseFilename(self) -> str:
        return self.baseFilename
