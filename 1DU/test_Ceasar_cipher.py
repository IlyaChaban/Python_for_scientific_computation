from Ceasar_cipher import caesar_decrypt
from Ceasar_cipher import caesar_encrypt
from Ceasar_cipher import MESSAGE, KEY, TABLE
import random

def test_basic_test():
    assert caesar_encrypt(MESSAGE, TABLE, KEY)=='epaopuafbuabmmanzapsbohft'

def test_test2():
    message = 'hello'
    table = 'helo'
    key = -5
    assert caesar_encrypt(message,table,key) == 'oheel'

def test_answer():
    assert caesar_decrypt(caesar_encrypt(MESSAGE, TABLE, KEY), TABLE, KEY) == MESSAGE

def test_random_test():
    for i in range(-1000,1001,1):
        RandomStringSize = random.randint(1, 50)
        temp_message = ''.join(random.choice(TABLE) for i in range(RandomStringSize))
        #print(temp_message)
        #print(caesar_decrypt(caesar_encrypt(temp_message, TABLE, i), TABLE, i))
        assert caesar_decrypt(caesar_encrypt(temp_message, TABLE, i), TABLE, i) == temp_message