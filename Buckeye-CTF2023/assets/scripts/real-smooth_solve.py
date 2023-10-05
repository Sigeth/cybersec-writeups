from pwn import xor

lines =  open("database.txt", "r").readlines()

soloLines = []
for line in lines:
    if line[-3:-1] != '48' and line[-1] == '\n':
        soloLines.append(line[:-1])
print(soloLines)


c1 = bytes.fromhex(soloLines[0])
c2 = bytes.fromhex(lines[0])
xored_ciphers = xor(c1, c2)
xorKnownPlaintext = xor(xored_ciphers, b'btcf{')
print(xorKnownPlaintext)

xorKnownPlaintext = xor(xored_ciphers, b'btcf{0000000000000')
print(xorKnownPlaintext)

xorKnownPlaintext = xor(xored_ciphers, b'btcf{n000000000000')
print(xorKnownPlaintext)

xorKnownPlaintext = xor(xored_ciphers, b'btcf{w000000000000')
print(xorKnownPlaintext)

xorKnownPlaintext = xor(xored_ciphers, b'frozen\n           ')
print(xorKnownPlaintext)


c1 = bytes.fromhex(soloLines[0])
c2 = bytes.fromhex(soloLines[1])
xored_ciphers = xor(c1, c2)
xorKnownPlaintext = xor(xored_ciphers, b'btcf{w3_d0_4_l177l')
print(xorKnownPlaintext)
