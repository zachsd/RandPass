# RandPass
This python script will generate a random string with the intention of these string to be used as a literal password. 

Command line option for character sets and character set weights are available. Setting a weight to 100 is the same as disabling all other sets.  
```python
~> python3 ./randpass.py -h
"""
General:
        -p, --passwd-length     The number of characters in the generated password, Default is 50
        -h, --help              Print this help message

    Enable or Disable Character Sets:
        -l, --lower             Lower case characters,  Default is True
        -u, --upper             Upper case characters,  Default is True
        -n, --number            Number characters,      Default is True
        -s, --special           Special characters,     Default is True
        
    Character Set weights:
        Total for all weights must equal 100.
        When the character set is enabled and the weight is set to None, the weight will be automatically calculated
    
        -L, --lower-weight      Sets the weight for the lower case character set,   Default is None
        -U, --upper-weight      Sets the weight for the upper case character set,   Default is None
        -N, --number-weight     Sets the weight for the number character set,       Default is None
        -S, --special-weight    Sets the weight for the special character set,      Default is None
"""

~> python3 ./randpass.py -L 100 -p 90
yfsjgnvreidnxalolyjytwcqndydkrqffporeqiwzjktgbmzcbaszpwmwjtnekutgzwrkutolkpabypawugirqupgq
```