#Board class presents the information to the computer screen in a 3*3 table 

class Board: 
    def __init__ (self):
        """Attributes: 
                data(list of strings): it contains 10 cells, with the first one to be a dummy cell. The rest of nine cells correspond to a place on the 3*3                     table
                """
        self.data = [' ', ' ', ' ',' ', ' ', ' ', ' ', ' ', ' ', ' ']
        
    def display (self): 
        """Function to display the board in a 3*3 table.
        
            Args:
                None
               
           Returns:
                None
           """
            
        print(" {} | {} | {}".format(self.data[1], self.data[2], self.data[3]))
        print("-----------")
        print(" {} | {} | {}".format(self.data[4], self.data[5], self.data[6]))
        print("-----------")
        print(" {} | {} | {}".format(self.data[7], self.data[8], self.data[9]))
        
    #here pay attention there is not space between {} 
        
    def change(self, num, k):
        """Function to change the content for the specified cell
           Args:
                num(int): the location of the cell to be changed
                k(string): either X or O 
           Return:
                None
           """
        self.data[num] = k 
        
    def win(self, k):
        """Function to decide whether either side wins the game
            Arg: 
                k(string):either X or O, to evaluate whether either of them is winning
            Return:
                boolean: True if specified one (X or O) is won, False if it has not won yet
            """
        if (self.data[1] == self.data[2] == self.data[3]== k) or \
           (self.data[4] == self.data[5] == self.data[6] == k) or \
           (self.data[7] == self.data[8] == self.data[9] == k) or \
           (self.data[1] == self.data[4] == self.data[7] == k) or \
           (self.data[2] == self.data[5] == self.data[8] == k) or \
           (self.data[3] == self.data[6] == self.data[9] == k) or \
           (self.data[1] == self.data[5] == self.data[9] == k) or \
           (self.data[3] == self.data[5] == self.data[5] == k):
            return True
        else:
            return False 