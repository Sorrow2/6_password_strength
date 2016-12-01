import re


def load_wordlist_file(filepath):
    wordlist_set = set()
    with open(filepath) as file:
        for line in file.readlines():
            wordlist_set.add(line.strip())
    return wordlist_set


def password_length_score(password):
    password_length = len(password)
    if password_length < 4:
        return 0
    elif password_length < 7:
        return 1
    elif password_length < 13:
        return 2
    else:
        return 3


def check_blacklist(password, wordlist):
    return password in wordlist


def check_upper_and_lower_case(password):
    return not password.islower() and not password.isupper()


def check_special_characters(password):
    return re.search('[^a-zа-яё0-9]', password, re.IGNORECASE)


def check_digits(password):
    return re.search('\d', password)


def check_date_and_plate_number_format(password):
    return re.match('\d+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря|rus|рус)',
                    password, re.IGNORECASE) and re.match('\d{1,2}\.\d{1,2}\.\d{2,4}', password)


def get_password_strength(password):
    score = password_length_score(password)

    if not check_blacklist(password, ru_en_wordlist):
        score += 1

    if not check_date_and_plate_number_format(password):
        score += 1

    if check_digits:
        score += 1

    if check_upper_and_lower_case(password):
        score += 2

    if check_special_characters(password):
        score += 2

    return score


if __name__ == '__main__':
    most_common_passwords = load_wordlist_file('10000_common_passwords.txt')
    ru_en_wordlist = load_wordlist_file('russian_words.txt') | load_wordlist_file(
        'english_words.txt') | load_wordlist_file('translit_words.txt')

    while 1:
        password = input('Введите пароль: ').strip()
        if password in ('quit', 'exit'):
            print('Программа завершена.')
            break
        elif password in most_common_passwords:
            print('Пароль небозопасен. Этот пароль один из наиболее часто используемых. Оценка: 0/10')
            break

        print('Оценка сложности вашего пароля: {}/10.'.format(get_password_strength(password)))
