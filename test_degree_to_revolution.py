def degree_to_revolution(self, degree):
    #the angle accuracy will be 1 revolution = 2.25 degree
    #use the absolute positioning, so it will be accurate
    #if using the relative/inceremental positioning, the error will accumulate
    #can be improved by sending the pulse, we have 2500 ppr encoder
    number_of_revolution =  int(4 * degree // 9)
    return number_of_revolution




degree_to_revolution(90)


