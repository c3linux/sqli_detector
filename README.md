# About

SQL Injection Detector

# Installation

Install python, pip and virtualenv
```
sudo apt install python python-pip virtualenv
```
create environment and activate
```
virtualenv [--python=python_path] env

source env/bin/activate
```
Install required libraries
```
pip install -r requirements.txt
```

# Using

```
python blind_sqli_detector.py -u "target"
```
#### Example

```
python3 blind_sqli_detector.py -u "http://testphp.vulnweb.com/artists.php?artist=1"
```
---

TODO:
- [ ] Add binary search
- [ ] Add POST method
- [ ] Add Authentication method
- [ ] Add payloads
- [ ] Optimize code
- [ ] Add other sqli techniques
    - [ ] Time Based (progressing)
    - [ ] Union Baed
    - [ ] Boolean Based
    - [ ] Error Based
