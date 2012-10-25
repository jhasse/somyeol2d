cpdef bint c_checkCollision(double x, double y, double other_x, double other_y, double width, double height, double other_width, double other_height):
	if (y+height < other_y): return False; # this rect is below the other rect
	if (y > other_y+other_height): return False; # this rect is above the other rect

	if (x+width < other_x): return False; # this rect is right to the other rect
	if (x > other_x+other_width): return False; # this rect is left to the other rect
	return True;

##cdef extern from "c-files.dll":
##    bint c_checlCollision(double,double,double,double,double,double,double,double)
##
##cdef bint checkCollision(double x, double y, double other_x, double other_y, double width, double height, double other_width, double other_height):
##    return c_checkCollision(x, y, other_x, other_y, width, height, other_width, other_height)
