# Python
import binascii

data = b"hello world"
hex_str = binascii.hexlify(data).decode()
print(hex_str)

original = binascii.unhexlify(hex_str).decode()
print(original)

num = 255
print(f"0x{num:02x}")
