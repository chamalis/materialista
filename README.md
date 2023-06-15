## Intro ##

Materialista is a web crawler for house renting websites
in Spain (currently only idealista.com supported),
which will search for listings by private owners (no agencies)
or listings that require only 1 rent deposit.

Its run through a system terminal (shell), and has only been tested 
in Linux so far (although should work in any OS with python & selenium).

It needs python3 to be installed, and basic knowledge of the shell.

The results are written in txt files (ideares.txt) under the directory (folder)
where the script is executed. It also stores the already identified properties
in *.pickle files, so that it doesnt append the same properties to the output
files each time its being ran. If you want to reset its "state", just delete
the .pickle files.

The current status of this quick & dirty script is under development, 
so expect all sorts of weird things to happen :)

## Installation ##

A script that includes the following steps is already written: `install.sh`.

So either:
```bash
cd materialista
chmod +x install.sh
./install.sh
```

or manually perform the following steps:

Navigate in the source code directory:
```bash
cd materialista
```

Create a python virtual environment (optional)
```bash
virtualenv -p python3 <directory_for_the_venv>
```

Enable the virtual env (if previous step was followe) 
```bash
source <directory_for_the_venv>/bin/activate
```

install the dependencies:
```bash
pip install -r requirements.txt
```


## Usage ##

Invoke via the command line:
```bash
python main.py
```
