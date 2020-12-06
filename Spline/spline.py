#Program Cubic Spline
#Tugas Akhir Metode Numerik
#FTI Universitas Tarumanagara
#Teknik Informatika
#Referensi dari:
#https://mathworld.wolfram.com/CubicSpline.html

import math

class Matrix:
    '''
    Kelas ini digunakan untuk mendefinisikan matriks.
    Hanya metode yang diperlukan untuk penghitungan spline saja yang dimasukan.
    '''
    def __init__(self, col:int, row:int):
        self.values = [[0 for _ in range(col)] for _ in range(row)]
        self.col = col
        self.row = row

    '''
    Menghitung inverse dari matriks menggunakan diagonalisasi matriks
    '''
    def inverse(self):
        assert (self.col == self.row), 'dimensi dari baris dan kolom harus sama'

        #Menggabungkan matrix dengan matrix identitas untuk menghitung matriks inverse
        mirrorMatrix = self.appendMatrix(IdentityMatrix(self.col))
        
        #Melakukan pendiagonalisasian pada matriks
        #Dimulai dengan mengenolkan segitiga bawah
        for x in range(self.col):
            yTest = x
            maxMat = mirrorMatrix.values[yTest][x]
            indexMax = yTest
            for y in range(x, self.row):
                if mirrorMatrix.values[y][x] > maxMat:
                    maxMat = mirrorMatrix.values[y][x]
                    indexMax = y
            assert (maxMat != 0), 'inversi matriks tidak dapat dicari'
            if (indexMax != yTest):
                mirrorMatrix.values[yTest], mirrorMatrix.values[indexMax] = mirrorMatrix.values[indexMax], mirrorMatrix.values[y]
            multiplier = 1/mirrorMatrix.values[indexMax][x]
            mirrorMatrix.values[indexMax] = [i * multiplier for i in mirrorMatrix.values[indexMax]]
            for y in range(indexMax+1, self.row):
                if(mirrorMatrix.values[y][x] != 0):
                    multiplier = mirrorMatrix.values[y][x]
                    for i in range(x, mirrorMatrix.col):
                        mirrorMatrix.values[y][i] -= mirrorMatrix.values[indexMax][i] * multiplier
        
        #Pengenolan segitiga atas
        for x in reversed(range(self.col)):
            for y in reversed(range(x)):
                multiplier = mirrorMatrix.values[y][x]
                for i in range(x, mirrorMatrix.col):
                    mirrorMatrix.values[y][i] -= mirrorMatrix.values[x][i] * multiplier

        #Mengambil matrix sebelah kanan, yang merupakan inverse dari matriks awal
        retMatrix = Matrix(self.col, self.row)
        retMatrix.values = [mirrorMatrix.values[i][self.col:] for i in range(self.row)]
        return retMatrix

    """
    Fungsi ini menggabungkan dua buah matriks.
    Mis:
    A = [ 0 1 2
          3 4 5 ]
    B = [ 2 3 4 
          3 2 1]
    A.appendMatrix(B) = [ 0 1 2 2 3 4
                          3 4 5 3 2 1]
    """
    def appendMatrix(self, right:'Matrix'):
        assert (self.row == right.row), 'jumlah baris kedua matriks harus sama'
        appendedMatrix = Matrix(self.col + right.col, self.row)
        for y in range(self.row):
            for x in range(self.col):
                appendedMatrix.values[y][x] = self.values[y][x]
        for y in range(right.row):
            for x in range(right.col):
                appendedMatrix.values[y][self.col+x] = right.values[y][x]
        return appendedMatrix

    """
    Melakukan perhitungan perkalian matriks
    """
    def __mul__(self, o:'Matrix'):
        assert(self.col == o.row), 'kolom matriks kanan harus sama dengan baris matriks kiri'
        retMatrix = Matrix(o.col, self.row)
        size = self.col
        for row in range(retMatrix.row):
            for col in range(retMatrix.col):
                value = 0
                left = self.getRow(row)
                right = o.getCol(col)
                for i in range(size):
                    value += left[i] * right[i]
                retMatrix.values[row][col] = value
        return retMatrix

    """
    Ambil satu baris matriks
    """
    def getRow(self, row: int):
        assert(row < self.row), 'diluar batas baris'
        return self.values[row]
    
    """
    Ambil satu kolom matriks
    """
    def getCol(self, col: int):
        assert (col < self.col), 'diluar batas kolom'
        return [self.values[i][col] for i in range(self.row)]


class IdentityMatrix(Matrix):
    """
    Kelas ini menciptakan matriks identitas size x size.
    """
    def __init__(self, size:int):
        self.col = size
        self.row = size
        self.values = [[0 for _ in range(size)] for _ in range(size)]

        for y in range(size):
            for x in range(size):
                if(x == y):
                    self.values[y][x] = 1

class TridiagonalMatrix(Matrix):
    """
    Kelas ini menciptakan matriks tridiagonal size x size
    (Digunakan untuk pencarian nilai D)
    Mis:
    size = 4
    closed = False
    Matriks =
    [ 2 1 0 0
      1 4 1 0
      0 1 4 1
      0 0 1 2 ]
    Untuk referensi lanjutan: https://en.wikipedia.org/wiki/Tridiagonal_matrix
    """
    def __init__(self, size:int, closed:bool = False):
        self.col = size
        self.row = size
        self.values = [[0 for x in range(size)] for y in range(size)]

        for y in range(size):
            for x in range(size):
                if(x == y):
                    self.values[y][x] = 4
                elif(abs(x-y) == 1):
                    self.values[y][x] = 1
        
        if(closed):
            self.values[size-1][0] = 1
            self.values[0][size-1] = 1
        else:
            self.values[0][0] = 2
            self.values[size-1][size-1] = 2

class CubicSpline:
    """
    Kelas untuk membuat spline cubic
    input berupa list berisi nilai float.
    ex: CubicSpline([5, 2, 3, 1, 4])
    """
    def __init__(self, points:list, closed: bool = False):
        self.__points = points
        self.size = len(points)
        self.__dMat = Matrix(1, self.size)
        self.isClosed = closed
        self.__recalculate__()
    
    """
    Menciptakan matriks D dengan menggunakan matriks tridiagonal
    """
    def __recalculate__(self):
        yEq = Matrix(1, self.size)
        #Menghitung isi dari matriks Y
        for i in range(self.size):
            if not (self.isClosed):
                yEq.values[i][0] = 3 * (self.__points[min(i+1, self.size-1)] - self.__points[max(i-1, 0)])
            else:
                yEq.values[i][0] = 3 * (self.__points[(i+1) % self.size] - self.__points[(i-1) % self.size])
        #Menghitung isi dari matriks D
        #Matriks ini merupakan hasil perkalian dari
        #(invers matrix tridiagonal NxN)*(matriks Y)
        self.__dMat = TridiagonalMatrix(self.size, self.isClosed).inverse() * yEq

    """
    Gunakan method ini untuk menciptakan ulang spline
    """
    def updatePoints(self, points:list, closed: bool = False):
        self.isClosed = closed
        self.__points = points
        self.size = len(points)
        self.__dMat = Matrix(1, self.size)
        self.__recalculate__()

    """
    Mengambil sampel titik pada spline
    ini adalah fungsi Yi(t) pada spline
    """
    def getPoint(self, position: float):
        assert(position >= 0 and position <= self.size), 'posisi diluar batasan'
        y = self.__points
        D = self.__dMat.getCol(0)
        i = math.floor(position)
        i %= self.size
        t = (position % self.size) - i
        ai = y[i]
        bi = D[i]
        ci = 3*(y[(i+1)%self.size] - y[i]) - 2 * D[i] - D[(i+1)%self.size]
        di = 2*(y[i]-y[(i+1)%self.size]) + D[i] + D[(i+1)%self.size]

        return ai + bi * t + ci * (t**2) + di * (t**3)