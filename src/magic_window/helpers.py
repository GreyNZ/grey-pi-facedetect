def return_largest(a,b):
    """Compare a,b and reutrn largest"""
    
    def calculate_delta(x):
        """calculate the size of face"""
        _,_,w,h = x
        return w * h
    
    if calculate_delta(a) > calculate_delta(b):
        return a
    else:
        return b
    
    