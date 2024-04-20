from read_log import read_log
import re


def get_ipv4s_from_log(slownik):
    lista_adresow = []
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    matches = re.findall(ip_pattern, slownik.get("message"))
    for match in matches:
        lista_adresow.append(match)
    return lista_adresow


# def get_user_from_log(slownik):



if __name__ == "__main__":
    lista_dict = read_log()
    # 1.1.1 testowy wydruk     type OpenSSH_2k.log | python lab_5_1_1.py
    for slownik in lista_dict:
        print(slownik)
        print(get_ipv4s_from_log(slownik))
        # print(get_user_from_log(slownik))
