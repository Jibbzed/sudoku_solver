import tkinter as tk

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Sudoku Solver')
        self.root.geometry('600x600')

        # Put a simple label for now
        self.label = tk.Label(self.root, text='Sudoku Solver', font=('Calibri', 16))
        self.label.pack()

        # Create the puzzle
        self.board = tk.Frame(self.root, bg='white')
        self.board.pack()

        # Create the 3*3 boxes
        self.boxes = []
        for r in range(3):
            row = []
            for col in range(3):
                box = tk.Frame(self.board, highlightbackground='light blue', highlightthickness=2, width=150, height=150)
                box.grid(row=r, column=col)
                row.append(box)
            self.boxes.append(row)
        
        # Create the cells
        self.cells = []
        for r in range(9):
            row = []
            for col in range(9):
                cellFrame = tk.Frame(self.boxes[r//3][col//3], height=50, width=50, bg='white', highlightbackground='black', highlightthickness=1)
                cellFrame.grid(row=r%3, column=col%3, sticky='nsew')
                cellFrame.rowconfigure(0, minsize=50, weight=1)
                cellFrame.columnconfigure(0, minsize=50, weight=1)
                #cell = tk.Button(cellFrame, bg='white')
                #cell.pack(fill='both', expand=True)
                row.append(cellFrame)
            self.cells.append(row)

    def mainloop(self):
        self.root.mainloop()

if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()