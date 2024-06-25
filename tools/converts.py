def convert_uptime(uptime):
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)

    return (hours if hours > 0 else 0), minutes


def convert_big_number(num):
    suffixes = ['', 'Thousand', 'Million', 'Billion', 'Trillion', 'Quadrillion', 'Quintillion']

    if num == 0:
        return '0'

    num_abs = abs(num)
    magnitude = 0

    while num_abs >= 1000:
        num_abs /= 1000
        magnitude += 1

    formatted_num = '{:.2f}'.format(num_abs).rstrip('0').rstrip('.')

    return '{} {}'.format(formatted_num, suffixes[magnitude])


def split_string_by_length(input_string, chunk_length):
    return [input_string[i:i + chunk_length] for i in range(0, len(input_string), chunk_length)]


def convert_time(uptime):
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)

    return (hours if hours > 0 else 0), minutes
