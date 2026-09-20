import os

from utils import ByteStream, Encryption


def main(fileName, lv1_string_encryption_decryption_keyOffset, lv1_string_encryption_read_ranges_range_tableOffset):
	fileBaseName, fileExtension = os.path.splitext(fileName)
	decryptedStringCount = 0

	stream = ByteStream(open(fileName, "rb").read())

	stream.offset = lv1_string_encryption_decryption_keyOffset
	lv1_string_encryption_decryption_key = stream.readBytes(128)

	stream.offset = lv1_string_encryption_read_ranges_range_tableOffset
	with open(f"{fileBaseName}_dump.txt", "w") as dumpFile:
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
			
			endOffset = stream.offset
			stream.offset = offset
			
			value = Encryption.xor(lv1_string_encryption_decryption_key, stream.readBytes(length))
			stream.buffer[offset:offset + length] = value
			dumpFile.write(f"{hex(offset)} {bytes(value)}\n")
			decryptedStringCount += 1
			
			stream.offset = endOffset
			v1, v2, v3 = v4, v5, v6

	with open(f"{fileBaseName}_decrypted{fileExtension}", "wb") as decryptedFile:
		decryptedFile.write(stream.buffer)

	print(f"Decrypted {decryptedStringCount} strings")

if __name__ == "__main__":
	""" Templates(withcorrect offsets):
	fileName = "bs_v29.258_arm32_libg.so"
	lv1_string_encryption_decryption_keyOffset = 0xA64106
	lv1_string_encryption_read_ranges_range_tableOffset = 0x908584

	fileName = "bs_v29.270_arm64_libg.so"
	lv1_string_encryption_decryption_keyOffset = 0xD97FEF
	lv1_string_encryption_read_ranges_range_tableOffset = 0xA67F10

	fileName = "bs_v29.274_ios"
	lv1_string_encryption_decryption_keyOffset = 0x275C0F3
	lv1_string_encryption_read_ranges_range_tableOffset = 0x2846610

	fileName = "bs_v36.218_arm64_libg.so"
	lv1_string_encryption_decryption_keyOffset = 0x1057EAC
	lv1_string_encryption_read_ranges_range_tableOffset = 0x101A7E4
	"""
	fileName = "bs_v29.270_arm64_libg.so"
	lv1_string_encryption_decryption_keyOffset = 0xD97FEF
	lv1_string_encryption_read_ranges_range_tableOffset = 0xA67F10
	
	main(fileName, lv1_string_encryption_decryption_keyOffset, lv1_string_encryption_read_ranges_range_tableOffset)