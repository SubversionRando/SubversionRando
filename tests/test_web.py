import os
from pathlib import Path


def get_pyscript_file_list(html_file_path: Path) -> list[str]:
    with open(html_file_path) as html_file:
        file_text = html_file.read()
    list_start = file_text.index("files = [") + 10
    list_close = file_text.index("]", list_start)
    list_end = file_text.rindex("\n", list_start, list_close)
    file_lines = file_text[list_start:list_end].splitlines()
    file_names = [line.strip(' ",') for line in file_lines]
    print(file_names)
    for name in file_names:
        assert name.startswith("subversion_rando/"), f"{name=}"
    return file_names


def test_web_file_list() -> None:
    repo_root = Path(__file__).parent.parent
    html_file_path = repo_root.joinpath("index.html")
    package_root = repo_root.joinpath("src", "subversion_rando")

    html_file_list = get_pyscript_file_list(html_file_path)

    no_need = {
        "__pycache__",
        "objective_rando.asm",
        "rom_room_names.py",
        "py.typed"
    }

    dir_list: list[str] = []
    for dir_entry in os.listdir(package_root):
        # print(dir_entry)
        if dir_entry not in no_need:
            dir_list.append(f"subversion_rando/{dir_entry}")
            if dir_list[-1] not in html_file_list:
                print(f"{dir_entry} not in html list")

    dir_list.sort()
    assert len(dir_list) == len(html_file_list), f"{len(dir_list)=} {len(html_file_list)=}"

    for i in range(len(dir_list)):
        assert dir_list[i] == html_file_list[i], f"{i=} {dir_list[i]=} {html_file_list[i]=}"


if __name__ == "__main__":
    test_web_file_list()
