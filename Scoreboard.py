import Communicator
import itertools
import random

NUM_REPEATS = 5
NUM_LABELS = 2
NUM_BANDS_IN_LABEL = 5
NUM_TOTAL_BANDS = NUM_LABELS * NUM_BANDS_IN_LABEL
NUM_WINNING_POSITIONS = 4

WIN_POINTS = 3
TIE_POINTS = 1

DUPLICATE_BOARD_LIMIT = 3

class Bot():
    def __init__(self, communicator, bot_id):
        self.communicator = communicator
        self.is_placeholder = not communicator
        self.player = "Empty" if self.is_placeholder else communicator.name
        self.id = bot_id
        self.name = 0 if self.is_placeholder else id(self)

    def __str__(self):
        return str(self.name)

    def __hash__(self):
        return self.id


def fail(message):
    print "ERROR: "+message
    for b in bots:
        b.communicator.kill()
    exit()

if __name__ == "__main__":
    names = Communicator.read_bot_list()
    points = dict()

    for name in names:
        points[name] = 0

    def add_points(name, num_points):
        points[name] += num_points
    for _ in xrange(NUM_REPEATS):
        for players in itertools.permutations(names, NUM_LABELS):
            #Create bot arrangement
            communicators = Communicator.create_bots(names=players*NUM_BANDS_IN_LABEL)
            ids = range(NUM_TOTAL_BANDS)
            random.shuffle(ids)
            states = {}
            bots = map(Bot, communicators, ids)
            #Inform bots

            names = [x.name for x in bots]
            for index, bot in enumerate(bots):
                info = [bot.id, index, bot.name]
                info.extend(names)
                bot.communicator.send_message(",".join([str(x) for x in info]))
            #Add empty bot
            bots.append(Bot(Communicator.Communicator("Placeholder", None, True), -1))
            placeholder_index = NUM_TOTAL_BANDS
            #Play the Game
            while True:
                #Test to see if a player has won
                player = bots[0].player
                if all(x == player for x in bots[0:NUM_WINNING_POSITIONS]):
                    add_points(player, WIN_POINTS)
                    break
                state = tuple(bots)
                #Test for a tie
                if state in states:
                    if states[state] is DUPLICATE_BOARD_LIMIT:
                        map(add_points, players, [TIE_POINTS, TIE_POINTS])
                        break
                    else:
                        states[state] += 1
                else:
                    states[state] = 1
                #Have bot call name
                caller = bots[placeholder_index-1]
                message = ",".join([str(bot) for bot in bots])
                caller.communicator.send_message(message)
                response = caller.communicator.get_response()
                try:
                    switcher_id = int(response)
                except ValueError, e:
                    fail(str(caller.name)+" didn't return an int:"+response)
                #Find the bot to switch with
                bot_ids = [bot.id for bot in bots]
                if switcher_id not in bot_ids:
                    fail(str(caller.name)+" sent a bad id:"+str(switcher_id))
                switcher_index = bot_ids.index(switcher_id)
                switcher = bots[switcher_index]
                #Inform the switched bot
                switcher.communicator.send_message(str(caller) + "," +
                                                   str(placeholder_index))
                #switch
                bots[switcher_index], bots[placeholder_index] \
                    = bots[placeholder_index], bots[switcher_index]
                placeholder_index = switcher_index
            for bot in bots:
                bot.communicator.send_message("0")
                bot.communicator.kill()
        points = list(points.items())
        points.sort(key=lambda tup: tup[1])
        for name, point in points:
            print name+" got "+str(point)+" points"

