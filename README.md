# Serial-Monitor
## About
A simple serial monitoring program that can be used as an alternative to the Arduino serial monitor. Allows for the selection of COM ports on Windows machines.

## Dependencies
This project utilizes the pySerial module for connecting to and monitoring ports. You can install this using either of the following:

```
pip install pyserial
```

```
conda install pyserial
```

Alternatively, you can use conda to load all the dependencies from `requirements.txt` using the following command (replace `<env>` with the environment name):

```
conda create --name <env> --file requirements.txt
```

### Notes to self:
To use conda in powershell, I had to add the following directories to my PATH
- `C:\Users\Scarfy\anaconda3` - My conda installation
- `C:\Users\Scarfy\anaconda3\Scripts` - All the applications conda uses

Then, on opening powershell, run the following:
```
conda init powershell
```

Exit powershell, and you should be able to activate and deactivate conda environments in a new powershell terminal.

To disable conda in powershell, run:
```
conda init --reverse powershell
```