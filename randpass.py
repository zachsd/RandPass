import getopt
import sys
import random
from requests import options


def get_random_letter_lower():
    return chr(random.randrange(97, 123))


def get_random_letter_upper():
    return chr(random.randrange(65, 91))


def get_random_number():
    return chr(random.randrange(48, 58))


def get_random_special():
    char_sets = [(58, 65), (91, 97)]
    this_char_set = random.choice(char_sets)
    return chr(random.randrange(this_char_set[0], this_char_set[1]))


def generate_passwd(
    pw_len: int,
    lower: bool = True,
    upper: bool = True,
    numbers: bool = True,
    special: bool = True,
    lower_weight=None,
    upper_weight=None,
    number_weight=None,
    special_weight=None,
):
    """
    This will generate a random password. 
    You can choose character sets to exclude and weights, how much of the string, for each character sets.

    Args:
        pw_len          (int):               The number of characters in the generated password.    Default is 50

    Character Sets: 
        lower           (bool, optional):    Lower case characters.  Defaults to True.
        upper           (bool, optional):    Upper case characters.  Defaults to True.
        numbers         (bool, optional):    Number characters.      Defaults to True.
        special         (bool, optional):    Special characters.     Defaults to True.

    Character Weights:
        lower_weight    (int, optional):     Sets the weight for the lower case character set.  Defaults to None.
        upper_weight    (int, optional):     Sets the weight for the upper case character set.  Defaults to None.
        number_weight   (int, optional):     Sets the weight for the number character set.      Defaults to None.
        special_weight  (int, optional):     Sets the weight for the special character set.     Defaults to None.

    Returns:
        str: A randomized string
    """
    character_sets = {
        'lower':    {
            'use': lower,
            'func': get_random_letter_lower,
            'count': 0,
            'weight': lower_weight
        },
        'upper':    {
            'use': upper,
            'func': get_random_letter_upper,
            'count': 0,
            'weight': upper_weight
        },
        'numbers':  {
            'use': numbers,
            'func': get_random_number,
            'count': 0,
            'weight': number_weight
        },
        'special':  {
            'use': special,
            'func': get_random_special,
            'count': 0,
            'weight': special_weight
        }
    }
    # For all char sets that are set to use and weights not set when calling the function, calculate and set them evenly.
    # If 1 or more weights are set remove that from the total weigh available for the other char sets.
    char_spread = 0
    char_weight = 100
    for case in character_sets.keys():
        # Gather info to calculate spread and weight for values not set
        if character_sets[case]['use'] == True and character_sets[case]['weight'] == None:
            char_spread += 1
        # Calculate spread for values that are set
        elif character_sets[case]['use'] == True and character_sets[case]['weight'] != None:
            # Remove weight if set from total available
            char_weight -= character_sets[case]['weight']
            character_sets[case]['weight'] = character_sets[case]['weight'] * .01
            character_sets[case]['count'] = int(
                (character_sets[case]['weight'] * pw_len))
    # Convert the weight to a percentage value, which will be used to calculate the number or chars in the set.
    weights = (char_weight / char_spread) * .01
    if (pw_len * weights) % 1 != 0:
        count = round(pw_len * weights) + 1
    else:
        count = round(pw_len * weights)
    # Apply calculated weights to character sets.
    for case in character_sets.keys():
        if character_sets[case]['use']:
            if character_sets[case]['weight'] == None:
                character_sets[case]['weight'] = weights
                character_sets[case]['count'] = count
    # Array to be used to collect the random characters.
    char_builder = []
    while char_builder.__len__() < pw_len:
        # Array to store this iteration of valid character sets
        choices = []
        for sets in character_sets.keys():
            # if a character set is set to use and still has character left based off of it's calculated weight, add it as a valid choice.
            if character_sets[sets]['use'] == True and character_sets[sets]['count'] > 0:
                choices.append(sets)
        # Select a random option from the valid choices, decrease it's count, generate the random character, add it to the character array.
        this_char_set = random.choice(choices)
        character_sets[this_char_set]['count'] -= 1
        char_builder.append(character_sets[this_char_set]['func']())
    # Convert the character array into a string and return the string
    return ''.join(char_builder)


if __name__ == '__main__':
    kwargs = {
        'pw_len': 50,
        'lower': True,
        'upper': True,
        'numbers': True,
        'special': True,
        'lower_weight': None,
        'upper_weight': None,
        'number_weight': None,
        'special_weight': None
    }

    argumentList = sys.argv[1:]
    options = "p:l:u:n:s:P:L:U:N:S:h"
    long_options = [
        'help',
        'passwd-length',
        'lower',
        'upper',
        'numbers',
        'special',
        'lower-weight',
        'upper-weight',
        'number-weight',
        'special-weight'
    ]
    help_message = """
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
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        # checking each argument
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--help"):
                print(help_message)
                exit()

            elif currentArgument in ("-p", "--passwd-length"):
                kwargs['pw_len'] = int(currentValue)

            elif currentArgument in ("-l", "--lower"):
                value = currentValue.lower()
                if value in ['no', 'false', '0']:
                    kwargs['lower'] = False

            elif currentArgument in ("-u", "--upper"):
                value = currentValue.lower()
                if value in ['no', 'false', '0']:
                    kwargs['upper'] = False

            elif currentArgument in ("-n", "--number"):
                value = currentValue.lower()
                if value in ['no', 'false', '0']:
                    kwargs['numbers'] = False

            elif currentArgument in ("-s", "--special"):
                value = currentValue.lower()
                if value in ['no', 'false', '0']:
                    kwargs['special'] = False

            elif currentArgument in ("-L", "--lower-weight"):
                kwargs['lower_weight'] = int(currentValue)

            elif currentArgument in ("-U", "--upper-weight"):
                kwargs['upper_weight'] = int(currentValue)

            elif currentArgument in ("-N", "--number-weight"):
                kwargs['number_weight'] = int(currentValue)

            elif currentArgument in ("-S", "--special-weight"):
                kwargs['special_weight'] = int(currentValue)
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

    print(generate_passwd(**kwargs))
