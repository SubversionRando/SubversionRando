import json
import os
import tkinter as tk
from tkinter import ttk
from typing import TypedDict
try:
    from typing import Literal
except ImportError:
    input("requires Python 3.9 or higher... press enter to quit")
    exit(1)

try:
    from game import CypherItems, GameOptions
    from gui_scroll_frame import ScrollFrame
    from gui_toggled_frame import ToggledFrame
    import logic_presets
except TypeError:
    input("requires Python 3.9 or higher... press enter to quit")
    exit(1)
from Main import generate, write_rom
from trick import Trick
from trick_data import Tricks


SETTINGS_FILE_NAME = "gui_settings.json"


_trick_to_name = {v: k for k, v in vars(Tricks).items() if isinstance(v, Trick)}


class GuiSettings(TypedDict):
    logic: dict[str, int]


def main() -> None:
    root = tk.Tk()
    logic_frame = ttk.Frame(root, padding=10)
    logic_frame.grid()
    custom_toggle = ToggledFrame(logic_frame, "customize logic")
    custom_toggle.grid(column=0, row=1, columnspan=3)

    custom_logic_frame = ScrollFrame(custom_toggle.sub_frame)
    custom_logic_frame.grid()

    logic_selections: dict[str, tk.IntVar] = {}

    row_i = 0
    for trick_name, trick in vars(Tricks).items():
        if isinstance(trick, Trick):
            logic_selections[trick_name] = tk.IntVar()
            ttk.Checkbutton(
                custom_logic_frame.viewPort, variable=logic_selections[trick_name], text=trick_name
            ).grid(sticky=tk.W, column=0, row=row_i)
            ttk.Label(
                custom_logic_frame.viewPort, text=trick.desc, justify=tk.LEFT, anchor="w", wraplength=150,
                borderwidth=1, relief="solid", padding=2
            ).grid(sticky=tk.W, column=1, row=row_i)
            row_i += 1

    def save_logic() -> None:
        logic_data = {
            k: v.get() for k, v in logic_selections.items()
        }
        data: GuiSettings = {
            "logic": logic_data
        }
        with open(SETTINGS_FILE_NAME, "w") as settings_file:
            json.dump(data, settings_file)

    def load_logic() -> None:
        if os.path.isfile(SETTINGS_FILE_NAME):
            with open(SETTINGS_FILE_NAME) as settings_file:
                content = settings_file.read()
                data: GuiSettings = json.loads(content)
                if isinstance(data, dict) and isinstance(data["logic"], dict):  # type: ignore
                    logic = data["logic"]
                    for k, v in logic.items():
                        if k in logic_selections:
                            if isinstance(v, int):  # type: ignore
                                logic_selections[k].set(v)
                            else:
                                print(f"invalid value in {SETTINGS_FILE_NAME}, {k=}: {v=}")  # type: ignore
                else:
                    print(f"invalid data in {SETTINGS_FILE_NAME}:\n{content}")  # type: ignore

    load_logic()

    def preset_buttons() -> None:
        ROW = 0
        ttk.Label(logic_frame, text="logic preset:").grid(column=0, row=ROW)

        def casual_button_action() -> None:
            for cb in logic_selections.values():
                cb.set(0)
            for t in logic_presets.casual:
                logic_selections[_trick_to_name[t]].set(1)

        casual_button = ttk.Button(logic_frame, text="casual", command=casual_button_action)
        casual_button.grid(column=1, row=ROW)

        def medium_button_action() -> None:
            for cb in logic_selections.values():
                cb.set(0)
            for t in logic_presets.medium:
                logic_selections[_trick_to_name[t]].set(1)

        medium_button = ttk.Button(logic_frame, text="medium", command=medium_button_action)
        medium_button.grid(column=2, row=ROW)

        def expert_button_action() -> None:
            for cb in logic_selections.values():
                cb.set(0)
            for t in logic_presets.expert:
                logic_selections[_trick_to_name[t]].set(1)

        expert_button = ttk.Button(logic_frame, text="expert", command=expert_button_action)
        expert_button.grid(column=3, row=ROW)

    preset_buttons()

    area_rando_value = tk.IntVar()

    ttk.Checkbutton(
        logic_frame, variable=area_rando_value, text="area rando"
    ).grid(sticky=tk.E, column=0, row=2)

    small_spaceport_value = tk.IntVar()
    small_spaceport_value.set(1)

    ttk.Checkbutton(
        logic_frame, variable=small_spaceport_value, text="small spaceport"
    ).grid(sticky=tk.E, column=1, row=2)

    escape_shortcuts_value = tk.IntVar()

    ttk.Checkbutton(
        logic_frame, variable=escape_shortcuts_value, text="escape shortcuts"
    ).grid(sticky=tk.E, column=2, row=2)

    fill_options: dict[str, Literal['M', 'MM', 'D', 'S', 'B']] = {
        "full random": "D",
        "major/minor bias": "B",
        "major/minor": "MM"
    }

    fill_select = ttk.Combobox(logic_frame)
    fill_select["values"] = tuple(fill_options.keys())
    fill_select.set("full random")
    fill_select.grid(sticky=tk.E, column=3, row=2)

    cypher_label = ttk.Label(logic_frame, text="Thunder Laboratory has:")
    cypher_label.grid(sticky=tk.E, column=0, row=3, columnspan=2)

    cypher_options = {
        "Anything": CypherItems.Anything,
        "Something not required": CypherItems.NotRequired,
        "Small Ammo Tanks": CypherItems.SmallAmmo,
    }

    cypher_select = ttk.Combobox(logic_frame)
    cypher_select["values"] = tuple(cypher_options.keys())
    cypher_select.set("Something not required")
    cypher_select.grid(sticky=tk.W, column=2, row=3, columnspan=2)

    name_label = ttk.Label(logic_frame, text="")
    name_label.grid(column=0, row=5)

    def roll_button_action() -> None:
        save_logic()

        logic: frozenset[Trick] = frozenset([
            getattr(Tricks, trick_name)
            for trick_name in logic_selections
            if logic_selections[trick_name].get()
        ])

        cypher_option = cypher_options[cypher_select.get()]

        options = GameOptions(logic,
                              bool(area_rando_value.get()),
                              fill_options[fill_select.get()],
                              bool(small_spaceport_value.get()),
                              bool(escape_shortcuts_value.get()),
                              cypher_option)
        game = generate(options)
        name = write_rom(game)
        name_label.config(text=name)

    ttk.Button(logic_frame, text="roll", command=roll_button_action).grid(column=1, row=5)

    def on_closing() -> None:
        save_logic()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


if __name__ == "__main__":
    main()
