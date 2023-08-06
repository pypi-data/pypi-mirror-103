import hashlib 
import cryptography
from cryptography.fernet import Fernet
import os.path
import sys

class VeryPy:
  def __init__(self, source_file, hash_file, key):
    self.source_file = source_file
    self.hash_file = hash_file
    self.key = key
    self.source_hash = ""
    self.keycontents = ""
    self.source_run_content = ''
    self.source_run_content_hash = ""
    
    if os.path.exists(self.hash_file and self.key):
      print('Setup already completed... decrypting')
      self.run()
    else:
      self.setup()
    
  def reader(self):
    with open(self.source_file, 'rb') as f:
      self.source_file = f.read()
  
  def readerRun(self):
    with open(self.source_file, 'rb') as f:
      self.source_run_content = f.read()

  def hasherRun(self):
    print(self.source_run_content)
    source_obj = hashlib.sha1(bytes(self.source_run_content))
    print(self.source_hash)
    self.source_run_content_hash= source_obj.hexdigest()
    
  def hasher(self):
    print(self.source_file)
    source_obj = hashlib.sha1(bytes(self.source_file))
    print(self.source_hash)
    self.source_hash = source_obj.hexdigest()
    if os.path.exists('hash.txt'):
      print('hash already exists')
    else:
      with open(self.hash_file, 'w') as f: 
        f.write(self.source_hash)
    
  def decrypter(self):
    with open(self.key, 'rb') as f:
      key = f.read()
    with open(self.hash_file, 'rb') as f:
      data = f.read()
    fernet = Fernet(key)
    decrypt = fernet.decrypt(data)
    with open(self.hash_file, 'wb') as f:
      f.write(decrypt) 
  
  def encrypter(self):
    file = open(self.key, 'rb')
    self.keycontents = file.read()
    file.close()

  
    with open(self.hash_file, 'rb') as f:
      data = f.read()

    fernet = Fernet(self.keycontents)
    encrypted = fernet.encrypt(data)


    with open(self.hash_file, 'wb') as f:
      f.write(encrypted)

  def compare(self):
    
    with open(self.hash_file, 'r') as f:
      hash = f.read()
    print(hash)
    print(self.source_hash)
    if hash == self.source_run_content_hash:
      return True
      
    else: 
      return False
  
  def keyGenerator(self):
    if os.path.exists('key.key'):
      print("Key exists")
    else:
      key = Fernet.generate_key()
      with open('key.key', 'wb') as f:
        f.write(key)

  def gate(self):
    if self.compare():
      print('Hashes Match')
    else:
      response = input('Hashes are different and changes may have been made to the source file. Press C to continue or Q to quit. > ')
      if response.upper() == 'Q':
        print('Quiting...')
        self.encrypter()
        sys.exit()
      else:
        pass

  def run(self):
    
    self.decrypter()
    self.readerRun()
    self.hasherRun()
    self.compare()
    self.gate()
    self.encrypter()
    
  def setup(self):
    self.keyGenerator()
    self.reader()
    self.hasher()
    self.encrypter()



#veripy = VeriPy('test.txt', 'hash.txt', 'key.key')
verypy = VeryPy(sys.argv[1],sys.argv[2], sys.argv[3])