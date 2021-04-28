def correct_placement(coordinate, size, map_size):
    corner_list = find_corners(coordinate, size)
    ref_space = move_onto_map(corner_list, map_size)
    return ref_space

def find_corners(coordinate, size):
    if size == 'large':
        offset = 1
    elif size == 'huge':
        offset = 2
    else:
        offset = 3
    top_left = coordinate
    top_right = [
        coordinate[0] + offset,
        coordinate[1],
        coordinate[2]
        ]   
    bottom_left = [
        coordinate[0],
        coordinate[1] + offset,
        coordinate[2]
        ]
    bottom_right = [
        coordinate[0] + offset,
        coordinate[1] + offset,
        coordinate[2]
        ]
    return [top_left, top_right, bottom_left, bottom_right]

def move_onto_map(corner_list, map_size):
    ref_space = corner_list[0]
    top_right = corner_list[1]
    bottom_left = corner_list[2]
    bottom_right = corner_list[3]
    while check_if_in_map(corner_list, map_size) == False:
        for corner in corner_list:
            if corner[0] < 0:
                delta = 0 - corner[0]
                ref_space[0] += delta
                top_right[0] += delta
                bottom_left[0] += delta
                bottom_right[0] += delta
                break
            elif corner[0] > map_size[0] - 1:
                delta = corner[0] - map_size[0] + 1
                ref_space[0] -= delta
                top_right[0] -= delta
                bottom_left[0] -= delta
                bottom_right[0] -= delta
                break
            if corner[1] < 0:
                delta = 0 - corner[1]
                ref_space[1] += delta
                top_right[1] += delta
                bottom_left[1] += delta
                bottom_right[1] += delta
                break
            elif corner[1] > map_size[1] - 1:
                delta = corner[1] - map_size[1] + 1
                ref_space[1] -= delta
                top_right[1] -= delta
                bottom_left[1] -= delta
                bottom_right[1] -= delta
                break
        corner_list = [ref_space, top_right, bottom_left, bottom_right]
    return ref_space

def check_if_in_map(corner_list, map_size):
    on_map = True
    for corner in corner_list:
        if corner[0] < 0 or corner[0] > map_size[0] - 1:
            on_map = False
            return on_map
        if corner[1] < 0 or corner[1] > map_size[1] - 1:
            on_map = False
            return on_map
    return on_map