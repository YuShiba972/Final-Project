"""
************************
***  author:Yeller   ***
***  date:2023/04/21 ***
************************
"""

class Point:
    def __init__(self, name='', location=None, battery=0, consume=0,
                 max_battery=10800, threshold=0.2, velocity=1):
        self.name = name
        self.location = location
        self.battery = battery

        self.max_battery = max_battery
        self.consume = consume
        self.threshold = threshold
        self.velocity = velocity

    @staticmethod
    def points40_bar10():
        A = Point(name='A', location=[0, 0])

        B = Point(name='B', location=[1, 18])
        C = Point(name='C', location=[18, 1])
        D = Point(name='D', location=[8, 3])
        E = Point(name='E', location=[6, 10])
        F = Point(name='F', location=[15, 15])

        G = Point(name='G', location=[10, 17])
        H = Point(name='H', location=[3, 3])
        I = Point(name='I', location=[16, 6])
        J = Point(name='J', location=[9, 5])
        K = Point(name='K', location=[10, 10])

        L = Point(name='L', location=[14, 1])
        M = Point(name='M', location=[15, 19])
        N = Point(name='N', location=[5, 11])
        O = Point(name='O', location=[7, 18])
        P = Point(name='O', location=[13, 9])

        Q = Point(name='Q', location=[10, 7])
        R = Point(name='R', location=[0, 14])
        S = Point(name='S', location=[9, 18])
        T = Point(name='T', location=[18, 12])
        U = Point(name='U', location=[16, 18])

        V = Point(name='V', location=[4, 6])
        W = Point(name='W', location=[4, 0])
        X = Point(name='X', location=[11, 15])
        Y = Point(name='Y', location=[5, 2])
        Z = Point(name='Z', location=[5, 19])

        AA = Point(name='AA', location=[10, 3])
        BB = Point(name='BB', location=[13, 2])
        CC = Point(name='CC', location=[14, 17])
        DD = Point(name='DD', location=[14, 7])
        EE = Point(name='EE', location=[12, 5])

        FF = Point(name='FF', location=[0, 3])
        GG = Point(name='GG', location=[0, 5])
        HH = Point(name='HH', location=[1, 10])
        II = Point(name='II', location=[1, 8])
        JJ = Point(name='JJ', location=[1, 6])

        KK = Point(name='KK', location=[2, 5])
        LL = Point(name='LL', location=[3, 9])
        MM = Point(name='MM', location=[3, 12])
        NN = Point(name='NN', location=[3, 14])
        OO = Point(name='OO', location=[4, 16])

        points_list = [A, B, C, D, E, F,
                       G, H, I, J, K,
                       L, M, N, O, P,
                       Q, R, S, T, U,
                       V, W, X, Y, Z,
                       AA, BB, CC, DD, EE,
                       FF, GG, HH, II, JJ,
                       KK, LL, MM, NN, OO]

        return points_list

    @staticmethod
    def points35_bar10():
        A = Point(name='A', location=[0, 0])

        B = Point(name='B', location=[1, 18])
        C = Point(name='C', location=[18, 1])
        D = Point(name='D', location=[8, 3])
        E = Point(name='E', location=[6, 10])
        F = Point(name='F', location=[15, 15])

        G = Point(name='G', location=[10, 17])
        H = Point(name='H', location=[3, 3])
        I = Point(name='I', location=[16, 6])
        J = Point(name='J', location=[9, 5])
        K = Point(name='K', location=[10, 10])

        L = Point(name='L', location=[14, 1])
        M = Point(name='M', location=[15, 19])
        N = Point(name='N', location=[5, 11])
        O = Point(name='O', location=[7, 18])
        P = Point(name='O', location=[13, 9])

        Q = Point(name='Q', location=[10, 7])
        R = Point(name='R', location=[0, 14])
        S = Point(name='S', location=[9, 18])
        T = Point(name='T', location=[18, 12])
        U = Point(name='U', location=[16, 18])

        V = Point(name='V', location=[4, 6])
        W = Point(name='W', location=[4, 0])
        X = Point(name='X', location=[11, 15])
        Y = Point(name='Y', location=[5, 2])
        Z = Point(name='Z', location=[5, 19])

        AA = Point(name='AA', location=[10, 3])
        BB = Point(name='BB', location=[13, 2])
        CC = Point(name='CC', location=[14, 17])
        DD = Point(name='DD', location=[14, 7])
        EE = Point(name='EE', location=[12, 5])

        FF = Point(name='FF', location=[0, 3])
        GG = Point(name='GG', location=[0, 5])
        HH = Point(name='HH', location=[1, 10])
        II = Point(name='II', location=[1, 8])
        JJ = Point(name='JJ', location=[1, 6])

        points_list = [A, B, C, D, E, F,
                       G, H, I, J, K,
                       L, M, N, O, P,
                       Q, R, S, T, U,
                       V, W, X, Y, Z,
                       AA, BB, CC, DD, EE,
                       FF, GG, HH, II, JJ, ]

        return points_list

    @staticmethod
    def points30_bar10():
        A = Point(name='A', location=[0, 0])

        B = Point(name='B', location=[1, 18])
        C = Point(name='C', location=[18, 1])
        D = Point(name='D', location=[8, 3])
        E = Point(name='E', location=[6, 10])
        F = Point(name='F', location=[15, 15])

        G = Point(name='G', location=[10, 17])
        H = Point(name='H', location=[3, 3])
        I = Point(name='I', location=[16, 6])
        J = Point(name='J', location=[9, 5])
        K = Point(name='K', location=[10, 10])

        L = Point(name='L', location=[14, 1])
        M = Point(name='M', location=[15, 19])
        N = Point(name='N', location=[5, 11])
        O = Point(name='O', location=[7, 18])
        P = Point(name='O', location=[13, 9])

        Q = Point(name='Q', location=[10, 7])
        R = Point(name='R', location=[0, 14])
        S = Point(name='S', location=[9, 18])
        T = Point(name='T', location=[18, 12])
        U = Point(name='U', location=[16, 18])

        V = Point(name='V', location=[4, 6])
        W = Point(name='W', location=[4, 0])
        X = Point(name='X', location=[11, 15])
        Y = Point(name='Y', location=[5, 2])
        Z = Point(name='Z', location=[5, 19])

        AA = Point(name='AA', location=[10, 3])
        BB = Point(name='BB', location=[13, 2])
        CC = Point(name='CC', location=[14, 17])
        DD = Point(name='DD', location=[14, 7])
        EE = Point(name='EE', location=[12, 5])

        points_list = [A, B, C, D, E, F,
                       G, H, I, J, K,
                       L, M, N, O, P,
                       Q, R, S, T, U,
                       V, W, X, Y, Z,
                       AA, BB, CC, DD, EE]

        return points_list

    @staticmethod
    def points25_bar10():
        A = Point(name='A', location=[0, 0])

        B = Point(name='B', location=[1, 18])
        C = Point(name='C', location=[18, 1])
        D = Point(name='D', location=[8, 3])
        E = Point(name='E', location=[6, 10])
        F = Point(name='F', location=[15, 15])

        G = Point(name='G', location=[10, 17])
        H = Point(name='H', location=[3, 3])
        I = Point(name='I', location=[16, 6])
        J = Point(name='J', location=[9, 5])
        K = Point(name='K', location=[10, 10])

        L = Point(name='L', location=[14, 1])
        M = Point(name='M', location=[15, 19])
        N = Point(name='N', location=[5, 11])
        O = Point(name='O', location=[7, 18])
        P = Point(name='O', location=[13, 9])

        Q = Point(name='Q', location=[10, 7])
        R = Point(name='R', location=[0, 14])
        S = Point(name='S', location=[9, 18])
        T = Point(name='T', location=[18, 12])
        U = Point(name='U', location=[16, 18])

        V = Point(name='V', location=[4, 6])
        W = Point(name='W', location=[4, 0])
        X = Point(name='X', location=[11, 15])
        Y = Point(name='Y', location=[5, 2])
        Z = Point(name='Z', location=[5, 19])
        points_list = [A, B, C, D, E, F,
                       G, H, I, J, K,
                       L, M, N, O, P,
                       Q, R, S, T, U,
                       V, W, X, Y, Z]

        return points_list

    @staticmethod
    def points20_bar10():
        A = Point(name='A', location=[0, 0])

        B = Point(name='B', location=[1, 18])
        C = Point(name='C', location=[18, 1])
        D = Point(name='D', location=[8, 3])
        E = Point(name='E', location=[6, 10])
        F = Point(name='F', location=[15, 15])

        G = Point(name='G', location=[10, 17])
        H = Point(name='H', location=[3, 3])
        I = Point(name='I', location=[16, 6])
        J = Point(name='J', location=[9, 5])
        K = Point(name='K', location=[10, 10])

        L = Point(name='L', location=[14, 1])
        M = Point(name='M', location=[15, 19])
        N = Point(name='N', location=[5, 11])
        O = Point(name='O', location=[7, 18])
        P = Point(name='O', location=[13, 9])

        Q = Point(name='Q', location=[10, 7])
        R = Point(name='R', location=[0, 14])
        S = Point(name='S', location=[9, 18])
        T = Point(name='T', location=[18, 12])
        U = Point(name='U', location=[16, 18])

        points_list = [A, B, C, D, E, F,
                       G, H, I, J, K,
                       L, M, N, O, P,
                       Q, R, S, T, U]
        return points_list

    @staticmethod
    def points15_bar10():
        A = Point(name='A', location=[0, 0])

        B = Point(name='B', location=[1, 18])
        C = Point(name='C', location=[18, 1])
        D = Point(name='D', location=[8, 3])
        E = Point(name='E', location=[6, 10])
        F = Point(name='F', location=[15, 15])

        G = Point(name='G', location=[10, 17])
        H = Point(name='H', location=[3, 3])
        I = Point(name='I', location=[16, 6])
        J = Point(name='J', location=[9, 5])
        K = Point(name='K', location=[10, 10])

        L = Point(name='L', location=[14, 1])
        M = Point(name='M', location=[15, 19])
        N = Point(name='N', location=[5, 11])
        O = Point(name='O', location=[7, 18])
        P = Point(name='O', location=[13, 9])
        points_list = [A, B, C, D, E, F,
                       G, H, I, J, K,
                       L, M, N, O, P]

        return points_list

    @staticmethod
    def points10_bar10():
        A = Point(name='A', location=[0, 0])

        B = Point(name='B', location=[1, 18])
        C = Point(name='C', location=[18, 1])
        D = Point(name='D', location=[8, 3])
        E = Point(name='E', location=[6, 10])
        F = Point(name='F', location=[15, 15])

        G = Point(name='G', location=[10, 17])
        H = Point(name='H', location=[3, 3])
        I = Point(name='I', location=[16, 6])
        J = Point(name='J', location=[9, 5])
        K = Point(name='K', location=[10, 10])

        points_list = [A, B, C, D, E, F,
                       G, H, I, J, K]

        return points_list

    @staticmethod
    def points5_bar10():
        A = Point(name='A', location=[0, 0])

        B = Point(name='B', location=[1, 18])
        C = Point(name='C', location=[18, 1])
        D = Point(name='D', location=[8, 3])
        E = Point(name='E', location=[6, 10])
        F = Point(name='F', location=[15, 15])

        points_list = [A, B, C, D, E, F]

        return points_list

