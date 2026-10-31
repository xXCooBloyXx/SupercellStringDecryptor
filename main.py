import os

from utils import ByteStream, Encryption


def main(fileName, lv1_string_encryption_decryption_keyOffset, lv1_string_encryption_read_ranges_range_tableOffset):
	stream = ByteStream(open(fileName, "rb").read())

	stream.offset = lv1_string_encryption_decryption_keyOffset
	lv1_string_encryption_decryption_key = stream.readBytes(128)

	strings = {}
	
	stream.offset = lv1_string_encryption_read_ranges_range_tableOffset
	v1 = stream.readInt32()
	v2 = stream.readInt32()
	v3 = stream.readInt32()
	while True:
		v4 = stream.readInt32()
		v5 = stream.readInt32()
		v6 = stream.readInt32()
		
		offset = (v4 - v1 - v2 - v3 + lv1_string_encryption_read_ranges_range_tableOffset) & 0xFFFFFFFF
		length = (v2 + v4 - v5) & 0xFFFFFFFF
		if length == 0:
			break
		
		decryptedValue = Encryption.xor(lv1_string_encryption_decryption_key, stream.buffer[offset:offset + length])
		stream.buffer[offset:offset + length] = decryptedValue
		strings[offset] = decryptedValue
		
		v1, v2, v3 = v4, v5, v6

	fileBaseName, fileExtension = os.path.splitext(fileName)
	with open(f"{fileBaseName}_decrypted{fileExtension}", "wb") as decryptedFile:
		decryptedFile.write(stream.buffer)
	
	with open(f"{fileBaseName}_dump.txt", "w") as dumpFile:
		dumpFile.writelines(f"{hex(offset)} {name}\n" for offset, name in strings.items())

	print(f"Decrypted {len(strings)} strings")

if __name__ == "__main__":
	fileName = "bs_v29.270_arm64_libg.so"
	lv1_string_encryption_decryption_keyOffset = 0xD97FEF
	lv1_string_encryption_read_ranges_range_tableOffset = 0xA67F10
	
	main(fileName, lv1_string_encryption_decryption_keyOffset, lv1_string_encryption_read_ranges_range_tableOffset)