
# MongpyBruter
Humble tool to carry out dictionary attacks over Mongo servers. 
The script uses regular expressions to extract ip values from hosts/target file ​​so it supports -oX outputs from nmap or masscan =D


## Installation

Install MongpyBruter with pip

```bash
  git clone https://github.com/L0stByt3/mongpyBruter.git
  cd mongpyBruter
  pip install -r requeriments.txt

```
    
## Usage
Launch unique conection prove over a target without credentials
```python
python mongpyBruter.py -h
options:
  -h, --help            show this help message and exit
  --hosts HOSTS         Path to target(s) host file. File must be content one or more ip address
  --target TARGET, -t TARGET
                        Single domain or ip address. Ex. 127.0.0.1
  --user USER, -u USER  A single username
  --password PASSWORD, -p PASSWORD
                        A single password
  --nullcredentials NULLCREDENTIALS, -n NULLCREDENTIALS
                        Test conection without credentials
  --users USERS         Path to user list dictionary file. By default is ./users.txt
  --passwords PASSWORDS
                        Path to password list dictionary file. By default is ./passwords.txt
  -m MODE, --mode MODE  Mode can be [unique | list] by default is: list

```
Launch unique conection prove over a target without credentials
```python
python mongpyBruter.py -m unique -t 127.0.0.1 -n true 
```
Launch single credentials prove over a target
```python
python mongpyBruter.py -m unique -t 127.0.0.1 -n true 
```
Launch dictionary attack from massive targets
```python
python mongpyBruter.py --hosts hosts.txt --users users.txt --passwords passwords.txt 
```


## License

[AGPL-3.0](https://choosealicense.com/licenses/agpl-3.0/)

