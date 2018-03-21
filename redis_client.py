import redis
import numpy as np

r = redis.StrictRedis(host='localhost', port=6379, db=0)
gamepool = {}
b = [[0, 0, 'k', 0, 'k', 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 'k', 'k', 'k', 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 'k', 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

unit_info_dict = {
    'k': [50, 25, 0],  # hp, armor, recovery
    'f': [65, 15, 0],
    'c': [24, 0, 0],
    's': [40, 20, 0],
    'mg': [60, 0, 0],
    'fg': [60, 60, 0],
    'br': [55, 15, 0],
    'd': [65, 18, 0],
    'a': [35, 20, 0]
}
def flipboard(setup):
    for i in range(11):
        for j in range(6,11):
            setup[i][j]= setup[i][10-j]
    return setup

def switch_player(game_id, current_player):
    print("current player", current_player)
    next_player = current_player % 2+1
    server_switch_move = str(['server', next_player, 'switch'])
    r.rpush('moves_gameid:%s' % game_id, server_switch_move)

def register_game(username, setup):

    gamepool[username] = eval(setup)

    if len(gamepool) % 2 == 0 and len(gamepool) > 0:
        print("lenght of game pool", len(gamepool))
        player1 = gamepool.popitem()
        player2 = gamepool.popitem()
        game_board = np.zeros([11, 11], dtype=np.int32).tolist()

        player1_username, player1_setup  = player1
        player2_username, player2_setup = player2
        player2_setup = flipboard(player2_setup)

        for i in range(11):
            for j in range(11):
                if j<6:
                    owner = "1"
                    unit_key = player1_setup[i][j]
                    orientation = 's'
                else:
                    owner = "2"
                    orientation = 'n'
                    unit_key = player2_setup[i][j]

                if unit_key is not 0:
                    unit_info = [owner, unit_key, orientation]
                    unit_info.extend(unit_info_dict[unit_key])
                    game_board[i][j] = unit_info

        print(game_board)
        gameid = 0
        r.set('gameid:%d'%gameid, str(game_board))
        r.rpush('game_lists', *[gameid, ])
        r.set(player1_username, gameid)
        r.set(player2_username, gameid)
        r.set("player_id%s" % player1_username, "1")
        r.set("player_id%s" % player2_username, "2")
        switch_player(gameid, 2)

def get_gameid(username):
    return r.get(username)

def get_turnplayer(username):
    return r.get("player_id%s" % username)

def get_board(gameid):
    return r.get('gameid:%d'%gameid).decode('utf-8')

def set_game_moves(gameid):
    r.rpush('gameid:%d'%gameid, gameid)


def add_moves(gameid, move):
    r.rpush('moves_gameid:%s' % gameid, move)
    if move[1] == "o" or move[1] == "w":
        current_player = move[0]
        switch_player(gameid, current_player)
    elif move[1] == 'a':
        attacker=move[2]
        defender=move[3]
        board = get_board(gameid)
        # look up game board for their hp and orientation
        # change the game board state with server set


    # last_3_moves= eval(r.lrange('moves_gameid:%d'%gameid, -3,-1))
        #  this is a validation make sure client is not cheating, not yet implemented
    # if turn is finished then add switch turns"
    # for m in reversed(last_3_moves):
    #     if m[1] == "o" or m[1] == 'w':
    #         switch_player(current_player, game_id)


def get_moves(gameid):

    a = r.lrange('moves_gameid:%s' % gameid.decode(), 0, -1)
    return list(map(lambda x: eval(x.decode()), a))

def get_pool():
    return r.lrange('game_lists', 0, 1)

if __name__ == '__main__':
    # register_game('walter', str(b))
    # register_game('walter2', str(b))
    # print(get_pool())
    # r.set_response_callback('LRANGE', str)
    # move = [2, 'w']
    # add_moves('0', move)

    a = r.lrange('moves_gameid:0', 0, -1)
    f = list(map(lambda x: eval(x.decode()), a))
    print(f)


    #moves: [[server, player 1 turn], [1, 'move', 'original', 'target'], [1 , 'attack', 'original', target'], [server, 'block', 'target', 'sucess/fail'], [server, player 1 to player2 turn],[2, 'orientation', target, direction], [server, player2 to player 1 turn]
