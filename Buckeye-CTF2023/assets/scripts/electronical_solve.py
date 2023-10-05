import requests
from urllib.parse import quote

# Url used in the challenge
base_url = "https://electronical.chall.pwnoh.io/encrypt?message="

def findOneByte(payload, knownBytes):
    # Getting the base ciphertext
    url = base_url + quote(payload, safe="")
    r = requests.get(url)
    cipherUnknown = r.text

    # Setting up a loop running from ! to ~, which are all of the bytes that may be in the flag.
    for i in range(33,0x7f):
        # Crafting a payload to test the next byte of the flag
        byteToAdd = bytes([i])
        payloadTest = payload + knownBytes + byteToAdd

        # Getting the bruteforced ciphertext
        urlToTest = base_url + quote(payloadTest, safe="")
        rTest = requests.get(urlToTest)
        cipherTest = rTest.text

        print(f"Trying with {byteToAdd}")
        # Checking if the first 4 blocks are the same (as the ciphertext is hexlified, we check 2 times the length of the ciphertext, so 4*16*2 = 128)
        if cipherTest[:128] == cipherUnknown[:128]:
            # Found next byte! Concenating it to the end of the flag, removing one A from the payload, and breaking the loop
            print(f'Found byte : {byteToAdd}')
            payload = payload[1:]
            knownBytes += byteToAdd
            break
    
    # Returning current state of the payload and the flag
    return payload, knownBytes

# Setting the payload to 63 times A. This means we will check the first 4 blocks, as 64/16 = 4
payload = b'A' * 63
knownBytes = b''

# Looping while the payload is not empty or we find the end of the flag, represented by the } character
while b'A' in payload and b'}' not in knownBytes:
    # Finding one byte of the flag
    payload, knownBytes = findOneByte(payload, knownBytes)
    # Printing current state of the flag
    print(f'Flag = {knownBytes}')

