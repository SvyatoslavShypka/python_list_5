from read_log import read_log
import re


def get_ipv4s_from_log(slownik):
    lista_adresow = []
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    matches = re.findall(ip_pattern, slownik.get("message"))
    for match in matches:
        lista_adresow.append(match)
    return lista_adresow


def get_user_from_log(slownik):
    lista_users = []
    user_patterns = [
        r"Accepted password for (\w+)",
        r"Failed password for (?:invalid user )?(\w+)",
        r"Invalid user\s+(\w+)",
        r"for user\s+(\w+)",
        r"user=(\w+)",
        r"input_userauth_request: invalid user (\w+) \[preauth\]"
    ]

    for pattern in user_patterns:
        matches = re.findall(pattern, slownik.get("message"))
        for match in matches:
            lista_users.append(match)
    if not lista_users:
        lista_users.append(None)
    return lista_users


if __name__ == "__main__":
    lista_dict = read_log()
    # 5.1.1.1 testowy wydruk     type OpenSSH_2k.log | python lab_5_1_1.py
    for slownik in lista_dict:
        print(slownik.get("message"))
        # 5.1.1.2
        print(get_ipv4s_from_log(slownik))
        # 5.1.1.3
        print(get_user_from_log(slownik))
