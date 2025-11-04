class Point :
    def __init__(        # конструктор: спец. метод __init__
            self,        # посилання на об'єкт явно передається 
            x=0.0,       # першим параметром методів
            y=0.0):      # Відсутність перевантаження не дозволяє робити 
        self.x = x       # кількох конструкторів, для варіативності 
        self.y = y       # вживаються параметри за замовчанням

    def __str__(self):
        return "Point(%f, %f)" % (self.x, self.y)

    def __repr__(self):
        return "(%f, %f)" % (self.x, self.y)
    
    def magnitude(self) -> float :
        return (self.x ** 2 + self.y ** 2) ** (0.5)
    
    def __add__(self, other) :    # спец. метод, який задає оператор "+"
        if isinstance(other, Point) :
            return Point(other.x + self.x, other.y + self.y)
        else :
            raise TypeError("Point addition requires other Point")
        
    def __mul__(self, other) :
        '''Множення на число - дає нову точку. 
        Множення на точку сприймається як скалярне множення і дає число'''
        if isinstance(other, (int, float)) :
            return Point(self.x * other, self.y * other)
        elif isinstance(other, Point) :
            return self.x * other.x + self.y * other.y
        else :
            raise TypeError("Point multiplication requires other Point or number")



def main():
    p1 = Point(1,2)
    p2 = Point(3,4)
    Point.x = 10            # !! під час роботи можна змінювати не лише об'єкти, а й типи
    print(str(p1))
    print(p2.magnitude())   # при виклику методів self передається неявно, зазначати не треба
    print(p1 + p2)
    print(p1 * p2)
    print(p1 * 2)
    # print(p1 * 2j)   # TypeError: Point multiplication requires other Point or number


if __name__ == '__main__':
    main()


'''
Д.З. Реалізувати клас для роботи з дробами 
чисельник - ціле число
знаменник - ціле число, не ноль
Створити 
 - конструктор, який контролює валідність даних
 - рядкове представлення дробу
 - метод скорочення (4/6 -> 2/3)
 - математичні операції також з контролем як типів, так і даних
    після операцій здійснювати скорочення результату
 - методи числового представлення (як float)
 * метод створення з float представлення
'''