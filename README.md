## Windows issues to protect users during a ransomware attack

#Procedure
  Download the Virtual Box from https://www.virtualbox.org/wiki/Downloads
  Download the Virtual Machine from https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/
  The Real-time protection may need to be turned off in the host machine before downloading our code since Windows Security flags it as a ransomware
  Drag and Drop the exes folder from the host machine to the Virtual Machine
  Run keysGenerator.exe
  Run server.exe
  Run encrytor.exe and verify file encryption
  Run decryptor.exe and verify file decryption
  Create recovery point
  Run keysGenerator.exe, IF the previous keys were removed
  Run server.exe, IF the server was shutdownw
  Run encryptor.exe
  Rollback to the recovery point and verify file encryption
  Verify that the OS did not stopped or mitigated the attack during it's execution
