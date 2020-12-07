# from Crypto.Cipher import AES
# from Crypto.Hash import SHA256

# password = ("anything")
# hash_obj = SHA256.new(password.encode('utf-8'))
# hkey = hash_obj.digest()

# def encrypt(info):
#     msg = info
#     BLOCK_SIZE = 16
#     PAD = "{"
#     padding = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PAD
#     cipher = AES.new(hkey, AES.MODE_ECB)
#     result = cipher.encrypt(padding(msg).encode('utf-8'))
#     return result

# msg = "Hello stackoverflow!"
# cipher_text = encrypt(msg)
# print(cipher_text)
# print(type(cipher_text))

# def decrypt(info):
#     msg = info
#     PAD = "{"
#     decipher = AES.new(hkey, AES.MODE_ECB)
#     pt = decipher.decrypt(msg).decode('utf-8')
#     pad_index = pt.find(PAD)
#     result = pt[: pad_index]
#     return result

# plaintext = decrypt(cipher_text)
# print(plaintext)

# hash password
# import basehash

# hash_fn = basehash.base36()  # you can initialize a 36, 52, 56, 58, 62 and 94 base fn
# hash_value = hash_fn.hash("gggga") # returns 'M8YZRZ'
# unhashed = hash_fn.unhash('M8YZRZ') # returns 1

import bcrypt
passw="super secret password"
password = bytes(passw, encoding='utf-8')

# Hash a password for the first time, with a randomly-generated salt
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(type(hashed))
print(hashed)
# Check that a unhashed password matches one that has previously been
#   hashed
if bcrypt.hashpw(password, hashed) == hashed:
    print("It Matches!")
else:
     print("It Does not Match :(")
