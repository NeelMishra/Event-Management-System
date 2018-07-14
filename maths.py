import pdb

def reference(mouse_coordinates, image_dimension):

    UL  = image_dimension
    LL = 0
    divider = 1
    midpoint = (UL + LL) // 2
    directions = []

    if(mouse_coordinates == UL):
        return (0, [1])

    elif(mouse_coordinates == LL):
        return (0, [-1])

    while(True):


        
        
        if (mouse_coordinates == midpoint):
            return (divider,directions)

        else:
            if(mouse_coordinates > midpoint):
                LL = midpoint
                divider += 1
                midpoint = round(((UL + LL) //2))
                directions.append(1)

            else:
                UL = midpoint
                divider += 1
                midpoint = round(((UL + LL) // 2))
                directions.append(-1)


    

def step_finder(mouse_coordinates, image_dimension):

    UL  = image_dimension
    LL = [0,0]
    divider = [0,0]
    midpoint = [(UL[0] + LL[0]) // 2, (UL[1] + LL[1]) // 2]
    direction = [[],[]]

    if(mouse_coordinates == UL[0] and mouse_coordinates == UL[1]):
        return (0, [[1],[1]])

    elif(mouse_coordinates == LL[1] and mouse_coordinates == LL[1]):
        return (0, [[1],[1]])



    while(True):
        #FOR Y
        #pdb.set_trace()

        if(mouse_coordinates[1] == LL[1]):
            if(divider[1] == 0):
                direction[1] = [-1]
                break

        if(mouse_coordinates[1] == UL[1]):
            if(divider[1] == 0):
                direction[1] = [1]
                break

        
        if(mouse_coordinates[1] == midpoint[1]):
            break

        
        

        else:
            if(mouse_coordinates[1] > midpoint[1]):
                LL[1] = midpoint[1]
                divider[1] += 1
                midpoint[1] = round(((UL[1] + LL[1]) // 2))
                direction[1].append(1)

            else:
                UL[1] = midpoint[1]
                divider[1] += 1
                midpoint[1] = round(((UL[1] + LL[1]) // 2))
                direction[1].append(-1)

        

    while(True):
        #FOR X
        #pdb.set_trace()

        if(mouse_coordinates[0] == LL[0]):
            if(divider[0] == 0):
                direction[0] = [-1]
                break

        if(mouse_coordinates[0] == UL[0]):
            if(divider[0] == 0):
                direction[0] = [1]
                break

        
        if ((mouse_coordinates[0] == midpoint[0])):
            if(divider[0] == 0):
                direction[0] = [1]
            break

        else:

            
            if(mouse_coordinates[0] > midpoint[0]):
                LL[0] = midpoint[0]
                divider[0] += 1
                midpoint[0] = round(((UL[0] + LL[0]) // 2))
                direction[0].append(1)

            else:
                UL[0] = midpoint[0]
                divider[0] += 1
                midpoint[0] = round(((UL[0] + LL[0]) // 2))
                direction[0].append(-1)

            #FOR Y
            

    return [divider, direction]

def value_finder(steps, image_dimension):


    pointer = [None, None]
    
    while(steps[0] != 0):
        pointer[0] /= 0
        step -= 1


    

