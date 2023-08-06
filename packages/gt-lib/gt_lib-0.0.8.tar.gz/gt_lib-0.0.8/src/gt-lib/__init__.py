class gt_lib:
    # First we create a constructor for this class
    # and add members to it, here models
    def __init__(self):
        self.models = ['i8', 'x1', 'x5', 'x6']
   
    # A normal print function
    def test(self):
        print("Test fn", self.models)