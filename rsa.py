# Code that uses RSA algorithm to encrypt a message
# Recieves a message from the user, generates a public key and a private key
# Encrypts and decrypts the message, generates and verifies a signature

import random
import math

# Function that verifies if a number is prime
# Returns True or False
def is_Prime(number):
    if number < 2:
        return False
    for i in range(2, (number // 2) + 1):
        if number % i == 0:
            return False
        
    return True


# Function to generate a prime
# Recieves a min and max value and keeps generating
# a random number until is a prime number
# Returns the prime number
def generate_Prime(min_Value, max_Value):
    prime = random.randint(min_Value, max_Value)
    while not is_Prime(prime):
        prime = random.randint(min_Value, max_Value)

    return prime

# Function that generates the private key
# Recieves the public key and the phi of n and generates a private key
# so that (private key)*(public key) mod phi == 1
# Returns the private key or an error message
def mod_Inverse(public_Key, phi):
    for private_Key in range(3, phi):
        if (private_Key * public_Key) % phi == 1:
            return private_Key

    raise ValueError("mod_inverse does not exist")

# Function that generates the public key, private key and n
# Generates two primes(p and q) and calculates n(n = p * q)
# Calculates phi of n(phi_n = (p - 1)*(q - 1))
# Generates the public key and verifies if public key and phi_n are coprimes
# Generates the private key
# Returns the public key, private key and n
def generate_Keys():
    p = generate_Prime(1000, 5000)
    q = generate_Prime(1000, 5000)
    while p == q:
        q = generate_Prime(1000, 5000)
    n = p * q
    phi_n = (p - 1)*(q - 1)
    public_Key = random.randint(3, phi_n - 1)
    while math.gcd(public_Key, phi_n) != 1:
        public_Key = random.randint(3, phi_n - 1)
    private_Key = mod_Inverse(public_Key, phi_n)

    return [public_Key, private_Key, n]

# Function that transforms the message in unicode
# Returns the message an array
def message_To_Unicode(message):
    message_encoded = [ord(ch) for ch in message]

    return message_encoded

# Function that transforms the unicode to letters/numbers
# Returns the message in a string
def unicode_To_Message(message):
    message = "".join(chr(ch) for ch in message)

    return message

# Function that encrypts the message
# message^public_Key mod n
# Returns the encrypted message
def encrypt_Message(message, public_Key, n):
    cipher_Text = [pow(ch, public_Key, n) for ch in message]
    return cipher_Text

# Function that decrypts the message
# message^private_Key mod n
# Returns the decrypted message(in unicode)
def decrypt_Message(cipher_Text, private_Key, n):
    message = [pow(ch, private_Key, n) for ch in cipher_Text]

    return message

# Function that signs the message
# message^private_Key mod n
# Returns the signature
def sign_Message(message, private_Key, n):
    signature = [pow(ch, private_Key, n) for ch in message]

    return signature

# Function that verifies if the signature is legitimate
# Calculates signature^public_Key mod n
# Verifies if is equal to message
# Returns True of False
def check_Signature(signature, message, public_Key, n):
    value = [pow(ch, public_Key, n) for ch in signature]
    if value == message:
        return True
    
    return False

print("Enter your message:")
message = message_To_Unicode(input())

keys = generate_Keys()
public_Key = keys[0]
private_Key = keys[1]
n = keys[2]
signature = sign_Message(message, private_Key, n)
cipher_Text = encrypt_Message(message, public_Key, n)
print("Encrypted message: ", cipher_Text)
message = decrypt_Message(cipher_Text, private_Key, n)
if(check_Signature(signature, message, public_Key, n)):
    print("Signature is valid!")
print("Decrypted message: ", unicode_To_Message(message))