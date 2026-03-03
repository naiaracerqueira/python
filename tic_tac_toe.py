from random import randint

def display_board(board):
    print(
        f"""
        +-------+-------+-------+
        |       |       |       |
        |   {board[0][0]}   |   {board[0][1]}   |   {board[0][2]}   |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |   {board[1][0]}   |   {board[1][1]}   |   {board[1][2]}   |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |   {board[2][0]}   |   {board[2][1]}   |   {board[2][2]}   |
        |       |       |       |
        +-------+-------+-------+
        """
    )

def enter_move(board):
    move = int(input("Make yout move: "))
    if move >= 1 and move <= 3:
        if board[0][move-1] not in ['O', 'X']:
            board[0][move-1] = 'O'
        else:
            print('Not available')
            enter_move(board)
    elif move >= 4 and move <= 6:
        if board[1][move-4] not in ['O', 'X']:
            board[1][move-4] = 'O'
        else:
            print('Not available')
            enter_move(board)
    elif move >= 7 and move <= 9:
        if board[2][move-7] not in ['O', 'X']:
            board[2][move-7] = 'O'
        else:
            print('Not available')
            enter_move(board)
    else: 
        print('Not valid')
        enter_move(board)
    display_board(board)
    return board

def make_list_of_free_fields(board):
    fields = []
    for i in range(3):
        for j in range(3):
            if board[i][j] not in ['O', 'X']:
                fields.append((i,j))
    return fields

def computer_move(board):
    fields = make_list_of_free_fields(board)
    my_move = randint(0, len(fields)-1)
    print(f"My turn: ")
    row, col = fields[my_move]
    board[row][col] = 'X'
    display_board(board)
    return board

def check_winner(board, sign):
    winner = 'me' if sign == 'X' else 'you'
    if board[0] == [sign,sign,sign] or board[1] == [sign,sign,sign] or board[2] == [sign,sign,sign]: # check row
        return winner
    elif board[0][0] == sign and board[1][0] == sign and board[2][0] == sign: # check col
        return winner
    elif board[0][1] == sign and board[1][1] == sign and board[2][1] == sign: # check col
        return winner
    elif board[0][2] == sign and board[1][2] == sign and board[2][2] == sign: # check col
        return winner
    elif board[0][0] == sign and board[1][1] == sign and board[2][2] == sign: # check cross \
        return winner
    elif board[0][2] == sign and board[1][1] == sign and board[2][0] == sign: # check cross /
        return winner
    else: 
        return None


board = [[1,2,3],[4,5,6],[7,8,9]]
display_board(board)

print('I start')
board[1][1] = 'X'
display_board(board)

fields = make_list_of_free_fields(board)
while len(fields) > 0:
    board = enter_move(board)
    winner = check_winner(board, 'O')
    if winner:
        break
 
    board = computer_move(board)
    winner = check_winner(board, 'X')
    if winner:
        break

    fields = make_list_of_free_fields(board)

print(f'And the winner is....: {winner}!')