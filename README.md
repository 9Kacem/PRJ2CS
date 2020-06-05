## OBD Data encryption w/ Crypto py 


##### Process:

 - [ ] Every period T of time, a new data instance is created by the OBD reader module.
 - [x] We encrypt it using `encrypt.py` and store it in a folder "encrypted_data". The clear data file will be deleted by the end of this step.
 - [ ] At the end of the trip, we start sending the data instances to the server one by one after signing them for integrity. 
 - [ ] Finally when the server receives data, it starts doing the reverse operation (Checks integrity, decrypt them one by one to a format that can be put in DB).

