def hex_to_bin(hex_val: str) -> str:
    # Convierte un caracter hexadeciamal a binario
    decimal_val = int(hex_val, 16)
    binary_val = bin(decimal_val)[2:]
    return binary_val

def complete_binary(binary: str, size_binary: int) -> str:
    # Completa un numero binario al tamaño deseado
    return binary.zfill(size_binary)

def generateSubKeys(cantRotate: int, keyMain: str, address: str = "r") -> list:
    return [subKey[4:] for subKey in [keyMain[i:] + keyMain[:i] if address == "r" and i < 0 else keyMain[i+1:] + keyMain[:i+1] 
            if address == "l" else keyMain[i+1:] + keyMain[:i+1]  for i in range(cantRotate)]]
        
def xor(a, b):
    a = int(a)
    b = int(b)
    return int((a and not b) or (not a and b))

def cifrado(msg_character: str, sub_keys: list):
    left = msg_character[:4]
    rigth = msg_character[4:]
    
    for ronda in range(0, 7):
        par_xor = list(zip(list(rigth), list(sub_keys[ronda])))
        char_desencrypt = [xor(par[0],par[1]) for par in par_xor]

        par_xor_desencrypt = list(zip(list(left), char_desencrypt))
        xor_left_fun = [xor(par[0],par[1]) for par in par_xor_desencrypt]

        left = rigth
        rigth = xor_left_fun
    
    result = [str(ent) for ent in [*left, *rigth]]
    return "".join(result)

def descifrado(msg_character: str, sub_keys: list):
    left = msg_character[:4]
    rigth = msg_character[4:]
    
    for ronda in range(6, -1, -1):
        par_xor = list(zip(list(left), list(sub_keys[ronda])))
        char_encrypt = [xor(par[0],par[1]) for par in par_xor]

        par_xor_encrypt = list(zip(list(rigth), char_encrypt))
        xor_rigth_fun = [xor(par[0],par[1]) for par in par_xor_encrypt]

        rigth = left
        left = xor_rigth_fun

    result = [str(ent) for ent in [*left, *rigth]]
    return "".join(result)

if __name__ == "__main__":
    msg = 'hola'
    msg_ascii = [104,111,108,97]
    msg_decimal_hexadecimal = [hex(char).lstrip('0x') for char in msg_ascii]
    msg_bin = [complete_binary(hex_to_bin(value), 8) for value in msg_decimal_hexadecimal]
    key = '10101010'
    sub_keys = generateSubKeys(8, key, 'r')

    result = []
    result_binari = []
    for msg_character in msg_bin:
        char_bin = cifrado(msg_character, sub_keys)
        result_binari.append(char_bin)
        char_decimal = int(char_bin, 2)
        result.append(char_decimal)

    print("cifrado: ", result)

    # Descifrado
    decrypted_result = []
    decrypted_binari = []
    for msg_character in result_binari:
        char_bin = descifrado(msg_character, sub_keys)
        decrypted_binari.append(char_bin)
        char_decimal = int(char_bin, 2)
        decrypted_result.append(char_decimal)

    print("descifrado: ", decrypted_result)

    # Convertir los valores decimales descifrados a caracteres
    decrypted_msg = ''.join([chr(char) for char in decrypted_result])
    print("mensaje descifrado: ", decrypted_msg)

