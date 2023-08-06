from .Board import Board
play = True        
 
while play:
    print("Welcome to the Tic Tac Toe Game \n")
    win = False
    count = 0
    board = Board()
    board.display()
    while not win:
        count=count+1
        if count % 2 ==1:
            #defensive programming, to make sure the input is valid. 
            while True:
                try:
                    num = int(input("Where do you want to place X?"))
                    if (num in range(1,10)) and (board.data[num]==' '):
                        break
                    else:
                        print("Invalid cell number. Input again please.")
                except:
                    print("Not an integer. Input again (1-9) please.")
            board.change(num, 'X')
            board.display()
            win = board.win('X')
        else: 
            while True:
                try:
                    num = int(input("Where do you want to place O?"))
                    if (num in range(1,10)) and (board.data[num]==' '):
                        break
                    else:
                        print("Invalid cell number. Input again please.")
                except:
                    print("Not an integer. Input again (1-9) please.")
            board.change(num, 'O')
            board.display()
            win = board.win('O')
        
    print("Congratulations! You have won the game!")
    if count % 2 ==1:
        print("The winner is X!")
    else:
        print("The winner is O!")
        
    #defensive programming, to make sure the input is within the range     
    while True:
        re=input("Do you want to play again? Please input Y or N \n")
        if re.upper() == 'Y' or re.upper() == 'N':
            break
        else:
            print("Not a valid input. Try again")
        
    if re.upper() == 'Y':
        play = True
    else:
        play = False 