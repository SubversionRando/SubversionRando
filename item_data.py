from typing import Iterable

Item = tuple[str, bytes, bytes, bytes, bytes]
""" Name, Visible, Chozo, Hidden, AmmoQty """


class Items:
    Missile = ("Missile",
               b"\xdb\xee",
               b"\x2f\xef",
               b"\x83\xef",
               b"\x00")
    Super = ("Super Missile",
             b"\xdf\xee",
             b"\x33\xef",
             b"\x87\xef",
             b"\x00")
    PowerBomb = ("Power Bomb",
                 b"\xe3\xee",
                 b"\x37\xef",
                 b"\x8b\xef",
                 b"\x00")
    Morph = ("Morph Ball",
             b"\x23\xef",
             b"\x77\xef",
             b"\xcb\xef",
             b"\x00")
    GravityBoots = ("Gravity Boots",
                    b"\x40\xfd",
                    b"\x40\xfd",
                    b"\x40\xfd",
                    b"\x00")
    Speedball = ("Speed Ball",
                 b"\x03\xef",
                 b"\x57\xef",
                 b"\xab\xef",
                 b"\x00")
    Bombs = ("Bombs",
             b"\xe7\xee",
             b"\x3b\xef",
             b"\x8f\xef",
             b"\x00")
    HiJump = ("HiJump",
              b"\xf3\xee",
              b"\x47\xef",
              b"\x9b\xef",
              b"\x00")
    GravitySuit = ("Gravity Suit",
                   b"\x0b\xef",
                   b"\x5f\xef",
                   b"\xb3\xef",
                   b"\x00")
    DarkVisor = ("Dark Visor",
                 b"\xb0\xfd",
                 b"\xb0\xfd",
                 b"\xb0\xfd",
                 b"\x00")
    Wave = ("Wave Beam",
            b"\xfb\xee",
            b"\x4f\xef",
            b"\xa3\xef",
            b"\x00")
    SpeedBooster = ("Speed Booster",
                    b"\xf7\xee",
                    b"\x4b\xef",
                    b"\x9f\xef",
                    b"\x00")
    Spazer = ("Spazer",
              b"\xff\xee",
              b"\x53\xef",
              b"\xa7\xef",
              b"\x00")
    Varia = ("Varia Suit",
             b"\x07\xef",
             b"\x5b\xef",
             b"\xaf\xef",
             b"\x00")
    Ice = ("Ice Beam",
           b"\xef\xee",
           b"\x43\xef",
           b"\x97\xef",
           b"\x00")
    Grapple = ("Grapple Beam",
               b"\x17\xef",
               b"\x6b\xef",
               b"\xbf\xef",
               b"\x00")
    MetroidSuit = ("Metroid Suit",
                   b"\x20\xfe",
                   b"\x20\xfe",
                   b"\x20\xfe",
                   b"\x00")
    Plasma = ("Plasma Beam",
              b"\x13\xef",
              b"\x67\xef",
              b"\xbb\xef",
              b"\x00")
    Screw = ("Screw Attack",
             b"\x1f\xef",
             b"\x73\xef",
             b"\xc7\xef",
             b"\x00")
    Hypercharge = ("Hypercharge",
                   b"\x80\xf7",
                   b"\x80\xf7",
                   b"\x80\xf7",
                   b"\x00")
    Charge = ("Charge Beam",
              b"\xeb\xee",
              b"\x3f\xef",
              b"\x93\xef",
              b"\x00")
    Xray = ("X-Ray Scope",
            b"\x0f\xef",
            b"\x63\xef",
            b"\xb7\xef",
            b"\x00")
    SpaceJump = ("Space Jump",
                 b"\x1b\xef",
                 b"\x6f\xef",
                 b"\xc3\xef",
                 b"\x00")
    Energy = ("Energy Tank",
              b"\xd7\xee",
              b"\x2b\xef",
              b"\x7f\xef",
              b"\x00")
    Refuel = ("Refuel Tank",
              b"\x27\xef",
              b"\x7b\xef",
              b"\xcf\xef",
              b"\x00")
    SmallAmmo = ("Small Ammo",
                 b"\x00\xf9",
                 b"\x04\xf9",
                 b"\x08\xf9",
                 b"\x05")
    LargeAmmo = ("Large Ammo",
                 b"\x00\xf9",
                 b"\x04\xf9",
                 b"\x08\xf9",
                 b"\x0a")
    # TODO: are damage amp and accel charge swapped?
    # when spoiler says damage amp, it's accel charge
    # when spoiler says charge amp, it's damage amp
    DamageAmp = ("Damage Amp",
                 b"\xa0\xf0",
                 b"\xa0\xf0",
                 b"\xa0\xf0",
                 b"\x00")
    AccelCharge = ("Accel Charge",
                   b"\x7e\xf8",
                   b"\x7e\xf8",
                   b"\x7e\xf8",
                   b"\x00")
    SpaceJumpBoost = ("Space Jump Boost",
                      b"\xc0\xfc",
                      b"\xc0\xfc",
                      b"\xc0\xfc",
                      b"\x00")
    spaceDrop = ("Space Drop", b"", b"", b"", b"")


items_unpackable: Iterable[Item] = (
    Items.Missile, Items.Super, Items.PowerBomb, Items.Morph, Items.GravityBoots, Items.Speedball, Items.Bombs,
    Items.HiJump, Items.GravitySuit, Items.DarkVisor, Items.Wave, Items.SpeedBooster, Items.Spazer, Items.Varia,
    Items.Ice, Items.Grapple, Items.MetroidSuit, Items.Plasma, Items.Screw, Items.Hypercharge, Items.Charge,
    Items.Xray, Items.SpaceJump, Items.Energy, Items.Refuel, Items.SmallAmmo, Items.LargeAmmo, Items.DamageAmp,
    Items.AccelCharge, Items.SpaceJumpBoost, Items.spaceDrop
)

all_items: dict[str, Item] = {
    item[0]: item
    for item in items_unpackable
}
