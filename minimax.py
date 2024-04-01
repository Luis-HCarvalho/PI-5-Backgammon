from backgammon import Backgammon, Checkers

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

def minimax_alfabeta(game, player, rolled_dices, maximum_depth = 3, alfa = float("-inf"), beta = float("inf")):
    if game.won() or maximum_depth == 0:
        return game.evaluate(player)
    
    valid_moves = []
    if (len(rolled_dices) != 0):
        x, y = rolled_dices[0], rolled_dices[1]
        dices_combinations = ([[x, y], [y, x]] if x != y else [[x, x, x, x]])
    else:
        dices_combinations = [[x, y] if x != y else [x, y] * 2 for x in range(1, 7) for y in range(x, 7)]
    
    for dices in dices_combinations:
        valid_moves.append(game.valid_moves(game.turn(), dices))
        # valid_moves = [*valid_moves, *game.valid_moves(game.turn(), dices)]
    
    # print(f"valid_moves: {valid_moves}")
    for moves in valid_moves:
        # print(f"movement: {move}")
        for move in moves:
            new_game = game.play(game.turn(next=True), move)
        
        evaluate = minimax_alfabeta(new_game, game.turn(), [], maximum_depth - 1, alfa, beta)
        if (game.turn() == player):
            alfa = max(evaluate, alfa)
        else:
            beta = min(evaluate, beta)
        
        if beta <= alfa:
            break

    return (alfa if game.turn() == player else beta)


    # if game.turn() == player: 
    #     for dices in dices_combinations:
    #         for next_game in game.valid_moves(player, dices):
    #             dices_copy = list(dices)
    #             dice_used = game.dice_used(next_game)
    #             dices_copy.remove(dice_used)

    #             new_game = game.play(len(dices_copy) > 0, next_game)
    #             evaluate = minimax_alfabeta(new_game, player, dices_copy, maximum_depth - 1, alfa, beta)
    #             alfa = max(evaluate, alfa)
    #             if beta <= alfa:
    #                 break

    #         return alfa
    # else:
    #     for dices in dices_combinations:
    #         for next_game in game.valid_moves(game.turn(), dices):
    #             dices_copy = list(dices)
    #             dice_used = game.dice_used(next_game)
    #             dices_copy.remove(dice_used)
                
    #             new_game = game.play(len(dices_copy) > 0, next_game)
    #             evaluate = minimax_alfabeta(new_game, game.turn(), dices_copy, maximum_depth - 1, alfa, beta)
    #             beta = min(evaluate, beta)
    #             if beta <= alfa:
    #                 break

    #         return beta

def best_move_agent(game, dices, maximum_depth = 8):
    best_value = float("-inf")
    best_move = [-1, -1]
    for next_game in game.valid_moves(dices):
        evaluate = minimax(game.play(next_game), False, game.turno(), maximum_depth)
        if evaluate > best_value:
            best_value = evaluate
            best_move = next_game
    return best_move

def best_move_agent_poda(game, dices, maximum_depth = 3):
    best_value = float("-inf")
    best_move = [-1, -1]
    for move in game.valid_moves(game.turn(), dices):
        # dices_copy = list(dices)
        # dice_used = game.dice_used(next_game)
        # print(dices_copy, dice_used)
        # dices_copy.remove(dice_used)
        new_game = game.play(game.turn(next=True), move)
        evaluate = minimax_alfabeta(new_game, game.turn(next=True), [], maximum_depth)
        print(f"evaluate: {evaluate}")
        if evaluate > best_value:
            best_value = evaluate
            best_move = move
    
    print(f"beat_move: {best_move}")
    return best_move

def first_moves(game, dices, player):

    next_game = game
    match(dices):
        case [1, 2] | [2, 1]:
            # 24/23 13/11
            next_game = game.play(True, [24, 23] if player == Checkers.BLACK else [1, 2])
            next_game = next_game.play(False, [13, 11] if player == Checkers.BLACK else [12, 14])
        case [1, 3] | [3, 1]:
            # 8/5 6/5
            next_game = game.play(True, [8, 5] if player == Checkers.BLACK else [17, 20])
            next_game = next_game.play(False, [6, 5] if player == Checkers.BLACK else [19, 20])
        case [1, 4] | [4, 1]:
            # 24/23 13/9
            next_game = game.play(True, [24, 23] if player == Checkers.BLACK else [1, 2])
            next_game = next_game.play(False, [13, 9] if player == Checkers.BLACK else [12, 16])
        case [1, 5] | [5, 1]:
            # 24/23 13/8
            next_game = game.play(True, [24, 23] if player == Checkers.BLACK else [1, 2])
            next_game = next_game.play(False, [13, 8] if player == Checkers.BLACK else [12, 17])
        case (1, 6) | (6, 1):
            # 13/7 8/7
            next_game = game.play(True, [13, 7] if player == Checkers.BLACK else [12, 18])
            next_game = next_game.play(False, [8, 7] if player == Checkers.BLACK else [17, 18])
        case [2, 3] | [3, 2]:
            # 24/21 13/11
            next_game = game.play(True, [24, 21] if player == Checkers.BLACK else [1, 4])
            next_game = next_game.play(False, [13, 11] if player == Checkers.BLACK else [12, 14])
        case [2, 4] | [4, 2]:
            # 8/4 6/4
            next_game = game.play(True, [8, 4] if player == Checkers.BLACK else [17, 21])
            next_game = next_game.play(False, [6, 4] if player == Checkers.BLACK else [19, 21])
        case [2, 5] | [5, 2]:
            # 13/11 13/8
            next_game = game.play(True, [13, 11] if player == Checkers.BLACK else [12, 14])
            next_game = next_game.play(False, [13, 8] if player == Checkers.BLACK else [12, 17])
        case [2, 6] | [6, 2]:
            # 24/18 13/11
            next_game = game.play(True, [24, 18] if player == Checkers.BLACK else [1, 7])
            next_game = next_game.play(False, [13, 11] if player == Checkers.BLACK else [12, 14])
        case [3, 4] | [4, 3]:
            # 24/20 13/10
            next_game = game.play(True, [24, 20] if player == Checkers.BLACK else [1, 5])
            next_game = next_game.play(False, [13, 10] if player == Checkers.BLACK else [12, 15])
        case [3, 5] | [5, 3]:
            # 8/3 6/3
            next_game = game.play(True, [8, 3] if player == Checkers.BLACK else [17, 22])
            next_game = next_game.play(False, [6, 3] if player == Checkers.BLACK else [19, 22])
        case [3, 6] | [6, 3]:
            # 24/18 13/10
            next_game = game.play(True, [24, 18] if player == Checkers.BLACK else [1, 7])
            next_game = next_game.play(False, [13, 10] if player == Checkers.BLACK else [12, 15])
        case [4, 5] | [5, 4]:
            # 24/20 13/8
            next_game = game.play(True, [24, 20] if player == Checkers.BLACK else [1, 5])
            next_game = next_game.play(False, [13, 8] if player == Checkers.BLACK else [12, 17])
        case [4, 6] | [6, 4]:
            # 24/18 13/9
            next_game = game.play(True, [24, 18] if player == Checkers.BLACK else [1, 7])
            next_game = next_game.play(False, [13, 9] if player == Checkers.BLACK else [12, 16])
        case [5, 6] | [6, 5]:
            # 24/18 18/13
            next_game = game.play(True, [24, 18] if player == Checkers.BLACK else [1, 7])
            next_game = next_game.play(False, [18, 13] if player == Checkers.BLACK else [7, 12])
        case _:
            next_game = best_move_agent_poda(game, dices)
    
    return next_game


if __name__ == "__main__":
    game = Backgammon()
    print(game)
    print(game.evaluate(game.turn()))
    dices = game.dices()
    print(dices)
    #print(first_move(game, dices, game.turn))
    print(best_move_agent_poda(game, dices, 8))