### py_patcher - patcher for binary files

This is a python version of `FirmwarePatcher`.

The original AlexWhiter's `FirmwarePatcher` can patch Garmin firmware to
remove jnx map restrictions. It's a windows program without source code.

It does a few things:

- Apply a patch itself. Patches are written as standard regular expressions
for data in hex representation and can be easily extracted from the program
code (something like windows ini file is needed). An additional file defs.txt
is available, with fixed patch for Garmin 66.

- Increase firmware version (optional). This may be needed because
update is only possible to a higher version.

- Change firmware about page (optional).

- Update file checksum.

The `py_patcher` script can only apply patch and update checksum. The
patch is applied by using standard python re module. The checksum is
calculated correctly for most tested original firmware files and all patch
variants produced by FirmwarePatcher, but I'm still not sure about
this calculation. Version increase is not implemented, it requires not
trivial modifications in different parts of the file.

At the moment I do not think that this script is any better and safer
then `FirmwarePatcher`. It works with exactly same patches, it can not
increase version, it was written without deep understanding of firmware
structure. Obviously, there is no guarantee that patches will work.

### Script usage

```
py_patcher [-F <patch_file> ] [-p <patch_name>] [--no_cs] [--force] <in file> [<out_file>]
```

Script reads `<in file>` and verifies checksum (unless `--no_cs` is given).
If checksum verification fails the script stops (unless `--force` option is given).
If `-F <patch_file>` option is given then patches are read and applied to the data.
With `-p <patch_name>` option one can select a specific patch.
If `<out_file>` is given and at least one patch can be applied then result is
written to the file.

### Test on a few gcd files

```
name                                CS  P1 PN       CMP
-------------------------------------------------------
Alpha100_860                        OK  +  Base15   +
Astro320_460                        OK  +  Base15   +
Atemos100_330                       OK  +  Base15   +
ColoradoTWN_WebupdaterGCDfile__330  OK  -  -
Colorado_WebUpdater__370            OK  +  Base01   +
D2Charlie_610                       OK  +  Added09  +
DakotaTWN_WebupdaterGCDfile__210    OK  -  -
Dakota_WebUpdater__580              OK  -  Base03   +
DriveSmart61_680               WRONG(!) +  Base20
Edge510_610                         OK  +  Base07   +
Edge605_705_330                     OK  -  -
Edge800_270                         OK  +  Base03   +
Edge810_630                         OK  +  Base07   +
Edge830_500                         OK  -  -
EpixSystem_WebUpdater__360          OK  +  Base18   +
eTrex20_30_Webupdater__490          OK  +  Base15   +
eTrex20x_30x_Webupdater__300        OK  +  Base15   +
eTrex22x_32x_Webupdater__270        OK  +  Base15   +
GPSMAP276cx_580                     OK  +  Base16   +
GPSMAP62_78_730                     OK  +  Base14   +
GPSMAP62sc_62stc_WebUpdater__530    OK  +  Base15   +
GPSMAP64sx_WebUpdater__310          OK  +  Base16   +
GPSMAP64_WebUpdater__660            OK  +  Base16   +
GPSMAP66_WebUpdater__960            OK  +  Added13  +
Montana610_680_350                  OK  +  Base15   +
Montana_WebUpdater__760             OK  +  Base15   +
NordicRino650_WebUpdater__270       OK  +  Base05   +
Oregon6x0_WebUpdater__560           OK  +  Base16   +
Oregon7xx_WebUpdater__600           OK  +  Base21   +
Oregonx50_WebUpdater__660           OK  +  Base08   +
Rino700_WebUpdater__250             OK  -  -
Rino7xxGMRS_WebUpdater__510         OK  +  Base16   +
Rino7xx_WebUpdater__510             OK  +  Base16   +

CS -- checksum calculation with patcher.py in the original file
P1 -- patchable with original FirmwarePatcher.exe
PN -- patch name which matches the file
PN -- patch name detected by patcher.py
CMP -- compare patched files produced by FirmwarePatcher.exe
      (no name and version change) and patcher.py

(!) -- File contains extra 261 bytes at the end. FirmwarePatcher
detects and removes them, patcher.py can't.
```

### some useful tricks for etrex 22x (could be useful for other models)

Broken jnx map can prevent device from booting and connecting via usb.
It's better to put strange jnx maps on external sd card (it can be removed).

This can be fixed with a special key binding: turn off the device; press
and hold joystick in up position; connect usb. The device will connect
as a mass storage without loading maps.

There is another special binding for resetting device (NOT useful for
the broken map problem): turn off; press and hold menu and enter
(joystick), turn on and wait until reset menu appears; confirm reset in
the menu.

For updating firmware put the new file to the device as
`Garmin/gupdate.gcd`. Some instructions say `Garmin/GUPDATE.gcd` but
this does not work for me.

An important firmware patching instructions and links (in RU):
https://docs.nakarte.me/garmin.html


#### slazav, 12.2024
