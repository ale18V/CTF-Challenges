import os


seed = int.from_bytes(os.urandom(6), byteorder='little', signed=False)
a_value = 25214903917
c_value = 11
m_value = 2**48

password = os.urandom(16).hex()
flag = "flag{Time traveling is easier than you thought!}"
