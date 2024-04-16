import linecache
import win32com.client as wc

def give_array2(file):


    layer_counter = 0
    line_counter = 0
    continue_read2 = False
    flag = None
    control = False

    sum_coordinates_wall_outer1 = []
    sum_coordinates_wall_outer2 = []
    sum_coordinates_wall_outer3 = []
    sum_coordinates_wall_outer4 = []
    sum_coordinates_wall_outer5 = []
    sum_mesh_eraser1 = []
    sum_mesh_eraser2 = []
    sum_fill = []
    sum_fill2 = []
    coordinates_wall_outer1 = []
    coordinates_wall_outer2 = []
    coordinates_wall_outer3 = []
    coordinates_wall_outer4 = []
    coordinates_wall_outer5 = []
    coordinates_mesh_eraser = []
    coordinates_fill = []
    coordinates_fill2 = []
    coordinates_mesh_eraser2 = []
    wall_outer = 0
    fill_counter = 1

    def read(array):

        same = False
        G1_control = False

        if line.startswith('G0'):
            next_line = linecache.getline(file, line_counter + 1)
            next_line2 = linecache.getline(file, line_counter + 2)
            if next_line.startswith('G1'):
                parts = next_line.split()  # Satırı boşluklara göre ayır
                for part in parts:
                    if part.startswith('X'):
                        G1_control = True
            if next_line.startswith('G0'):
                pass

            elif G1_control:

                if flag == "fill" or flag == "fill2":
                    array.append([None, None])
                parts = line.split()  # Satırı boşluklara göre ayır
                for part in parts:
                    if part.startswith('X'):
                        x_coordinate = float(part[1:])  # X koordinatını al
                        same = True
                    elif part.startswith('Y'):
                        y_coordinate = float(part[1:])  # Y koordinatını al
                if same:
                    array.append([x_coordinate/10, y_coordinate/10])
            elif G1_control == False and next_line2.startswith('G1') and next_line.startswith('G1'):
                if flag == "fill" or flag == "fill2":
                    array.append([None, None])
                parts = line.split()  # Satırı boşluklara göre ayır
                for part in parts:
                    if part.startswith('X'):
                        x_coordinate = float(part[1:])  # X koordinatını al
                        same = True
                    elif part.startswith('Y'):
                        y_coordinate = float(part[1:])  # Y koordinatını al
                if same:
                    array.append([x_coordinate/10, y_coordinate/10])
            else:
                pass
        if line.startswith('G1'):
            parts = line.split()
            for part in parts:
                if part.startswith('X'):
                    same = True
                    x_coordinate = float(part[1:])
                elif part.startswith('Y'):
                    y_coordinate = float(part[1:])
            if same:
                array.append([x_coordinate/10, y_coordinate/10])
        else:
            pass
    with open(file, 'r') as text:

        for line in text:
            line_counter += 1
            if f';LAYER:{layer_counter}' in line:
                wall_outer = 0
                fill_counter = 1
                if layer_counter > 0:
                    coordinates_mesh_eraser2 = coordinates_mesh_eraser2[0:5]
                    if len(coordinates_fill2) < 3:
                        coordinates_fill2 = []
                    sum_coordinates_wall_outer1.append(coordinates_wall_outer1)
                    sum_coordinates_wall_outer2.append(coordinates_wall_outer2)
                    sum_coordinates_wall_outer3.append(coordinates_wall_outer3)
                    sum_coordinates_wall_outer4.append(coordinates_wall_outer4)
                    sum_coordinates_wall_outer5.append(coordinates_wall_outer5)
                    sum_mesh_eraser1.append(coordinates_mesh_eraser)
                    sum_fill.append(coordinates_fill)
                    sum_fill2.append(coordinates_fill2)
                    sum_mesh_eraser2.append(coordinates_mesh_eraser2)


                    coordinates_wall_outer1 = []
                    coordinates_wall_outer2 = []
                    coordinates_wall_outer3 = []
                    coordinates_wall_outer4 = []
                    coordinates_wall_outer5 = []
                    coordinates_mesh_eraser = []
                    coordinates_mesh_eraser2 = []
                    coordinates_fill = []
                    coordinates_fill2 = []


            if ';TYPE:WALL-OUTER' in line:
                control = False
                wall_outer += 1
                previous_line = linecache.getline(file, line_counter - 1)
                if previous_line.startswith('G0'):

                    parts = previous_line.split()
                    for part in parts:
                        if part.startswith('X'):
                            x_coordinate = float(part[1:])
                        elif part.startswith('Y'):
                            y_coordinate = float(part[1:])
                    if wall_outer == 1:
                        coordinates_wall_outer1.append([x_coordinate/10, y_coordinate/10])
                        flag = "wall_outer1"
                    elif wall_outer == 2:
                        coordinates_wall_outer2.append([x_coordinate/10, y_coordinate/10])
                        flag = "wall_outer2"
                    elif wall_outer == 3:
                        coordinates_wall_outer3.append([x_coordinate/10, y_coordinate/10])
                        flag = "wall_outer3"
                    elif wall_outer == 4:
                        coordinates_wall_outer4.append([x_coordinate/10, y_coordinate/10])
                        flag = "wall_outer4"
                    elif wall_outer == 5:
                        coordinates_wall_outer5.append([x_coordinate/10, y_coordinate/10])
                        flag = "wall_outer5"
                continue_read2 = True

            if ';MESH:Eraser(3)' in line and (layer_counter<3 or layer_counter>106):
                control = False
                previous_line = linecache.getline(file, line_counter - 1)
                if previous_line.startswith('G0'):
                    parts = previous_line.split()
                    for part in parts:
                        if part.startswith('X'):
                            x_coordinate = float(part[1:])
                        elif part.startswith('Y'):
                            y_coordinate = float(part[1:])
                    coordinates_mesh_eraser2.append([x_coordinate/10, y_coordinate/10])
                flag = "mesh_eraser2"
                continue_read2 = True

            if ';TYPE:FILL' in line:
                control = False
                if fill_counter > 1 and fill_counter < 4:
                    if fill_counter == 3:
                        coordinates_fill2 = []
                    previous_line = linecache.getline(file, line_counter - 1)
                    if previous_line.startswith('G0'):
                        parts = previous_line.split()
                        for part in parts:
                            if part.startswith('X'):
                                x_coordinate = float(part[1:])
                            elif part.startswith('Y'):
                                y_coordinate = float(part[1:])
                        coordinates_fill2.append([x_coordinate/10, y_coordinate/10])
                    flag = "fill2"
                    continue_read2 = True

                elif fill_counter == 1:
                    previous_line = linecache.getline(file, line_counter - 1)
                    next_line = linecache.getline(file, line_counter + 1)
                    if previous_line.startswith('G0'):
                        parts = previous_line.split()
                        for part in parts:
                            if part.startswith('X'):
                                x_coordinate = float(part[1:])
                            elif part.startswith('Y'):
                                y_coordinate = float(part[1:])
                        coordinates_fill.append([x_coordinate/10, y_coordinate/10])
                    if next_line.startswith(';MESH:Eraser(2)'):
                        previous_line2 = linecache.getline(file, line_counter - 3)
                        parts = previous_line2.split()
                        for part in parts:
                            if part.startswith('X'):
                                x_coordinate = float(part[1:])
                            elif part.startswith('Y'):
                                y_coordinate = float(part[1:])
                        coordinates_fill.append([x_coordinate/10, y_coordinate/10])

                    flag = "fill"
                    continue_read2 = True

                fill_counter += 1
            if ';MESH:Eraser(1)' in line and (layer_counter < 5 or layer_counter > 104):

                control = False
                previous_line = linecache.getline(file, line_counter - 1)
                if previous_line.startswith('G0'):
                    parts = previous_line.split()
                    for part in parts:
                        if part.startswith('X'):
                            x_coordinate = float(part[1:])
                        elif part.startswith('Y'):
                            y_coordinate = float(part[1:])
                    coordinates_mesh_eraser.append([x_coordinate/10, y_coordinate/10])
                flag = "mesh_eraser"
                continue_read2 = True
            if line.startswith(';TIME_ELAPSED'):
                layer_counter += 1

            if continue_read2 and line.startswith('G'):

                control = True
                if flag == "wall_outer1":
                    read(coordinates_wall_outer1)
                if flag == "wall_outer2":
                    read(coordinates_wall_outer2)
                if flag == "wall_outer3":
                    read(coordinates_wall_outer3)
                if flag == "wall_outer4":
                    read(coordinates_wall_outer4)
                if flag == "wall_outer5":
                    read(coordinates_wall_outer5)
                if flag == "mesh_eraser":
                    read(coordinates_mesh_eraser)
                if flag == "mesh_eraser2":

                    read(coordinates_mesh_eraser2)
                if flag == "fill":
                    read(coordinates_fill)
                if flag == "fill2":
                    read(coordinates_fill2)
            if continue_read2 and control and line.startswith(';'):
                continue_read2 = False
    coordinates_mesh_eraser2 = coordinates_mesh_eraser2[0:5]
    sum_coordinates_wall_outer1.append(coordinates_wall_outer1)
    sum_coordinates_wall_outer2.append(coordinates_wall_outer2)
    sum_coordinates_wall_outer3.append(coordinates_wall_outer3)
    sum_coordinates_wall_outer4.append(coordinates_wall_outer4)
    sum_coordinates_wall_outer5.append(coordinates_wall_outer5)
    sum_mesh_eraser1.append(coordinates_mesh_eraser)
    sum_mesh_eraser2.append(coordinates_mesh_eraser2)
    sum_fill.append(coordinates_fill)
    sum_fill2.append(coordinates_fill2)

    return sum_coordinates_wall_outer1,sum_coordinates_wall_outer2,sum_coordinates_wall_outer3,sum_coordinates_wall_outer4,sum_coordinates_wall_outer5,sum_mesh_eraser1,sum_mesh_eraser2,sum_fill,sum_fill2








