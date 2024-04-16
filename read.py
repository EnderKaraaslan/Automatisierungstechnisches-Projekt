import linecache


def give_array(file):
    #integer variables
    layer_counter = 0
    wallouter_counter = 0
    line_counter = 0

    #boolean variables
    continue_read = False
    flag = None #checks which part we're on
    control = False #checks if we should write to array

    #temporary arrays
    coordinates_wall_outer = []
    coordinates_wall_outer2 = []
    coordinates_fill = []

    #main arrays
    sum_coordinates_wall_outer = []
    sum_coordinates_wall_outer2 = []
    sum_coordinates_fill = []


    def read(array):

        #variables
        same = False
        main_control = False

        #Controls required to add to array
        if flag == "fill":
            main_control = True
        if line.startswith('G0'):
            next_line = linecache.getline(file, line_counter + 1) #check the next line
            if next_line.startswith('G1'):
                parts = next_line.split()  #Separate line by spaces
                for part in parts:
                    if part.startswith('X'):
                        main_control = True
            if next_line.startswith('G0'):
                pass

            elif main_control:
                array.append([None, None])
                parts = line.split()  #Separate line by spaces
                for part in parts:
                    if part.startswith('X'):
                        x_coordinate = float(part[1:])  # Take the X coordinate
                        same = True
                    elif part.startswith('Y'):
                        y_coordinate = float(part[1:])  # Take the X coordinate
                if same:
                    array.append([x_coordinate/10, y_coordinate/10]) # add to array

        if line.startswith('G1'):
            parts = line.split()
            for part in parts:
                if part.startswith('X'):
                    same = True
                    x_coordinate = float(part[1:])# Take the X coordinate
                elif part.startswith('Y'):
                    y_coordinate = float(part[1:])# Take the X coordinate
            if same:
                array.append([x_coordinate/10, y_coordinate/10]) # add to array


    #read file
    with open(file, 'r') as text:

        #read line by line
        for line in text:
            line_counter += 1
            #work on each layer
            if f';LAYER:{layer_counter}' in line:


                #edits after each layer
                if layer_counter > 0:
                    sum_coordinates_wall_outer.append(coordinates_wall_outer)
                    sum_coordinates_wall_outer2.append(coordinates_wall_outer2)
                    sum_coordinates_fill.append(coordinates_fill)

                    coordinates_wall_outer = []
                    coordinates_wall_outer2 = []
                    coordinates_fill = []

            # start reading if the line is equal to ;TYPE:WALL-OUTER
            if ';TYPE:WALL-OUTER' in line:
                control = False
                wallouter_counter += 1
                previous_line = linecache.getline(file, line_counter - 1)
                if previous_line.startswith('G0'):
                    parts = previous_line.split()
                    for part in parts:
                        if part.startswith('X'):
                            x_coordinate = float(part[1:])
                        elif part.startswith('Y'):
                            y_coordinate = float(part[1:])

                    #There's more than one ;TYPE:WALL-OUTER. We must therefore understand which one it is
                    if wallouter_counter % 2 == 1:
                        flag = "wall_outer" #flag adjustment
                        coordinates_wall_outer.append([x_coordinate/10, y_coordinate/10])
                        continue_read = True #keep saving to array
                    else:
                        flag = "wall_outer2" #flag adjustment
                        coordinates_wall_outer2.append([x_coordinate/10, y_coordinate/10])
                        continue_read = True #keep saving to array

                #flag adjustment
                if wallouter_counter % 2 == 1:
                    flag = "wall_outer"
                elif wallouter_counter % 2 == 0:
                    flag = "wall_outer2"

            # start reading if the line is equal to ;TYPE:FILL
            if ';TYPE:FILL' in line and (wallouter_counter % 2 == 0):
                control = False
                previous_line = linecache.getline(file, line_counter - 1)
                if previous_line.startswith('G0'):
                    parts = previous_line.split()
                    for part in parts:
                        if part.startswith('X'):
                            x_coordinate = float(part[1:])
                        elif part.startswith('Y'):
                            y_coordinate = float(part[1:])
                    flag = "fill" #flag adjustment
                    coordinates_fill.append([x_coordinate/10, y_coordinate/10])
                    continue_read = True #keep saving to array
                flag = "fill" #flag adjustment

            #Understanding that the layer has changed
            if line.startswith(';TIME_ELAPSED'):
                layer_counter += 1



            #start writing to array
            if continue_read and line.startswith('G'):
                control = True
                if flag == "wall_outer":
                    read(coordinates_wall_outer)
                if flag == "wall_outer2":
                    read(coordinates_wall_outer2)
                if flag == "fill":
                    read(coordinates_fill)


            # finish writing to array
            if continue_read and control and line.startswith(';'):
                continue_read = False


    #adding the last layer
    sum_coordinates_wall_outer.append(coordinates_wall_outer)
    sum_coordinates_wall_outer2.append(coordinates_wall_outer2)
    sum_coordinates_fill.append(coordinates_fill)

    return sum_coordinates_wall_outer, sum_coordinates_wall_outer2, sum_coordinates_fill