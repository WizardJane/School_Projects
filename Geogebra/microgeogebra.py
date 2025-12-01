import math
import pygame
from copy import *
pygame.init()

size_x = 1201
size_y = 751
size = (size_x, size_y)
screen = pygame.display.set_mode(size)


red = (255, 0, 0)
grey = (0, 255, 0)
white = (255, 255, 255)
green = (50, 205, 50)
violet = (138, 43, 226)
black = (0, 0, 0)
lime = (0, 255, 0)
blue = (0, 255, 255)
green_yellow = (173, 255, 47)
pink = (255, 20, 147)
orange = (255, 127, 80)
dark_red = (220, 20, 60)
lavander = (230, 230, 250)
shift_color = dark_red
common_color = lavander
start_button_colors = [common_color] * 11
button_colors = [common_color] * 11
screen.fill(white)
mouse_download = pygame.image.load('/Users/kate/Desktop/Code/Школа/Geogebra/mouse.png').convert_alpha()
save_download = pygame.image.load('/Users/kate/Desktop/Code/Школа/Geogebra/save.png').convert_alpha()
save_pic = pygame.transform.scale(save_download, (50, 50))
download_download = pygame.image.load('/Users/kate/Desktop/Code/Школа/Geogebra/download.png').convert_alpha()
download_pic = pygame.transform.scale(download_download, (50, 50))
clean_download = pygame.image.load('/Users/kate/Desktop/Code/Школа/Geogebra/clean.png').convert_alpha()
clean_pic = pygame.transform.scale(clean_download, (50, 50))

class Point:
    def __init__(self, x, y=None, polar=False):
        if isinstance(x, Point):
            self.x = x.x
            self.y = x.y
        else:
            if polar:
                self.x = math.cos(y) * x
                self.y = math.sin(y) * x
            else:
                self.x = x
                self.y = y
    

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __str__(self):
        return str(self.x) + " " + str(self.y)

    def dist(self, p=None, q=None):
        if (type(p) == float or type(p) == int) and (type(q) == float or type(q) == int):
            other = Point(p, q)
        elif p is None:
            other = Point(0, 0)
        else:
            other = p
        a = self.x - other.x
        b = self.y - other.y
        return math.hypot(a, b)

    def angle(self):
        if self.dist() == 0: 
            return 0
        n = math.acos(self.x / self.dist())
        if self.y >= 0:
            return n
        else:
            return (math.pi * 2 - n)

    
    def angle_between(self, other):
        n = abs(self.angle() - other.angle())
        return min(n, math.pi * 2 - n)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False
               

class Vector(Point):
    def __init__(self, x1, y1=None, x2=None, y2=None):
        if isinstance(x1, Point) and isinstance(y1, Point):
            super().__init__(y1.x - x1.x, y1.y - x1.y)
            self = Point(y1.x - x1.x, y1.y - x1.y)
        elif type(x1) == Vector or type(x1) == Point:
            super().__init__(x1)
            self = x1
        elif x2 is None and y2 is None:
            super().__init__(x1, y1)
            self = Point(x1, y1)
        else:
            super().__init__(x2 - x1, y2 - y1)
            self = Point(x2 - x1, y2 - y1)


        
    def __str__(self):
        return str(self.x) + " " + str(self.y)
        

    def dot_product(self, other):
        return (self.x * other.x + self.y * other.y)


    def __mul__(self, other):
        if type(other) == Point or type(other) == Vector:
            return (self.x * other.x + self.y * other.y)
        else:
            return Point(self.x + self.x * other, self.y + self.y * other)


    def cross_product(self, other):
        return (self.x * other.y - self.y * other.x)


    def __xor__(self, other):
        return (self.x * other.y - self.y * other.x)


    def mul(self, n):
        return Point(self.x * n, self.y * n)
    
    def __rmul__(self, n):
        self = Point(self.x * n, self.y * n)
        return self

    def square(self, other):
        return 0.5 * self.dist() * other.dist() * math.sin(self.angle_between(other))

    def if_collinear(self, other):
        n = self * other 
        e = 1e-7
        m = self.dist() * other.dist()
        if m == 0:
            return True
        if abs(n - m) < e:
            return True
        return False

    def if_on_ray(self, a):
        e = 1e-7
        if self.square(a) < e and ((a.x >= 0 and self.x >= 0) or (a.x <= 0 and self.x <= 0)) and ((a.y >= 0 and self.y >= 0) or (a.y <= 0 and self.y <= 0)):
            return True
        else:
            return False

    def if_on_distant(self, a):
        e = 1e-7
        if self.square(a) < e and min(self.x, 0) <= a.x <= max(self.x, 0) and min(0, self.y) <= a.y <= max(0, self.y):
            return True
        else:
            return False

    def if_in_angle(self, b, p):
        b_ang = b.angle()
        p_ang = p.angle()
        a_ang = self.angle()
        if self.if_on_ray(b) or self.if_on_ray(p):
            return True
        if p_ang < b_ang:
            b_ang, p_ang = p_ang, b_ang
            b, p = p, b
        if abs(b_ang - p_ang) > math.pi:
            if 0 <= a_ang <= b_ang or p_ang <= a_ang <= 2 * math.pi:
                return True
        else:
            if b_ang <= a_ang <= p_ang:
                return True
        return False


class Line():
    
    def __init__(self, x1, y1, x2=None, y2=None, d=None):
        if isinstance(x1, Point) and isinstance(y1, Point):
            self.a = y1.y - x1.y
            self.b = x1.x - y1.x
            self.c = -self.a * x1.x - self.b * x1.y
        elif d is None and y2 is None:
            self.a = x1
            self.b = y1
            self.c = x2
        
        else:
            self.a = x1
            self.b = y1
            self.c = x2

    def __str__(self):
        return f'{self.a} {self.b} {self.c}'


    def perp_line(self, p):
        if self.b == 0:
            return Line(0, 1, -p.y)
        elif self.a == 0:
            return Line(1, 0, -p.x)
        else:
            return Line(self.b, -self.a, -p.x * self.b + p.y * self.a)
    
    def contains(self, p):
        e = 1e-5
        if abs(p.x * self.a + p.y * self.b + self.c) < e:
            return True
        return False

    def find(self, x):
        if self.b == 0:
            return 0
        return -(self.c + self.a * x) / self.b

    def check_one_side(self, a, b):
        if self.b == 0:
            x = -self.c / self.a
            da = x - a.x
            db = x - b.x
        else:
            da = self.find(a.x) - a.y
            db = self.find(b.x) - b.y
        if (da < 0 and db < 0) or (da > 0 and db > 0):
            return True
        return False

    def is_parallel(self, other):
        if (self.a * other.b) == (self.b * other.a):
            return True
        return False

    def is_perpendicular(self, other):
        if self.a * other.a == - self.b * other.b:
            return True
        return False

    def eq(self, other):
        if self.a * other.b == self.b * other.a and self.b * other.c == self.c * other.b and self.a * other.c == self.c * other.a:
            return True
        return False

    def dist(self, p):
        if self.b == 0:
            x = -self.c / self.a
            return abs(p.x - x)
        else:
            a = Point(0, self.find(0))
            b = Point(1, self.find(1))
            oa = Vector(p, a)
            ob = Vector(p, b)
            return 2 * oa.square(ob) / a.dist(b)

    def parallel(self, d):
        if d == 0:
            return self
        if self.b == 0:
            return Line(self.a, self.b, self.c + self.a * d)
        else:
            old_c = 1
            other = Line(self.a, self.b, self.c - 1)
            old_d = abs(self.dist(Point(0, other.find(0))))
            new_c = round(old_c * d / old_d, 5)
            return Line(self.a, self.b, self.c + new_c)
            

    def cross(self, other):
        x = (self.b * other.c - self.c * other.b) / (self.a * other.b - self.b * other.a)
        if other.b == 0:
            y = self.find(x)
        else:
            y = other.find(x)
        return Point(x, y)

    def foot_of_perp(self, a):
        h = self.dist(a)
        help_line = self.parallel(h)
        perp = help_line.perp_line(a)
        return self.cross(perp)


    def dist_on_line(self, dot, d, direction=1):
        if self.b == 0:
            if direction == 1:
                return Point(dot.x, dot.y + d)
            else:
                return Point(dot.x, dot.y - d)
        k = -self.a / self.b
        ab = math.sqrt(d * d / (k * k + 1))
        bc = ab * k
        if direction == 1:
            return Point(dot.x + ab, dot.y + bc)
        else:
            return Point(dot.x - ab, dot.y - bc)



class Triangle:
    def __init__(self, pa, pb, pc):
        self.a = pa
        self.b = pb
        self.c = pc
    

    def bisector(self, num): 
        #   исходя из факта, что биссектриса делит отрезок в отношении прилежащих сторон
        a = self.a
        b = self.b
        c = self.c
        if num == 2:
            a, b = b, a
        elif num == 3:
            a, c = c, a

        bc = Vector(b, c)
        ab_d = a.dist(b)
        ac_d = a.dist(c)
        bc *= (ab_d / (ac_d + ab_d)) - 1
        p_k = Point(bc.x + b.x, bc.y + b.y)
        return Line(a, p_k)


    def point_of_medians(self):
        #   исходя из факта, что медиана соединяет вершину и середину стороны
        bc = Vector(self.b, self.c)
        ac = Vector(self.a, self.c)
        pm_bc = bc.mul(0.5)
        pm_ac = ac.mul(0.5)
        median1 = Line(self.a, Point(pm_bc.x + self.b.x, pm_bc.y + self.b.y))
        median2 = Line(self.b, Point(pm_ac.x + self.a.x, pm_ac.y + self.a.y))
        return Point(median1.cross(median2))

    def height(self, num):
        #   высота на сторону из точки - высота на прямую через точки стороны из точки
        a = self.a
        b = self.b
        c = self.c
        if num == 2:
            a, b = b, a
        elif num == 3:
            a, c = c, a
        
        bc = Line(b, c)
        p_of_h = bc.foot_of_perp(a)
        return Line(a, p_of_h)

    def m_perp(self, num):
        a = self.a
        b = self.b
        c = self.c
        if num == 2:
            a, b = b, a
        elif num == 3:
            a, c = c, a
    
        bc = Vector(b, c)
        pm_bc = bc.mul(0.5)
        bc_line = Line(b, c)
        perp = bc_line.perp_line(Point(pm_bc.x + b.x, pm_bc.y + b.y))
        return perp


    def bisector_center_radius(self):
        #   центр вписанной окружности - точка пересечения биссектрис треугольника, ее радиус - высота из центра на сторону
        p1 = self.bisector(1)
        p2 = self.bisector(2)
        center = p1.cross(p2)
        line = Line(self.a, self.b)
        return line.dist(center)

    def perp_center(self):
        p1 = self.m_perp(1)
        p2 = self.m_perp(2)
        center = p1.cross(p2)
        return center

    def perp_center_radius(self):
        #   центр описанной окружности - точка пересечения серединных перпендикуляров треугольника, радиус - расстояние от центра до вершины
        p1 = self.m_perp(1)
        p2 = self.m_perp(2)
        center = p1.cross(p2)
        return center.dist(self.a)
    
    def bisector_center(self):
        p1 = self.bisector(1)
        p2 = self.bisector(2)
        center = p1.cross(p2)
        return center

    
    def is_in_triangle(self, point):
        #  если точка лежит внутри двух углов треугольника, то она лежит внутри треугольника
        v_ab = Vector(self.a, self.b)
        v_ac = Vector(self.a, self.c)
        v_bc = Vector(self.b, self.c)
        v_ba = Vector(self.b, self.a)
        v_ap = Vector(self.a, point)
        v_bp = Vector(self.b, point)
        if v_ap.if_in_angle(v_ab, v_ac) and v_bp.if_in_angle(v_ba, v_bc):
            return True
        return False



class Circle:
    def __init__(self, center, r, x=None):
        if x is None:
            self.center = center
            self.r = r
        else:
            self.center = Point(center, r)
            self.r = x

    def dist_line(self, line):
        return max(0, line.dist(self.center) - self.r)

    def dist_point(self, p):
        return abs(p.dist(self.center) - self.r)

    def dist_center_to_line(self, line):
        return line.dist(self.center)
    
    def is_on_circle(self, p):
        e = 1e-7
        a = p.x - self.center.x
        b = p.y - self.center.y
        if abs(a * a + b * b - self.r * self.r) < e:
            return True
        return False

    
    def __eq__(self, other):
        if self.center == other.center and self.r == other.r:
            return True
        return False


    def is_in_circle(self, p):
        e = 1e-7
        if p.dist(self.center) < self.r:
            return True
        return False


    def crosses(self, line):
        e = 1e-7
        x = self.dist_center_to_line(line)
        if abs(x - self.r) < e:
            return [line.foot_of_perp(self.center)]
        elif x - self.r < e:
            h = line.dist(self.center)
            distance = math.sqrt(self.r * self.r - x * x)
            dot = line.foot_of_perp(self.center)
            p1 = line.dist_on_line(dot, distance, 1)
            p2 = line.dist_on_line(dot, distance, -1)
            return [p1, p2]
        else:
            return []

    def angle_between_tangents(self, dot):
        d = dot.dist(self.center)
        return math.asin(self.r / d) * 2

    def turn_dot_by_circle(self, angle):
        dy = math.sin(angle) * self.r
        dx = math.cos(angle) * self.r
        return Point(dx, dy)

    def crosses_of_circles(self, other):
        e = 1e-7
        x = self.center.dist(other.center)
        if self == other:
            return []
        elif abs(x - (self.r + other.r)) < e or abs(x - abs((self.r - other.r))) < e:
            line = Line(self.center, other.center)
            p1 = self.crosses(line)
            p2 = other.crosses(line)
            if p1[0] == p2[0] or p1[0] == p2[1]:
                p = p1[0]
            else:
                p = p2[0]
            return [p]
        elif x > self.r + other.r or x < abs(self.r - other.r):
            return []
        else:
            a1, b1, r1 = self.center.x, self.center.y, self.r
            a2, b2, r2 = other.center.x, other.center.y, other.r
            line = Line(-2 * (a1 - a2), -2 * (b1 - b2), -r1 * r1 + a1 * a1 + b1 * b1 + r2 * r2 - a2 * a2 - b2 * b2)
            points = other.crosses(line)
            return points


        
class Draw_point(Point):
    def __init__(self, x, y=None):
        super().__init__(x, y)
    

    def draw(self):
        pygame.draw.circle(screen, black, (self.x, self.y), 3)

    def highlight(self):
        pygame.draw.circle(screen, grey, (self.x, self.y), 3)
        pygame.draw.circle(screen, black, (self.x, self.y), 1)


class Draw_vector(Vector):
    def __init__(self, points):
        a, b = points[0], points[1]
        self.start = a
        super().__init__(a, b)

    def draw(self):
        pygame.draw.line(screen, black, (self.start.x, self.start.y), (self.start.x + self.x, self.start.y + self.y), 1)

    def highlight(self):
        pygame.draw.line(screen, grey, (self.start.x, self.start.y), (self.start.x + self.x, self.start.y + self.y), 3)
        pygame.draw.line(screen, black, (self.start.x, self.start.y), (self.start.x + self.x, self.start.y + self.y), 1)

    def dist_for_vector(self, p):
        x1, y1 = p.x, p.y
        x2, y2 = self.start.x, self.start.y
        x3, y3 = self.start.x + self.x, self.start.y + self.y
        v21 = Vector(x2, y2, x1, y1)
        v31 = Vector(x3, y3, x1, y1)
        v12 = Vector(x1, y1, x2, y2)
        v13 = Vector(x1, y1, x3, y3)
        ray23 = Vector(x2, y2, x3, y3)
        ray32 = Vector(x3, y3, x2, y2)
        if v21.if_on_distant(ray23) or v31.if_on_distant(ray32):
            return 0
        else:
            main_ans = 2 * v12.square(v13) / ray23.dist()
            ans1 = v13.dist()
            ans2 = v12.dist()
            ang_cos1 = (v21 * ray23) / (ray23.dist() * v21.dist())
            ang_cos2 = (v31 * ray32) / (ray32.dist() * v31.dist())
            if ang_cos1 < 0 or ang_cos2 < 0:
                return round(min(ans1, ans2), 7)
            else:
                return round(main_ans, 7)


class Draw_line(Line):
    def __init__(self, points):
        super().__init__(points[0], points[1])
        if self.b == 0:
            self.main_point1, self.main_point2 =  Point(-self.c / self.a, 0), Point(-self.c / self.a, size_y)
        elif self.a == 0:
            self.main_point1, self.main_point2 = Point(0, -self.c / self.b), Point(size_x, -self.c / self.b)
        else:
            y0 = Point(0, self.find(0))
            y_max = Point(size_x, self.find(size_x))
            x_max = Point((-self.c - self.b * size_y) / self.a, size_y)
            x0 = Point(-self.c / self.a, 0)
            if self.is_in_window(x0) and self.is_in_window(y0):
                self.main_point1, self.main_point2 = Point(x0.x, x0.y), Point(y0.x, y0.y)
            elif self.is_in_window(x0) and self.is_in_window(y_max):
                self.main_point1, self.main_point2 = Point(x0.x, x0.y), Point(y_max.x, y_max.y)
            elif self.is_in_window(x0) and self.is_in_window(x_max):
                self.main_point1, self.main_point2 = Point(x0.x, x0.y), Point(x_max.x, x_max.y)
            elif self.is_in_window(y0) and self.is_in_window(y_max):
                self.main_point1, self.main_point2 = Point(y0.x, y0.y), Point(y_max.x, y_max.y)
            elif self.is_in_window(y0) and self.is_in_window(x_max):
                self.main_point1, self.main_point2 = Point(y0.x, y0.y), Point(x_max.x, x_max.y)
            elif self.is_in_window(x_max) and self.is_in_window(y_max):
                self.main_point1, self.main_point2 = Point(x_max.x, x_max.y), Point(y_max.x, y_max.y)

    def draw(self):
        pygame.draw.line(screen, black, (self.main_point1.x, self.main_point1.y), (self.main_point2.x, self.main_point2.y), 1)


    def highlight(self):
        pygame.draw.line(screen, grey, (self.main_point1.x, self.main_point1.y), (self.main_point2.x, self.main_point2.y), 2)
        pygame.draw.line(screen, black, (self.main_point1.x, self.main_point1.y), (self.main_point2.x, self.main_point2.y), 1)


    def is_in_window(self, p):
        if p.x >= 0 and p.x <= size_x and p.y >= 0 and p.y <= size_y:
            return True
        return False

    def contains(self, p):
        e = 1e-5
        if abs(p.x * self.a + p.y * self.b + self.c) < 20:
            return True
        return False
    

class Draw_circle2(Circle):
    def __init__(self, points):
        c = Point(points[0])
        r = c.dist(points[1])
        super().__init__(c, r)

    def draw(self):
        pygame.draw.circle(screen, black, (self.center.x, self.center.y), self.r, 1)
    
    def highlight(self):
        pygame.draw.circle(screen, grey, (self.center.x, self.center.y), self.r, 3)
        pygame.draw.circle(screen, black, (self.center.x, self.center.y), self.r, 1)


class Draw_circle3(Circle):
    def __init__(self, points):
        t = Triangle(points[0], points[1], points[2])
        c = t.perp_center()
        r = t.perp_center_radius()
        super().__init__(c, r)
    
    def draw(self):
        pygame.draw.circle(screen, black, (self.center.x, self.center.y), self.r, 1)
    
    def highlight(self):
        pygame.draw.circle(screen, grey, (self.center.x, self.center.y), self.r, 3)
        pygame.draw.circle(screen, black, (self.center.x, self.center.y), self.r, 1)     


class Draw_triangle(Triangle):
    def __init__(self, points):
        super().__init__(points[0], points[1], points[2])

    def draw(self):
        pygame.draw.line(screen, black, (self.a.x, self.a.y), (self.b.x, self.b.y), 1)
        pygame.draw.line(screen, black, (self.a.x, self.a.y), (self.c.x, self.c.y), 1)
        pygame.draw.line(screen, black, (self.b.x, self.b.y), (self.c.x, self.c.y), 1)

    def highlight(self):
        pygame.draw.line(screen, grey, (self.a.x, self.a.y), (self.b.x, self.b.y), 2)
        pygame.draw.line(screen, grey, (self.a.x, self.a.y), (self.c.x, self.c.y), 2)
        pygame.draw.line(screen, grey, (self.b.x, self.b.y), (self.c.x, self.c.y), 2)
        self.draw()

    def dist_point(self, p):
        av = Draw_vector([self.b, self.c])
        bv = Draw_vector([self.a, self.c])
        cv = Draw_vector([self.a, self.b])
        return min(av.dist_for_vector(p), bv.dist_for_vector(p), cv.dist_for_vector(p))



def clean_points():
    global current_points
    global count_points
    count_points = 0
    current_points = []


def draw_utilits():
    global button_colors
    global instruction
    global important_words
    pygame.draw.rect(screen, button_colors[0], (0, 0, 49, 49), 0) # mouse
    pygame.draw.rect(screen, button_colors[1], (50, 0, 49, 49), 0) # point
    pygame.draw.rect(screen, button_colors[2], (100, 0, 49, 49), 0) # vector
    pygame.draw.rect(screen, button_colors[3], (150, 0, 49, 49), 0) # line
    pygame.draw.rect(screen, button_colors[4], (200, 0, 49, 49), 0) # circle2
    pygame.draw.rect(screen, button_colors[5], (250, 0, 49, 49), 0) # circle3
    pygame.draw.rect(screen, button_colors[6], (300, 0, 49, 49), 0) # triangle
    pygame.draw.rect(screen, button_colors[7], (350, 0, 49, 49), 0) # intersect
    pygame.draw.rect(screen, button_colors[8], (400, 0, 49, 49), 0) # save
    pygame.draw.rect(screen, button_colors[9], (450, 0, 49, 49), 0) # download
    pygame.draw.rect(screen, button_colors[10], (500, 0, 49, 49), 0) # delete
    screen.blit(mouse_download, (12, 3)) # mouse
    pygame.draw.circle(screen, black, (75, 25), 2) # point
    pygame.draw.line(screen, black, (110, 25), (140, 25), 1) # vector
    pygame.draw.circle(screen, black, (110, 25), 3) # vector
    pygame.draw.circle(screen, black, (140, 25), 3) # vector
    pygame.draw.line(screen, black, (150, 25), (198, 25), 1) # line
    pygame.draw.circle(screen, black, (225, 25), 10, 1) # circle2
    pygame.draw.circle(screen, black, (225, 25), 2) # circle2
    pygame.draw.circle(screen, black, (235, 25), 2) # circle2
    pygame.draw.circle(screen, black, (275, 25), 10, 1) # circle3
    pygame.draw.circle(screen, black, (285, 25), 2) # circle3
    pygame.draw.circle(screen, black, (265, 25), 2) # circle3
    pygame.draw.circle(screen, black, (275, 15), 2) # circle3
    pygame.draw.polygon(screen, black, [(325, 10), (315, 30), (335, 30)], 0) # triangle
    pygame.draw.line(screen, black, (350, 0), (398, 48), 1) # intersect
    pygame.draw.line(screen, black, (350, 48), (398, 0), 1) # intersect
    pygame.draw.circle(screen, black, (374, 24), 2) # intersect
    screen.blit(save_pic, (400, 0)) # save
    screen.blit(download_pic, (450, 0)) # download
    screen.blit(clean_pic, (500, 0)) # clean

    if instruction:
        my_font = pygame.font.SysFont('serif', 20)
        for i in range(0, len(important_words)):
            text_now = my_font.render(important_words[i], True, black)
            screen.blit(text_now, (50, 75 + i * 20))

    

def clean_screen():
    global objects
    screen.fill(white)
    global current_points
    global objects_type
    global all_points
    global intersections
    intersect()
    for i in range(len(objects)):
        t = objects_type[i]
        objects[i] = t(all_points[i])
        objects[i].draw()
        if highlighted_check[i]:
            objects[i].highlight()
    for i in range(len(intersections)):
        intersections[i].draw()

    for i in range(len(current_points)):
        p = current_points[i]
        pygame.draw.circle(screen, black, (p.x, p.y), 1) # current_point
    draw_utilits()
        

def has_point(obj, a):
    global obj_mode
    is_close = 10
    if isinstance(obj, Draw_point) and obj.dist(a) < is_close:
        obj_mode = "point"
        return True
    elif isinstance(obj, Draw_vector) and obj.dist_for_vector(a) < is_close:
        obj_mode = "vector"
        return True
    elif isinstance(obj, Draw_line) and obj.dist(a) < is_close:
        obj_mode = "line"
        return True
    elif isinstance(obj, Draw_circle2) and obj.dist_point(a) < is_close:
        obj_mode = "circle2"
        return True
    elif isinstance(obj, Draw_circle3) and obj.dist_point(a) < is_close:
        obj_mode = "circle3"
        return True
    elif isinstance(obj, Draw_triangle) and obj.dist_point(a) < is_close:
        obj_mode = "triangle"
        return True
    obj_mode = None
    return False
    

def find_object(x, y):
    global objects
    global obj_mode
    i = 0
    while True and i < len(objects):
        obj = objects[i]
        if has_point(obj, Draw_point(x, y)):
            return i
        i += 1
    return None


def move(now, prev):
    global objects
    global obj_mode
    global important_point
    global all_points
    dx = now[0] - prev[0]
    dy = now[1] - prev[1]
    i = 0
    for i in range(len(objects)):
        if highlighted_check[i]:
            obj = objects[i]
            if isinstance(obj, Draw_point):
                all_points[i].x += dx
                all_points[i].y += dy
            else:
                is_important = False
                for j in range(len(all_points[i])):
                    if important_point == all_points[i][j]:
                        all_points[i][j].x += dx
                        all_points[i][j].y += dy
                        is_important = True
                if not is_important:
                    for j in range(len(all_points[i])):
                        all_points[i][j].x += dx
                        all_points[i][j].y += dy


def highlight_smth():
    radius_s = 5
    global current_points
    global obj_mode
    global objects
    global highlighted_check
    global count_highlighted
    global important_point
    #global highlighted_points
    x = current_points[0].x 
    y = current_points[0].y
    obj_index = None
    f = False
    for i in range(x - radius_s, x + radius_s):
        for j in range(y - radius_s, y + radius_s):
            color = screen.get_at((i, j))
            if color == black:
                obj_index = find_object(i, j)
                if isinstance(objects[obj_index], Draw_point):
                    important_point = Point(x, y)
    if obj_index is not None:
        if highlighted_check[obj_index]:
            highlighted_check[obj_index] = False
            count_highlighted -= 1
            #if isinstance(objects[obj_index], Draw_point):
                #highlighted_points.append(i)
        else:
            highlighted_check[obj_index] = True
            count_highlighted += 1
    else:
        highlighted_check = [False] * len(objects)
        #highlighted_points = []
        count_highlighted = 0
    
    
def intersect():
    global highlighted_check
    global objects
    global intersections
    global intersect_objects
    intersections = []
    for i in range(len(intersect_objects)):
        obj1 = objects[intersect_objects[i][0]]
        obj2 = objects[intersect_objects[i][1]]
        intersect_2_objects(obj1, obj2)
    

def intersect_2_objects(obj1, obj2):
    global highlighted_check
    global objects
    global intersections
    global intersect_objects
    points = []
    if isinstance(obj1, Circle) and isinstance(obj2, Draw_line): 
        points = obj1.crosses(obj2)
    elif isinstance(obj2, Circle) and isinstance(obj1, Draw_line): 
        points = obj2.crosses(obj1)
    elif isinstance(obj2, Draw_line) and isinstance(obj1, Draw_line): 
        points = [obj1.cross(obj2)]
    elif isinstance(obj2, Circle) and isinstance(obj1, Circle): 
        points = obj1.crosses_of_circles(obj2)
    elif isinstance(obj2, Draw_vector) and isinstance(obj1, Draw_line): 
        help = Line(Point(obj2.start.x, obj2.start.y), Point(obj2.start.x + obj2.x, obj2.start.y + obj2.y))
        p = help.cross(obj1)
        if obj2.if_on_distant(Vector(obj2.start, p)):
            points = [p]
    elif isinstance(obj2, Draw_line) and isinstance(obj1, Draw_vector): 
        help = Line(Point(obj1.start.x, obj1.start.y), Point(obj1.start.x + obj1.x, obj1.start.y + obj1.y))
        p = help.cross(obj2)
        if obj1.if_on_distant(Vector(obj1.start, p)):
            points = [p]
    elif isinstance(obj2, Draw_vector) and isinstance(obj1, Draw_vector): 
        help1 = Line(Point(obj1.start.x, obj1.start.y), Point(obj1.start.x + obj1.x, obj1.start.y + obj1.y))
        help2 = Line(Point(obj2.start.x, obj2.start.y), Point(obj2.start.x + obj2.x, obj2.start.y + obj2.y))
        p = help1.cross(help2)
        if obj1.if_on_distant(Vector(obj1.start, p)) and obj2.if_on_distant(Vector(obj2.start, p)):
            points = [p]
    elif isinstance(obj2, Circle) and isinstance(obj1, Draw_vector): 
        help = Line(Point(obj1.start.x, obj1.start.y), Point(obj1.start.x + obj1.x, obj1.start.y + obj1.y))
        p = obj2.crosses(help)
        for i in range(len(p)):
            if obj1.if_on_distant(Vector(obj1.start, p[i])):
                points.append(p[i])
    elif isinstance(obj2, Draw_vector) and isinstance(obj1, Circle): 
        help = Line(Point(obj2.start.x, obj2.start.y), Point(obj2.start.x + obj2.x, obj2.start.y + obj2.y))
        p = obj1.crosses(help)
        for i in range(len(p)):
            if obj2.if_on_distant(Vector(obj2.start, p[i])):
                points.append(p[i])
    elif isinstance(obj2, Circle) and isinstance(obj1, Draw_triangle): 
        v1, v2, v3 = Draw_vector([obj1.a, obj1.b]), Draw_vector([obj1.b, obj1.c]), Draw_vector([obj1.a, obj1.c])
        for v in [v1, v2, v3]:
            help = Line(Point(v.start.x, v.start.y), Point(v.start.x + v.x, v.start.y + v.y))
            p = obj2.crosses(help)
            for i in range(len(p)):
                if v.if_on_distant(Vector(v.start, p[i])):
                    points.append(p[i])
    elif isinstance(obj2, Draw_triangle) and isinstance(obj1, Circle): 
        v1, v2, v3 = Draw_vector([obj2.a, obj2.b]), Draw_vector([obj2.b, obj2.c]), Draw_vector([obj2.a, obj2.c])
        for v in [v1, v2, v3]:
            help = Line(Point(v.start.x, v.start.y), Point(v.start.x + v.x, v.start.y + v.y))
            p = obj1.crosses(help)
            for i in range(len(p)):
                if v.if_on_distant(Vector(v.start, p[i])):
                    points.append(p[i])
    elif isinstance(obj2, Draw_line) and isinstance(obj1, Draw_triangle): 
        v1, v2, v3 = Draw_vector([obj1.a, obj1.b]), Draw_vector([obj1.b, obj1.c]), Draw_vector([obj1.a, obj1.c])
        for v in [v1, v2, v3]:
            help = Line(Point(v.start.x, v.start.y), Point(v.start.x + v.x, v.start.y + v.y))
            p = obj2.cross(help)
            if v.if_on_distant(Vector(v.start, p)):
                points.append(p)
    elif isinstance(obj2, Draw_vector) and isinstance(obj1, Draw_triangle): 
        v1, v2, v3 = Draw_vector([obj1.a, obj1.b]), Draw_vector([obj1.b, obj1.c]), Draw_vector([obj1.a, obj1.c])
        help2 = Line(Point(obj2.start.x, obj2.start.y), Point(obj2.start.x + obj2.x, obj2.start.y + obj2.y))
        for v in [v1, v2, v3]:
            help1 = Line(Point(v.start.x, v.start.y), Point(v.start.x + v.x, v.start.y + v.y))
            p = help2.cross(help1)
            if v.if_on_distant(Vector(v.start, p)):
                points.append(p)
    elif isinstance(obj2, Draw_triangle) and isinstance(obj1, Draw_line): 
        v1, v2, v3 = Draw_vector([obj2.a, obj2.b]), Draw_vector([obj2.b, obj2.c]), Draw_vector([obj2.a, obj2.c])
        for v in [v1, v2, v3]:
            help = Line(Point(v.start.x, v.start.y), Point(v.start.x + v.x, v.start.y + v.y))
            p = obj1.cross(help)
            if v.if_on_distant(Vector(v.start, p)):
                points.append(p)
    elif isinstance(obj2, Draw_triangle) and isinstance(obj1, Draw_vector): 
        v1, v2, v3 = Draw_vector([obj2.a, obj2.b]), Draw_vector([obj2.b, obj2.c]), Draw_vector([obj2.a, obj2.c])
        help2 = Line(Point(obj1.start.x, obj1.start.y), Point(obj1.start.x + obj1.x, obj1.start.y + obj1.y))
        for v in [v1, v2, v3]:
            help1 = Line(Point(v.start.x, v.start.y), Point(v.start.x + v.x, v.start.y + v.y))
            p = help2.cross(help1)
            if v.if_on_distant(Vector(v.start, p)):
                points.append(p)
    elif isinstance(obj2, Draw_triangle) and isinstance(obj1, Draw_triangle):
        v1, v2, v3 = Draw_vector([obj2.a, obj2.b]), Draw_vector([obj2.b, obj2.c]), Draw_vector([obj2.a, obj2.c])
        v4, v5, v6 = Draw_vector([obj1.a, obj1.b]), Draw_vector([obj1.b, obj1.c]), Draw_vector([obj1.a, obj1.c])
        for vx in [v1, v2, v3]:
            for vy in [v4, v5, v6]:
                help1 = Line(Point(vx.start.x, vx.start.y), Point(vx.start.x + vx.x, vx.start.y + vx.y))
                help2 = Line(Point(vy.start.x, vy.start.y), Point(vy.start.x + vy.x, vy.start.y + vy.y))
                p = help1.cross(help2)
                if vx.if_on_distant(Vector(vx.start, p)) and vy.if_on_distant(Vector(vy.start, p)):
                    points.append(p)

    for i in range(len(points)):
        intersections.append(Draw_point(points[i]))


        #highlighted_check.append(False)
        #objects_type.append(Draw_point)
        #all_points.append(p)
        
    # crosses - line and circle


def download():
    global objects
    global all_points
    global intersect_objects
    global objects_type
    global highlighted_check
    global connected
    f = open('geogebra_save.txt', "r", encoding="UTF-8")
    k = list(f.read().split("\n"))
    c1 = int(k[0])
    second_part = False
    for i in range(1, c1 + 1):
        a = list(map(str, k[i].split()))
        if a[0] == "point":
            objects_type.append(Draw_point)
            objects.append(Draw_point(int(a[1]), int(a[2])))
            all_points.append(Draw_point(int(a[1]), int(a[2])))
        elif a[0] == "circle2":
            objects_type.append(Draw_circle2)
            listing = [Draw_point(int(a[1]), int(a[2])), Draw_point(int(a[3]), int(a[4]))]
            objects.append(Draw_circle2(listing))
            all_points.append(listing)
        elif a[0] == "circle3":
            objects_type.append(Draw_circle3)
            listing = [Draw_point(int(a[1]), int(a[2])), Draw_point(int(a[3]), int(a[4])), Draw_point(int(a[5]), int(a[6]))]
            objects.append(Draw_circle3(listing))
            all_points.append(listing)
        elif a[0] == "line":
            objects_type.append(Draw_line)
            listing = [Draw_point(int(a[1]), int(a[2])), Draw_point(int(a[3]), int(a[4]))]
            objects.append(Draw_line(listing))
            all_points.append(listing)
        elif a[0] == "vector":
            objects_type.append(Draw_vector)
            listing = [Draw_point(int(a[1]), int(a[2])), Draw_point(int(a[3]), int(a[4]))]
            objects.append(Draw_vector(listing))
            all_points.append(listing)
        elif a[0] == "triangle":
            objects_type.append(Draw_triangle)
            listing = [Draw_point(int(a[1]), int(a[2])), Draw_point(int(a[3]), int(a[4])), Draw_point(int(a[5]), int(a[6]))]
            objects.append(Draw_triangle(listing))
            all_points.append(listing)
    c2 = int(k[c1 + 1])
    for j in range(c1 + 2, c1 + 2 + c2):
        a = []
        a = list(map(str, k[j].split()))
        intersect_objects.append([int(a[0]), int(a[1])])
    highlighted_check = [False] * len(objects)
    c3 = int(k[c2 + c1 + 2])
    for m in range(c2 + c1 + 3, c1 + 3 + c2 + c3):
        a = []
        a = list(map(int, k[m].split()))
        if len(a) == 3:
            index = a[0]
            all_points[index] = [all_points[a[1]], all_points[a[2]]]
        elif len(a) == 4:
            index = a[0]
            all_points[index] = [all_points[a[1]], all_points[a[2]], all_points[a[3]]]
    f.close()


def save():
    global objects
    global all_points
    global intersect_objects
    global connected
    f = open('geogebra_save.txt', "w", encoding="UTF-8")
    f.write(str(len(objects)) + "\n")
    for i in range(len(objects)):
        obj = objects[i]
        if isinstance(obj, Draw_circle3):
            s = "circle3" + " " + str(all_points[i][0]) + " " + str(all_points[i][1]) + " " + str(all_points[i][2])
            f.write(s + "\n")
        elif isinstance(obj, Draw_circle2):
            s = "circle2" + " " + str(all_points[i][0]) + " " + str(all_points[i][1])
            f.write(s + "\n")
        elif isinstance(obj, Draw_line):
            s = "line" + " " + str(all_points[i][0]) + " " + str(all_points[i][1])
            f.write(s + "\n")
        elif isinstance(obj, Draw_point):
            s = "point" + " " + str(all_points[i])
            f.write(s + "\n")
        elif isinstance(obj, Draw_vector):
            s = "vector" + " " + str(all_points[i][0]) + " " + str(all_points[i][1])
            f.write(s + "\n")
        elif isinstance(obj, Draw_triangle):
            s = "triangle" + " " + str(all_points[i][0]) + " " + str(all_points[i][1]) + " " + str(all_points[i][2])
            f.write(s + "\n")
    f.write(str(len(intersect_objects)) + "\n")
    for i in range(len(intersect_objects)):
        s = str(intersect_objects[i][0]) + " " + str(intersect_objects[i][1])
        f.write(s + "\n")

    f.write(str(len(connected)) + "\n")
    
    for i in range(len(connected)):
        s = ""
        for j in range(len(connected[i])):
            s += str(connected[i][j]) 
            s += " "
        f.write(s + "\n")
    f.close()


def delete_all():
    global current_points
    global count_points
    global highlighted_check
    global count_highlighted
    global intersect_objects
    global objects_type
    global all_points
    global intersections
    global important_point
    global prev
    global moving
    global objects
    global highlighted_objects
    global connected 

    current_points = []
    count_points = 0
    objects = []
    highlighted_check = []
    count_highlighted = 0
    highlighted_objects = []
    intersect_objects = []
    objects_type = []
    all_points = []
    intersections = []
    important_point = Draw_point(0, 0)
    prev = [0, 0]
    moving = False
    connected = []

mode = "point"
modes = ["mouse", "circle2", "circle3", "line", "triangle", "vector", "point", "intersect"]
current_points = []
count_points = 0
objects = []
highlighted_check = []
count_highlighted = 0
highlighted_objects = []
intersect_objects = []
objects_type = []
all_points = []
intersections = []
important_point = Draw_point(0, 0)
prev = [0, 0]
moving = False
connected = [] # чтобы связать точки и объекты при проведении объекта через точки. Первый элемент - индекс объекта, остальное - индексы точек.
instruction = True
important_words = ["Инструкция:", "Чтобы нарисовать объект, нажмите его иконку и ткните нужное количество точек для построения объекта;", "Если вы хотите построить объект через выделенные точки, то выберете нужное количество точек и нажмите иконку объекта;", "Выбирать нужно СТРОГО нужное количество точек. Для прямой, отрезка - 2, для треугольника - 3 и т.д.;", "Чтобы выделить объект, нажмите на него;", "Чтобы снять выделение, ткните в свободное место;", "Выделенные объекты перетаскиваются мышкой;", "Чтобы построить пересечение, выделите ровно 2 объекта и нажмите кнопку пересечения;", "Все действия производятся левой кнопкой мыши;", "Точки пересечения не выделяются :( ждите обновления."]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEMOTION:
            if moving:
                now = event.pos
                move(now, prev)
                prev = now
        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            instruction = False
            moving = True
            position = event.pos
            prev = position
            x = position[0] 
            y = position[1]
            if 0 <= x <= 550 and 0 <= y <= 50:
                button_colors = start_button_colors[:]
                if 0 <= x <= 50:
                    mode = "mouse"
                    button_colors[0] = shift_color
                elif 50 < x <= 100:
                    mode = "point"
                    button_colors[1] = shift_color
                elif 100 < x <= 150:
                    mode = "vector"
                    button_colors[2] = shift_color
                    highlighted_points = 0
                    dop = [len(objects)]
                    if count_highlighted == 2:
                        for i in range(len(highlighted_check)):
                            if highlighted_check[i] and isinstance(objects[i], Draw_point):
                                highlighted_points += 1 
                                highlighted_objects.append(all_points[i])
                                dop.append(i)
                        if highlighted_points == 2:
                            object = Draw_vector(highlighted_objects)
                            objects.append(object)
                            highlighted_check.append(False)
                            objects_type.append(Draw_vector)
                            all_points.append(highlighted_objects)
                            connected.append(dop)
                        highlighted_objects = []
                    dop = []

                elif 150 < x <= 200:
                    mode = "line"
                    button_colors[3] = shift_color
                    highlighted_points = 0
                    dop = [len(objects)]
                    if count_highlighted == 2:
                        for i in range(len(highlighted_check)):
                            if highlighted_check[i] and isinstance(objects[i], Draw_point):
                                highlighted_points += 1 
                                highlighted_objects.append(all_points[i])
                                dop.append(i)
                        if highlighted_points == 2:
                            object = Draw_line(highlighted_objects)
                            objects.append(object)
                            highlighted_check.append(False)
                            objects_type.append(Draw_line)
                            all_points.append(highlighted_objects)
                            connected.append(dop)
                        highlighted_objects = []
                    dop = []
                elif 200 < x <= 250:
                    mode = "circle2"
                    button_colors[4] = shift_color
                    highlighted_points = 0
                    dop = [len(objects)]
                    if count_highlighted == 2:
                        for i in range(len(highlighted_check)):
                            if highlighted_check[i] and isinstance(objects[i], Draw_point):
                                highlighted_points += 1 
                                highlighted_objects.append(all_points[i])
                                dop.append(i)
                        if highlighted_points == 2:
                            object = Draw_circle2(highlighted_objects)
                            objects.append(object)
                            highlighted_check.append(False)
                            objects_type.append(Draw_circle2)
                            all_points.append(highlighted_objects)
                            connected.append(dop)
                        highlighted_objects = []
                    dop = []
                elif 250 < x <= 300:
                    mode = "circle3"
                    button_colors[5] = shift_color
                    highlighted_points = 0
                    dop = [len(objects)]
                    if count_highlighted == 3:
                        for i in range(len(highlighted_check)):
                            if highlighted_check[i] and isinstance(objects[i], Draw_point):
                                highlighted_points += 1 
                                highlighted_objects.append(all_points[i])
                                dop.append(i)
                        if highlighted_points == 3:
                            object = Draw_circle3(highlighted_objects)
                            objects.append(object)
                            highlighted_check.append(False)
                            objects_type.append(Draw_circle3)
                            all_points.append(highlighted_objects)
                            connected.append(dop)
                        highlighted_objects = []
                    dop = []
                elif 300 < x <= 350:
                    mode = "triangle"
                    button_colors[6] = shift_color
                    highlighted_points = 0
                    dop = [len(objects)]
                    if count_highlighted == 3:
                        for i in range(len(highlighted_check)):
                            if highlighted_check[i] and isinstance(objects[i], Draw_point):
                                highlighted_points += 1 
                                highlighted_objects.append(all_points[i])
                                dop.append(i)
                        if highlighted_points == 3:
                            object = Draw_triangle(highlighted_objects)
                            objects.append(object)
                            highlighted_check.append(False)
                            objects_type.append(Draw_triangle)
                            all_points.append(highlighted_objects)
                            connected.append(dop)
                        highlighted_objects = []
                    dop = []
                elif 350 < x <= 400:
                    if count_highlighted == 2:
                        highlighted_objects = []
                        for i in range(len(highlighted_check)):
                            if highlighted_check[i]:
                                highlighted_objects.append(i)
                        i_obj1 = highlighted_objects[0]
                        i_obj2 = highlighted_objects[1]
                        intersect_objects.append([i_obj1, i_obj2])
                        intersect()
                    button_colors[7] = shift_color
                elif 400 < x <= 450:
                    save()
                    button_colors[8] = shift_color
                elif 450 < x <= 500:
                    delete_all()
                    download()
                    button_colors[9] = shift_color
                elif 500 < x <= 550:
                    delete_all()
                    button_colors[10] = shift_color
                    
                clean_points()
            else:
                current_points.append(Point(x, y))
                count_points += 1

                if mode == "mouse" and count_points == 1:
                    highlight_smth()
                    clean_points()
                
                elif mode == "point" and count_points == 1:
                    object = Draw_point(current_points[0])
                    objects.append(object)
                    highlighted_check.append(False)
                    objects_type.append(Draw_point)
                    all_points.append(current_points[0])
                    clean_points()     

                elif mode == "circle2" and count_points == 2:
                    object = Draw_circle2(current_points)
                    objects.append(object)
                    highlighted_check.append(False)
                    objects_type.append(Draw_circle2)
                    all_points.append(current_points)
                    clean_points()

                elif mode == "circle3" and count_points == 3:
                    object = Draw_circle3(current_points)
                    objects.append(object)
                    highlighted_check.append(False)
                    objects_type.append(Draw_circle3)
                    all_points.append(current_points)
                    clean_points()

                elif mode == "triangle" and count_points == 3:
                    object = Draw_triangle(current_points)
                    objects_type.append(Draw_triangle)
                    all_points.append(current_points)
                    objects.append(object)
                    highlighted_check.append(False)
                    clean_points()

                elif mode == "line" and count_points == 2:
                    objects_type.append(Draw_line)
                    all_points.append(current_points)
                    object = Draw_line(current_points)
                    objects.append(object)
                    highlighted_check.append(False)
                    
                    clean_points()
                
                elif mode == "vector" and count_points == 2:
                    object = Draw_vector(current_points)
                    objects.append(object)
                    highlighted_check.append(False)
                    objects_type.append(Draw_vector)
                    all_points.append(current_points)
                    clean_points()

                

    clean_screen()
    pygame.display.update()