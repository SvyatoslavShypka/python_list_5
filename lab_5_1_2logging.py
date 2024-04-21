import sys
from read_log import read_log
import re
import logging


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


# Konfiguracja loggera
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Ustawienie handlerów dla różnych poziomów logowania
console_info_handler = logging.StreamHandler(sys.stdout)
console_info_handler.setLevel(logging.INFO)
console_info_handler.setFormatter(logging.Formatter('%(message)s'))
logging.getLogger('').addHandler(console_info_handler)

console_error_handler = logging.StreamHandler(sys.stderr)
console_error_handler.setLevel(logging.ERROR)
console_error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger('').addHandler(console_error_handler)

if __name__ == "__main__":
    lista_dict = read_log()
    for slownik in lista_dict:
        logging.info(slownik.get("message"))
        logging.debug("Przeczytano %d bajtów", len(slownik.get("message")))
        if "Accepted password" in slownik.get("message") or "session opened for user" in slownik.get("message"):
            logging.info("Udana próba logowania lub otwarcie sesji")
        elif "Failed password" in slownik.get("message") and "invalid user" not in slownik.get("message"):
            logging.warning("Nieudana próba logowania")
        elif "Failed password" in slownik.get("message") and "invalid user" in slownik.get("message"):
            logging.error("Nieudana próba logowania - nieprawidłowy użytkownik")
        elif "error" in slownik.get("message").lower():
            logging.error("Wystąpił błąd")
        elif "włamania" in slownik.get("message").lower():
            logging.critical("Wykryto próbę włamania")

        # logging.info(get_ipv4s_from_log(slownik))
        # logging.info(get_user_from_log(slownik))
