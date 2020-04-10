class MyList(list):

    def __sub__(self, other):
        # if type(other) == list:
        #     other = MyList(other)
        l1, l2 = len(self), len(other)
        new_lst = []
        for i in range(min(l1, l2)):
            new_lst.append(self[i] - other[i])

        if l1 >= l2:
            new_lst.extend(self[l2:])
        else:
            new_lst.extend(other[l1:])
        return MyList(new_lst)

    def __isub__(self, other):
        return self.__sub__(other)

    def __add__(self, other):
        # if type(other) == list:
        #     other = MyList(other)
        l1, l2 = len(self), len(other)
        new_lst = []
        for i in range(min(l1, l2)):
            new_lst.append(self[i] + other[i])

        if l1 >= l2:
            new_lst.extend(self[l2:])
        else:
            new_lst.extend(other[l1:])
        return MyList(new_lst)

    def __iadd__(self, other):
        return self.__add__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)
