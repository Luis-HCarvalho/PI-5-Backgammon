def minimax(game, max_turn, player, maximum_depth = 8):
    if game.won() or maximum_depth == 0:
        return game.evaluate(player)

    if max_turn:
        best_value = float("-inf") 
        for next_game in game.valid_moves():
            evaluate = minimax(game.play(next_game), False, player, maximum_depth - 1)
            best_value = max(evaluate, best_value)
        return best_value
    else:
        worst_value = float("inf") 
        for next_game in game.valid_moves():
            evaluate = minimax(game.play(next_game), True, player, maximum_depth - 1)
            worst_value= min(evaluate, worst_value) 
        return worst_value

def minimax_alfabeta(game, max_turn, player, maximum_depth = 8, alfa = float("-inf"), beta = float("inf")):
    if game.won() or maximum_depth == 0:
        return game.evaluate(player)

    if max_turn:
        for next_game in game.valid_moves():
            evaluate = minimax_alfabeta(game.play(next_game), False, player, maximum_depth - 1, alfa, beta)
            alfa = max(evaluate, alfa)
            if beta <= alfa:
                continue
        return alfa
    else: 
        for next_game in game.valid_moves():
            evaluate = minimax_alfabeta(game.play(next_game), True, player, maximum_depth - 1, alfa, beta)
            beta = min(evaluate, beta)
            if beta <= alfa:
                continue
        return beta

def best_move_agent(game, dices, maximum_depth = 8):
    best_value = float("-inf")
    best_move = [-1, -1]
    for next_game in game.valid_moves(dices):
        evaluate = minimax(game.play(next_game), False, game.turno(), maximum_depth)
        if evaluate > best_value:
            best_value = evaluate
            best_move = next_game
    return best_move

def best_move_agent_poda(game, dices, maximum_depth = 8):
    best_value = float("-inf")
    best_move = [-1, -1]
    for next_game in game.valid_moves(dices):
        evaluate = minimax_alfabeta(game.play(next_game), False, game.turno(), maximum_depth)
        if evaluate > best_value:
            best_value = evaluate
            best_move = next_game
    return best_move

def first_move(game):
    dices = game.dices()
    
    next_game = game
    match(dices):
        case [1, 2] | [2, 1]:
            # 24/23 13/11
            dices.remove(1)
            next_game = game.play([24, 23], dices)
            dices.remove(2)
            next_game = game.play([13, 11], dices)
        case [1, 3] | [3, 1]:
            # 8/5 6/5
            dices.remove(3)
            next_game = game.play([8, 5], dices)
            dices.remove(1)
            next_game = game.play([6, 5], dices)
        case [1, 4] | [4, 1]:
            # 24/23 13/9
            dices.remove(1)
            next_game = game.play([24, 23], dices)
            dices.remove(4)
            next_game = game.play([6, 5], dices)
        case [1, 5] | [5, 1]:
            # 24/23 13/8
            dices.remove(1)
            next_game = game.play([24, 23], dices)
            dices.remove(5)
            next_game = game.play([13, 8], dices)
        case (1, 6) | (6, 1):
            # 13/7 8/7
            dices.remove(1)
            next_game = game.play([13, 7], dices)
            dices.remove(6)
            next_game = game.play([8, 7], dices)
        case [2, 3] | [3, 2]:
            # 24/21 13/11
            dices.remove(2)
            next_game = game.play([24, 21], dices)
            dices.remove(3)
            next_game = game.play([13, 11], dices)
        case [2, 4] | [4, 2]:
            # 8/4 6/4
            dices.remove(4)
            next_game = game.play([8, 4], dices)
            dices.remove(2)
            next_game = game.play([6, 4], dices)
        case [2, 5] | [5, 2]:
            # 13/11 13/8
            dices.remove(2)
            next_game = game.play([13, 11], dices)
            dices.remove(5)
            next_game = game.play([13, 8], dices)
        case [2, 6] | [6, 2]:
            # 24/18 13/11
            dices.remove(6)
            next_game = game.play([24, 18], dices)
            dices.remove(2)
            next_game = game.play([13, 11], dices)
        case [3, 4] | [4, 3]:
            # 24/20 13/10
            dices.remove(4)
            next_game = game.play([24, 20], dices)
            dices.remove(3)
            next_game = game.play([13, 10], dices)
        case [3, 5] | [5, 3]:
            # 8/3 6/3
            dices.remove(5)
            next_game = game.play([8, 3], dices)
            dices.remove(3)
            next_game = game.play([6, 3], dices)
        case [3, 6] | [6, 3]:
            # 24/18 13/10
            dices.remove(6)
            next_game = game.play([24, 18], dices)
            dices.remove(3)
            next_game = game.play([13, 10], dices)
        case [4, 5] | [5, 4]:
            # 24/20 13/8
            dices.remove(4)
            next_game = game.play([24, 20], dices)
            dices.remove(5)
            next_game = game.play([13, 8], dices)
        case [4, 6] | [6, 4]:
            # 24/18 13/9
            dices.remove(6)
            next_game = game.play([24, 18], dices)
            dices.remove(4)
            next_game = game.play([13, 9], dices)
        case [5, 6] | [6, 5]:
            # 24/18 18/13
            dices.remove(6)
            next_game = game.play([24, 18], dices)
            dices.remove(5)
            next_game = game.play([18, 13], dices)
        case _:
            # 
            next_game = best_move_agent_poda(game, dices)
    
    return next_game