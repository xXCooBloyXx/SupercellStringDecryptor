# Supercell String Decryptor
A tool created for "manual" string decryption in Supercell games

## How to use?
First, you need to find 2 file offsets:
- lv1_string_encryption_decryption_key - the decryption key(always 128 bytes long)
- lv1_string_encryption_read_ranges_range_table - a packed/obfuscated table containing strings offsets and lengths. It is VERY VERY long

You can find them in **the first function of .init_array segment** in your library.
**Important:**
Both values must be file offsets (FOs). Do NOT use the virtual addresses (VAs) that are shown in your disassembler. You need to convert them to file offsets using corresponding segment mapping.

You can also use presets below, but only if your game, version and architecture matches:

| Game, version and architecture | lv1_string_encryption_decryption_keyOffset | lv1_string_encryption_read_ranges_range_tableOffset |
|---|---:|---:|
| Brawl Stars v29.258 arm32 | `0xA64106` | `0x908584` |
| Brawl Stars v29.270 arm64 | `0xD97FEF` | `0xA67F10` |
| Brawl Stars v29.274 ios | `0x275C0F3` | `0x2846610` |
| Brawl Stars v36.218 arm64 | `0x1057EAC` | `0x101A7E4` |

Then you just need to replace 3 variables at the end of script to your fileName and offsets, and simply run the program

## Why?
You might wonder why would this be useful, when there is already an automated alternative((Supercell ArxanUnprotector)[https://github.com/Mimi8298/Supercell.ArxanUnprotector])?
Well, the answer is... it doesnt always work. This is especially noticable in older versions (like Brawl Stars v14 and below), probably due to fact that it uses thumb, although im not entirely sure