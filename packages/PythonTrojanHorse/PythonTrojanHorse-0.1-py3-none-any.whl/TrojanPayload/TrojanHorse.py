class Trojan: 
	def main():
		return 0

	def Encrypt(self, data):
		s=7 #shift
		cipher = ""
		
		for char in data:
			#uppercase letter
			if(char.isupper()):
				cipher += chr((ord(char) + s-65) % 26 + 65)
			#lowercase letter
			elif(char.islower()):
				cipher += chr((ord(char) + s-97) % 26 + 97)
			#non-letter characters are kept the same
			else:
				cipher += char
		return cipher

	def Decrypt(self, cipher):
		s=7 #shift
		data = ""
		
		for char in cipher:
			#uppercase letters
			if(char.isupper()):
				data += chr((ord(char) - s-65) % 26 + 65)
			#lowercase letters
			elif(char.islower()):
				data += chr((ord(char) - s-97) % 26 + 97)
			#non-letter characters are kept the same
			else:
				data += char
		return data

	def Hash(self, data):
		hash_size = 20  # fixed size of hash value
		hash_value = ""
		salt = 'asdfghjklpoiuytrewqzxcvbnm1234567890'
		#check the length of input data
		if len(data) <= hash_size:   
			add_len = hash_size - len(data) # length of the salt to be added
			hash_value = salt[0:(add_len//2)] + data + salt[(add_len//2):]
			hash_value = hash_value[:20]
		else:
			hash_value = data[:20]
		return hash_value


	