def xor(key, data):
	result = bytearray(len(data))
	
	keyLength = len(key)
	for i, byte in enumerate(data):
		result[i] = byte ^ key[i % keyLength]

	return result

def rc4(key, data):
	S = bytearray(range(256))
	
	j = 0
	keyLength = len(key)
	for i in range(256):
		j = (j + S[i] + key[i % keyLength]) & 0xFF
		S[i], S[j] = S[j], S[i]

	i = 0
	j = 0
	result = bytearray(len(data))
	for k, byte in enumerate(data):
		i = (i + 1) & 0xFF
		j = (j + S[i]) & 0xFF
		S[i], S[j] = S[j], S[i]
		result[k] = byte ^ S[(S[i] + S[j]) & 0xFF]

	return result