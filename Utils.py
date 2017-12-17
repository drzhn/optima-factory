class Utils:

    # поиск компонент связности. m - двумерная матрица связности
    @staticmethod
    def connection_components(m):
        sets = []
        for i in range(len(m)):
            s = set()
            s.add(i)
            for j in range(len(m)):
                if m[i][j] > 0:
                    s.add(j)
            sets.append(s)

        for i in range(len(sets)):
            for j in range(len(sets)):
                if i != j:
                    if not sets[i].isdisjoint(sets[j]):
                        sets[i] = sets[i].union(sets[j])
                        # sets.remove(sets[j])
        # print(sets)
        ret = []
        for s in sets:
            if not list(s) in ret:
                ret.append(list(s))
        return ret
        # print(ret)