
class Cars():


    def __init__(self, color, index, x, y):
        self.cor_x = []
        self.cor_y = []
        self.color = color
        self.index = index
        self.cor_x.append(x)
        self.cor_y.append(y)



c = []
car1 = Cars(0, 0, 0, 1)

c.append(car1)
car2 = Cars(1, 1, 1, 2)

c.append(car2)
for car in c:
    print car.color, car.cor_x, car.cor_y, car.index
    if car.index == 1:
        car.cor_x.append(2)
        car.cor_y.append(3)
for car in c:
    print car.color, car.cor_x, car.cor_y, car.index
