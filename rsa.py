from modulo_helpers import exponentiationModulo, gcd
import random

# determines the public and private keys from the 2 input prime numbers
def choose_keys(p1 = 31, p2 = 53):
    n = p1 * p2
    phi = (p1 - 1) * (p2 - 1)

    e = random.randrange(2, phi)
    while(True):
        if(gcd(e, phi) == 1):
            break
        e = random.randrange(2, phi)

    # d is the inverse of e in the context of mod phi
    # it was computed using a built in python function, it can also be determined from the extended
    #    euclidean algorithm
    d = pow(e, -1, phi)

    return ({'n': n, 'e': e}, {'n': n, 'd': d})

# map from the english alphabet letters + '_' to their numeric equivalents (0 -> 26)
# to allow encoding letters to numbers
alphabet_map = dict({chr(ord('a') + i - 1): i for i in range(1, 27)}, **{'_' : 0})

# reverse of the previous map to allow decoding numbers back to letters
reverse_alphabet_map = {j : i for (i, j) in alphabet_map.items()}


def encode_block(block, block_size):
    # complete the block with '_' if the block is smaller than the block_size
    if(len(block) < block_size):
        for _ in range(block_size - len(block)):
            block.append('_')

    # encoding the block
    # the base 10 equivalent after mapping the block to a base 27 number using the alphabet map
    code = 0
    for i in range(len(block)):
        code = code + alphabet_map[block[i]] * (len(alphabet_map) ** (len(block) - i - 1))
    
    return code

def decode_code(code, block_size):
    block = []
    
    # decodes the number back to letters 
    # it's actually writing the number is base 27 and then converting each digit to the corresponding letter
    while code > 0:
        block.insert(0, reverse_alphabet_map[code % len(alphabet_map)])
        code = code // len(alphabet_map)

    # complete the block with '_' if the block is smaller than the block_size (prepended, opposite of what was done for encoding)
    if(len(block) < block_size):
        for _ in range(block_size - len(block)):
            block.insert(0, '_')

    return block

def validate_message(message):
    for c in message:
        if(c not in alphabet_map):
            return False
    return True


def encrypt(message, public_key, block_size = 2, ciphertext_block_size = 3):
    # split the message in blocks of size block_size
    if not validate_message(message):
        print("The message is invalid")
        return None

    blocks = [list(message)[i:i+block_size] for i in range(0, len(message), block_size)]

    codes = [encode_block(b, block_size) for b in blocks]
    encrypted_codes = [exponentiationModulo(m, public_key['e'], public_key['n']) for m in codes]
    encrypted_message = ''.join([''.join(decode_code(c, ciphertext_block_size)) for c in encrypted_codes])
    return encrypted_message
    

def decrypt(message, private_key, block_size = 2, ciphertext_block_size = 3):
    # split the message in blocks of size ciphertext_block_size
    blocks = [list(message)[i:i+ciphertext_block_size] for i in range(0, len(message), ciphertext_block_size)]

    codes = [encode_block(b, ciphertext_block_size) for b in blocks]
    decrypted_codes = [exponentiationModulo(c, private_key['d'], private_key['n']) for c in codes]
    decrypted_message = ''.join([''.join(decode_code(c, block_size)) for c in decrypted_codes])
    return decrypted_message

    
message = 'A'
(public_key, private_key) = choose_keys()
encrypted_message = encrypt(message, public_key)

if(encrypted_message is not None):
    print(f'Encrypted message: {encrypted_message}')
    decrypted_message = decrypt(encrypted_message, private_key)
    print(f'Decrypted message: {decrypted_message}')