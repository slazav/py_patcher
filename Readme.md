### py_patcher - patcher for binary files

The original AlexWhiter's `FirmwarePatcher` can patch Garmin firmware to
remove jnx map restrictions. It's a windows program without source code.

It does a few things:

- Apply a patch itself. Patches are written as standard regular expressions
for data in hex representation and can be easily extracted from the program
code (something like windows ini file is needed).

- Increase firmware version (optional). This may be needed because
update is only possible to a higher version.

- Change firmware name (optional).

- Update file checksum.

The `py_patcher` script can only apply patch and update checksum. The
patch is applied by using standard python re module. The checksum is
calculated correctly for a few original firmware files and a few patch
variants produced by FirmwarePatcher, but I'm still not sure about
this calculation. Version increase is not implemented, it requires not
trivial modifications in different parts of the file.

At the moment I do not think that this script is any better then
`FirmwarePatcher`. It works with exactly same patches, it can not
increase version, it was written without deep understanding of firmware
structure. Obviously, there is no guarantee that patches will work.
With this script I was able to produce a valid patch for my etrex 22x.

### script usage

```
py_patcher [-p <name>] [-no_cs] [-force] <patch file> <in file> [<out_file>]
```

Patch file is a "windows ini" file with patches. If only `<patch file>`
and `<in file>` arguments are given than all patches are listed and
tested with the input file. If `<out_file>` is given the result of the
last successful patch will be written there.

With `-p` option one can select a specific patch name.

With `-no_cs` option control sum is not calculated, tested or updated.

With `-force` option the patch will be applied even if the control sum
of the original file is incorrect.

### some useful tricks with etrex 22x

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
