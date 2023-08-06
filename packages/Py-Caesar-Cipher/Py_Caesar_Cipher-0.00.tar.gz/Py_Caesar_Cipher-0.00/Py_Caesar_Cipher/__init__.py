# __init__.py file

# Caesar Cipher Encryptor & Decryptor 

alphabetLower = 'abcdefghijklmnopqrstuvwxyz'
alphabetUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Numbers = '1234567890'


class Main:
    # Encryption
    def Encrypt(message, key):
        newMessage = ""
        for character in message:
            if character in alphabetLower:          
                position = alphabetLower.find(character)          
                newPosition = (position + key) % 26
                newCharacter = alphabetLower[newPosition]
                newMessage += newCharacter    

            elif character in alphabetUpper:
                position = alphabetUpper.find(character)
                newPosition = (position + key) % 26
                newCharacter = alphabetUpper[newPosition]
                newMessage += newCharacter
  
            elif character in Numbers:
                position = Numbers.find(character)
                newPosition = (position + key) % 10
                newCharacter = Numbers[newPosition]
                newMessage += newCharacter                
      
            else:
                newMessage += character

        return newMessage


# Decryption
    def Decrypt(message, key):
        newMessage = ""
        for character in message:
            if character in alphabetLower:
                position = alphabetLower.find(character)
                newPosition = (position - key) % 26
                newCharacter = alphabetLower[newPosition]
                newMessage += newCharacter    

            elif character in alphabetUpper:
                position = alphabetUpper.find(character)
                newPosition = (position - key) % 26
                newCharacter = alphabetUpper[newPosition]
                newMessage += newCharacter
  
            elif character in Numbers:
                position = Numbers.find(character)
                newPosition = (position - key) % 10
                newCharacter = Numbers[newPosition]
                newMessage += newCharacter
        
            else:
                newMessage += character
      
        return newMessage


    # Brute Force 
    def BruteForce(message):
        i = 0
        while i < 26:
            DecryptMsg = "Key " + str(i) + ": " + str(Main.Decrypt(message, i)) 
            print(DecryptMsg)
            print("\r")
                
            i = i + 1
                    
# Commands:

# Encrypt:
# Syntax - Encrypt("<text>", <key>)
# Note: Can be executed only from inside the variable


# Decrypt:
# Syntax - Decrypt("<text>", <key>)
# Note: Can be executed only from inside the variable


# BruteForce:
Main.BruteForce("Khoor Zruog")
