
from .romWriter import RomWriter, RomWriterType


class TerrainWriter:
    empty_space: int
    rom_writer: RomWriter

    def __init__(self, rom_writer: RomWriter) -> None:
        self.empty_space = 0x2f51c4
        self.rom_writer = rom_writer

    def write(self, data: bytes, indexes_to_point_to_new_data: list[int]) -> None:
        # verify the space is empty
        if self.rom_writer.romWriterType == RomWriterType.file:
            for i in range(len(data)):
                assert self.rom_writer.rom_data[self.empty_space + i] == 0xff

        self.rom_writer.writeBytes(self.empty_space, data)
        p_level_data = RomWriter.index_to_snes_addr(self.empty_space).to_bytes(3, "little")
        # print(f"{p_level_data=}")
        for pointer in indexes_to_point_to_new_data:
            self.rom_writer.writeBytes(pointer, p_level_data)

        self.empty_space += len(data) + 1
