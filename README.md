## Windows issues to protect users during a ransomware attack

#Procedure
  Download the Virtual Box from https://www.virtualbox.org/wiki/Downloads <br>
  Download the Virtual Machine from https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/ <br>
  The Real-time protection may need to be turned off in the host machine before downloading our code since Windows Security flags it as a ransomware <br>
  Drag and Drop the exes folder from the host machine to the Virtual Machine <br>
  Run keysGenerator.exe <br>
  Run server.exe <br>
  Run encrytor.exe and verify file encryption <br>
  Run decryptor.exe and verify file decryption <br>
  Create recovery point <br>
  Run keysGenerator.exe, IF the previous keys were removed <br>
  Run server.exe, IF the server was shutdownw <br>
  Run encryptor.exe <br> 
  Rollback to the recovery point and verify file encryption <br>
  Verify that the OS did not stopped or mitigated the attack during it's execution <br>
