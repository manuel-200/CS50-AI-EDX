import random

def main():
    signin()
    
def signin():
    IBAN=input("IBAN: ")
    IBANlen=len(IBAN)  
    while IBANlen!=22:
        print("Enter a valid IBAN")
        IBAN=input("IBAN: ")
        IBANlen=len(IBAN)
    print("Country code: "+IBAN[0:1])
    print("Check number: "+IBAN[2:3])
    print("Sort code: "+IBAN[4:10])
    print("Account Number: "+IBAN[11:21])

main()