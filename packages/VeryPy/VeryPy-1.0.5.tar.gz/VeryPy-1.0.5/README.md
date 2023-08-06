*PLEASE READ THE ENTIRE README*


```sh
#Navigate to the directory/folder that the file(s) are located in. The files might  be the source file, the encryption key file, the hash file, or any combination of these files.  
cd /PATH/TO/YOUR/WORKING-DIRECTORY

#PIP install the required dependencies once in the working directory
PIP install cryptography
PIP install Verypy

#This file will need to be created and placed in the working directory for the VeryPy package to work. You should call this file VeryPy.py once it is created and saved. 

import VeryPy
import cryptography

if __name__ == '__main__':
  VeryPy(sys.argv[1], sys.argv[2], sys.argv[3])


#Specify the file being tested for changes, a hash file for the hash to be placed, and an encryption key. (Either provide a Fernet encryption key file or let the program generate one for you if this is being ran for the first time. The key.key file should be placed somewhere safe and only provided upon run-time!)
python VeryPy.py sample.txt hash.txt key.key
```
```sh
#If this is the first time running Verypy, the current directory may look like this. In this case, the key.key and hash.txt will be generate for you. The key.key will contain the encryption key that is used to encrypt/decrypt the hash.txt file. The hash.txt file will contain the new hash digest of the sample.txt file, which will then be encrypted. 

#If the key and hash are being generated for the first time, line 13 will need to be ran again to run the actual script to decrypt the hash.txt file so that it can be read from and then re-encrypted. 
python VeryPy.py sample.txt hash.txt key.key
```
*initial setup sample*
```sh
Working-Directory/
---sample.txt
---VeryPy.py
```




```sh
If the intial setup of has already been completed and the hash.txt and key.key files have already been generated or provided, line 13 will be the only command that needs to be ran from the command line for every subsequent use. 
```
*sample after running line 10*
```sh
Working-Directory/
---sample.txt
---VeryPy.py
---key.key
---hash.txt
```