import sys

last_switched = -1


def get_data():
    data = sys.stdin.readline().strip()
    if data == "0":
        exit()
    return [int(x) for x in data.split(",")]


def startup():
    global _id, position, name
    try:
        all_data = get_data()
    except:
        raise NameError
    player_names = all_data[3:]
    _id, position, name = all_data[:3]


def switched(switcher, new_position):
    global position, last_switched
    position = new_position
    last_switched = switcher


def call_id(player_names):
    return min(position, 9)

_id = -1
position = -1
name = -1
startup()
while True:
    data = get_data()
    if len(data) == 1:
        break
    elif len(data) == 2:
        switched(*data)
    else:
        print call_id(player_names=data)
        sys.stdout.flush()