import sys
     
class PBar:

    def __init__(self, totalItems, size = 100):
        self.totalItems = totalItems
        self.size = size

    def progress(self, current):
        percentComplete = (current / self.totalItems*(1.0))
        percentBar = self.size * (percentComplete * 1)  

        prog = ""

        for i in range(0, self.size + 1):
            if i <= percentBar:
                prog += "|"
            else:
                prog += " "

        sys.stdout.flush()
        sys.stdout.write("\r[" + prog + "] " + "{:.2%}".format(percentComplete)) 

