from lab_5_1_1 import get_ipv4s_from_log
from lab_5_1_1 import get_user_from_log
from read_log import read_log
import random
import re
from datetime import datetime
import statistics


def get_random_logs_for_user(lista_dict, user, n):
    filtered_logs = [slownik for slownik in lista_dict if user == get_user_from_log(slownik)]
    if len(filtered_logs) <= n or n == 0:
        return filtered_logs
    else:
        return random.sample(filtered_logs, n)


def calculate_ssh_connection_stats(lista_dict):
    open_list = []
    close_list = []

    # Podział wpisów na listy otwierające i zamykające sesję
    for slownik in lista_dict:
        message = slownik.get("message")
        if "session opened for user" in message:
            open_list.append(slownik)
        elif "session closed for user" in message:
            close_list.append(slownik)

    # Stworzenie słownika, gdzie kluczem jest użytkownik, a wartością lista par czasowych (start, end)
    user_sessions = {}
    for open_entry in open_list:
        user = get_user_from_log(open_entry)
        if user not in user_sessions:
            user_sessions[user] = []
        for close_entry in close_list:
            if get_user_from_log(close_entry) == user:
                user_sessions[user].append((open_entry.get("date"), close_entry.get("date")))
                # Usuwamy wpis zamykający sesję, aby nie był używany ponownie
                close_list.remove(close_entry)
                break

    # Obliczanie średniej długości trwania sesji dla każdego użytkownika
    user_avg_durations = {}
    user_dev_durations = {}
    all_user_stat = []
    for user, sessions in user_sessions.items():
        durations = []
        for session in sessions:
            start_time = convert_str_to_datetime(session[0])
            end_time = convert_str_to_datetime(session[1])
            duration = end_time - start_time
            durations.append(duration.total_seconds())
            all_user_stat.append(duration.total_seconds())
        if durations:
            user_avg_durations[user] = statistics.mean(durations)
            print(f"Średni czas trwania sesji po użytkowniku {user}: {user_avg_durations[user]} sekund")
            if len(durations) > 1:
                user_dev_durations[user] = statistics.stdev(durations)
                print(f"Odchylenie standardowe czasu trwania sesji po użytkowniku {user}: {user_dev_durations[user]} sekund")
            else:
                print(f"Odchylenie standardowe czasu trwania sesji po użytkowniku {user}: nie może być obliczone")
    print(f"Średni czas trwania sesji ze wszystkich logów: {statistics.mean(all_user_stat)}")
    print(f"Odchylenie standardowe czasu trwania sesji ze wszystkich logów: {statistics.stdev(all_user_stat)}")


def convert_str_to_datetime(date_str):
    # Data to string w formacie "Dec 10 11:41:14"
    current_year = datetime.now().year
    new_date_str = f"{current_year} {date_str}"
    if date_str.startswith("Dec"):
        # dodamy poprzedni rok dla Grudnia
        new_date_str = "2023 " + date_str
    date_obj = datetime.strptime(new_date_str, "%Y %b %d %H:%M:%S")
    return date_obj


def calculate_user_login_frequency(lista_dict):
    user_logins = {}
    for slownik in lista_dict:
        user = get_user_from_log(slownik)
        if user:
            if user in user_logins:
                user_logins[user] += 1
            else:
                user_logins[user] = 1

    if not user_logins:
        return None, None

    min_login_user = min(user_logins, key=user_logins.get)
    max_login_user = max(user_logins, key=user_logins.get)

    return min_login_user, max_login_user


if __name__ == "__main__":
    lista_dict = read_log()

    # 1.3.1
    user = "root"
    iloscWpisow = 2
    random_logs = get_random_logs_for_user(lista_dict, user, iloscWpisow)
    print(f"Random logs for user {user}:")
    for log in random_logs:
        print(log)

    # 1.3.2
    calculate_ssh_connection_stats(lista_dict)
    # mean_duration, stdev_duration = calculate_ssh_connection_stats(lista_dict)
    # if mean_duration is not None and stdev_duration is not None:
    #     print("Mean duration of SSH connections:", mean_duration)
    #     print("Standard deviation of SSH connection duration:", stdev_duration)
    # else:
    #     print("No SSH connection durations found.")

    # 1.3.3
    min_login_user, max_login_user = calculate_user_login_frequency(lista_dict)
    if min_login_user is not None and max_login_user is not None:
        print("User who logged in least frequently:", min_login_user)
        print("User who logged in most frequently:", max_login_user)
    else:
        print("No user login frequencies found.")
