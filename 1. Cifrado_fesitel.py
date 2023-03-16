
def hex_to_bin(hex_val: str) -> str:
    # Convierte un caracter hexadeciamal a binario
    decimal_val = int(hex_val, 16)
    binary_val = bin(decimal_val)[2:]
    return binary_val

def complete_binary(binary: str, size_binary: int) -> str:
    # Completa un numero binario al tamaño deseado
    return binary.zfill(size_binary)

def generate_key(iterations: int) -> list:
    # Generar todas las claves de un caracter de 8 bits en binario = 256
    keys = []
    for i in range(iterations):
        key = format(i, '08b')
        keys.append(key)
    return keys

def generateSubKeys(cantRotate: int, keyMain: str, address: str = "r") -> list:
    return [subKey[4:] for subKey in [keyMain[i:] + keyMain[:i] if address == "r" and i < 0 else keyMain[i+1:] + keyMain[:i+1] 
            if address == "l" else keyMain[i+1:] + keyMain[:i+1]  for i in range(cantRotate)]]

def xor(a, b):
    a = int(a)
    b = int(b)
    return int((a and not b) or (not a and b))

def cifrado_feistel(msg_character: str, sub_keys: list):
    left = msg_character[:4]
    rigth = msg_character[4:]

    # rigth = msg_character[:4]
    # left = msg_character[4:]
    
    char_desencrypt = []
    for ronda in range(7, -1, -1):
        par_xor = list(zip(list(rigth), list(sub_keys[ronda])))
        # import pdb; pdb.set_trace() 
        char_desencrypt = [xor(par[0],par[1]) for par in par_xor]

        par_xor_desencrypt = list(zip(list(left), char_desencrypt))
        xor_left_fun = [xor(par[0],par[1]) for par in par_xor_desencrypt]

        # rigth = left
        # left = new_rigth

        left = rigth
        rigth = xor_left_fun
    
    
    result = [str(ent) for ent in [*rigth, *left]]
    return "".join(result)

if __name__ == "__main__":
    msg_hex = ['ab','49','72','7e','22','64','6f','63','68','22','77','69','75','22','62','63','74','65','6f','60','75','67','75','23']
    msg_bin = [complete_binary(hex_to_bin(value), 8) for value in msg_hex]
    keys = generate_key(256)
    # import pdb; pdb.set_trace()
    for key in keys:
        result = ''
        sub_keys = generateSubKeys(8, key, 'r')
        for msg_character in msg_bin:
            char_bin = cifrado_feistel(msg_character, sub_keys)
            char_decimal = int(char_bin, 2)
            char = chr(char_decimal)
            result += char
            # print(len(result))

        print(result, "\n___________________")

