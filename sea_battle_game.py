import random
import copy


class SeaBattleGame:
    def __init__(self):
        self.__sea = [[0] * 10 for _ in range(10)]

    # ------------- Random ships placement block ------------- #
    # Generation of random indices and ship position (vertical or horizontal).
    @staticmethod
    def __i_j_route():
        i = random.choice((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
        j = random.choice((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
        route = random.choice(('vertical', 'horizontal'))
        return i, j, route

    # The function searches for the correct location for the ship and returns the sea with a new ship,
    # if no location is found - it returns the sea unchanged.
    @staticmethod
    def __form_ship(sea_f, width, height, i_f, j_f):
        sea = copy.deepcopy(sea_f)
        total = 0
        hor_start_build = j_f + ((j_f + width) // 10) * (10 - (j_f + width))
        hor_start_chek = hor_start_build - {0: 0, 1: 1}[j_f - 1 >= 0]
        vert_start_chek = i_f - {0: 0, 1: 1}[i_f - 1 >= 0]
        vert_count_chek = height + 2 - {0: 0, 1: 1}[9 - i_f == 0] - {0: 1, 1: 0}[i_f - 1 >= 0]
        try:
            for vert_chek in range(vert_count_chek):
                total += sum(sea[vert_start_chek + vert_chek][hor_start_chek: hor_start_build + width + 2])
        except IndexError:
            return sea
        if total == 0:
            for vert_build in range(height):
                for hor_build in range(width):
                    sea[i_f + vert_build][hor_start_build + hor_build] = 1
        return sea

    # The main function. Generates the count and size of ships, placing them at random.
    def ships_randomizer(self):
        sea = [[0] * 10 for _ in range(10)]
        for ship_size in (4, 3, 2, 1):
            for ship_count in range(5-ship_size):
                while True:
                    i, j, route = self.__i_j_route()
                    wid = {'vertical': 1, 'horizontal': ship_size}[route]
                    hei = {'vertical': ship_size, 'horizontal': 1}[route]
                    new_sea = self.__form_ship(sea, wid, hei, i, j)
                    if sea != new_sea:
                        sea = copy.deepcopy(new_sea)
                        break
        return sea
    # ----------- END Random ships placement block ----------- #

    # ------------- Manual ships placement block ------------- #
    # Takes a list of manually set coordinates ('ij', 'ij') and puts ships on the field
    @staticmethod
    def manual_placement_marking(lst_manual_coord):
        new_sea = [[0] * 10 for _ in range(10)]
        for coord in lst_manual_coord:
            new_sea[int(coord[0])][int(coord[1])] = 1
        return new_sea
    # ----------- END Manual ships placement block ----------- #

    # -- Block for checking the correct placement of ships --- #
    # Check for a position with a value = 0
    @staticmethod
    def __zero_f(shs, i_f, j_f):
        h = shs[i_f][j_f - 1] + shs[i_f - 1][j_f] == 2 or shs[i_f][j_f + 1] + shs[i_f - 1][j_f] == 2
        k = shs[i_f][j_f + 1] + shs[i_f + 1][j_f] == 2 or shs[i_f][j_f - 1] + shs[i_f + 1][j_f] == 2
        return h or k

    # Check for a position with a value = 1
    @staticmethod
    def __one_f(sps, i_x, j_x):
        return sps[i_x-1][j_x-1] + sps[i_x-1][j_x+1] + sps[i_x+1][j_x-1] + sps[i_x+1][j_x+1] > 0

    # Checks for intersection ships
    def intersection_reviewer(self, ships_f):
        errors_col = []
        for i in range(1, 9):
            for j in range(1, 9):
                if {0: self.__zero_f, 1: self.__one_f}[ships_f[i][j]](ships_f, i, j):
                    errors_col.append((i, j))
        # List of coordinates as a tuple (i, j) with incorrect ships positions
        return errors_col

    # Collects lists with coordinates of all available ships in a list
    # A field of '0' arrives at the entrance with marks of ships in the form of '1'
    @staticmethod
    def ships_counter(ships_x):
        ships_col, one_ship, added_coord = [], [], []

        def add_coord(I, J):
            nonlocal one_ship, added_coord
            one_ship.append((I, J))
            added_coord.append((I, J))

        def add_ship():
            nonlocal ships_col, one_ship
            ships_col.append(one_ship)
            one_ship = []

        def down_i(i_x, j_x):
            nonlocal ships_x
            try:
                down_i = ships_x[i_x + 1][j_x]
            except IndexError:
                down_i = 0
            return down_i

        for i in range(10):
            for j in range(10):
                vert_zero = {0: ships_x[i-1][j], 1: 0}[i == 0] + down_i(i, j) == 0
                next_value = sum(ships_x[i][j+1: j+2])
                try:
                    {1: {1: add_coord}}[ships_x[i][j]][vert_zero](i, j)
                    {1: {1: {0: add_ship}}}[ships_x[i][j]][vert_zero][next_value]()
                except KeyError:
                    pass
        for j in range(10):
            for i in range(10):
                try:
                    {1: {1: add_coord}}[ships_x[i][j]][(i, j) not in added_coord](i, j)
                    {1: {0: add_ship}}[ships_x[i][j]][down_i(i, j)]()
                except KeyError:
                    pass
        # List of coordinates as a tuple (i, j) with a ships positions
        return ships_col

    # Displays statistics on the correct placement and the count of ships
    # At the entrance, a list with the coordinates of the wrong positions,
    # as well a list with the coordinates of the existing ships.
    @staticmethod
    def resultant(errors_lst, ships_lst):
        is_intersection = ('Error - ships intersecting', 'Good - no crossing ships')[len(errors_lst) == 0]
        res = {'Allocation': '', 'Ships count': ''}
        ships_lst.sort(key=lambda shp: len(shp), reverse=True)
        reference_ships_count = {'Allocation': '', 'Ships count': '', '4-deck ships': 1,
                                 '3-deck ships': 2, '2-deck ships': 3, '1-deck ships': 4}

        for ship in ships_lst:
            res[f'{len(ship)}-deck ships'] = res.get(f'{len(ship)}-deck ships', 0) + 1

        shc = ('Wrong', 'Correct')[reference_ships_count == res]
        res['Ships count'] = shc
        res['Allocation'] = is_intersection

        return res

    # Generate of a random number of shots
    @staticmethod
    def counter_fire():
        fire_container = (0, 1, 2, 3, 4, 5, 1, 2, 3, 4, 1, 2, 3, 1, 2, 1)
        return random.choice(fire_container)

    # Mark the shot coordinates
    @staticmethod
    def clarif_damage(actual_matrix, fire_lst, count_shoot):
        random.shuffle(fire_lst)
        for i in range(count_shoot):
            try:
                actual_matrix[int(fire_lst[i][0])][int(fire_lst[i][1])] -= 5
            except IndexError:
                break
        return actual_matrix

    # Counts the number of undamaged decks, and also reveals the coordinates at which it makes no sense to shoot
    @staticmethod
    def counting_survivors(actual_sea):
        total = 0
        not_shoot = set()
        for i in range(10):
            for j in range(10):
                if actual_sea[i][j] == 1:
                    total += 1

                if actual_sea[i][j] == -4:
                    for k in range(4):
                        a, b = ((i-1, j-1), (i-1, j+1), (i+1, j+1), (i+1, j-1))[k]
                        if (-1 < a < 10) and (-1 < b < 10):
                            not_shoot.add(str(a) + str(b))
        return total, not_shoot

    # --- END Block for checking the correct placement of ships --- #
