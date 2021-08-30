# DNI Calculator

A simple package to help calculate DNIs missing information (National Identity Documents in Spain)

  - Find a missing letter
  - Find missing numbers provided the letter is known
  - Find all possible DNIs that can end up with a given letter
  - Simple CLI interface powered by [fire][python-fire]
  
 ## CLI usage
 
 ```console
 user@user:~$ python3 calculate_dni.py find_letter 11-111-111
 11111111H
 
 user@user:~$ python3 calculate_dni.py find_missing_num 11-?11-?11-H
 11111111H
 
 user@user:~$ python3 calculate_dni.py find_all_possible_dnis 11-?11-1?1-H
 11111111H
 11211161H
 11611131H
 11711181H
 ```
  
  [python-fire]: https://github.com/google/python-fire
