from datetime import datetime


def calculate_nb_of_blocks_until_date(future_date: str or datetime):
    if isinstance(future_date, str):
        future_date = datetime.strptime(future_date, '%Y-%m-%d %H:%M:%S')
    delay = future_date - datetime.now()
    nb_blocks = int(delay.seconds / 4.5)
    return nb_blocks
