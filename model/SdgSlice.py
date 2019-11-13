import math
import xml.etree.cElementTree as ElementTree

from model.Point import Point


class SdgSlice:

    @property
    def svg_element(self):
        return self._svg_element

    @property
    def svg_path(self):
        return self._svg_path

    @property
    def color(self):
        return self._color

    def __init__(self, index, percentage, background):
        self._slice_angles = [-0.831598055, -0.46199892, -0.092399784, 0.277199352, 0.646798488, 1.016397623,
                              1.385996759, 1.755595895, 2.12519503, 2.494794166, 2.864393302, 3.233992438, 3.603591573,
                              3.973190709, 4.342789845, 4.71238898, 5.081988116]
        self._colors = ['F1F1F1', 'E5243B', 'DDA63A', '4C9F38', 'C5192D', 'FF3A21', '26BDE2', 'FCC30B', 'A21942',
                        'FD6925',
                        'DD1367', 'FD9D24', 'BF8B2E', '3F7E44', '0A97D9', '56C02B', '00689D', '19486A']

        self._inner_radius = 130
        self._max_slice_radius = 120
        self._slice_offset = 40
        self._angle = 2 / 17 * math.pi
        if background:
            self._color = self._colors[0]
        else:
            self._color = self._colors[index]
        self._slice_radius = self._max_slice_radius * percentage
        self._outer_radius = self._inner_radius + self._slice_radius
        self._point_one = Point(self._inner_radius, 0)
        self._point_two = Point(self._outer_radius, 0)
        self._point_three = Point(self._outer_radius * math.cos(self._angle),
                                  self._outer_radius * math.sin(self._angle))
        self._point_four = Point(self._inner_radius * math.cos(self._angle), self._inner_radius * math.sin(self._angle))
        self.polar_shift(self._angle / 2, self._slice_offset)
        self._position_angle = index * self._angle + 3 / 2 + math.pi
        self.rotate(self._position_angle)
        self.cartesian_shift(297.64, 297.64)
        self._svg_path = self.generate_svg_path()
        self._svg_element = self.generate_svg_element("black", 1)

    def generate_svg_path(self):
        movement_string = 'M ' + self._point_one.to_string()
        first_line = 'L ' + self._point_two.to_string()
        outer_circle = 'A ' + str(self._outer_radius + self._slice_offset) + ', ' + str(
            self._outer_radius + self._slice_offset) + ' 0 0,1 ' + self._point_three.to_string()
        second_line = 'L ' + self._point_four.to_string()
        inner_circle = 'A ' + str(self._inner_radius + self._slice_offset) + ', ' + str(
            self._inner_radius + self._slice_offset) + ' 0 0,0 ' + self._point_one.to_string()
        return movement_string + ' ' + first_line + ' ' + outer_circle + ' ' + second_line + ' ' + inner_circle

    def generate_svg_element(self,stroke, stroke_width):
        path = ElementTree.Element("path")
        path.set("d", self._svg_path)
        path.set("fill", self._color)
        path.set("stroke", stroke)
        path.set("stroke-width", stroke_width)
        return '<path d="' + self._svg_path + 'fill=#"' + self._color + 'stroke="black" stroke-width="1"'

    def rotate(self, angle):
        self._point_one.rotate(angle)
        self._point_two.rotate(angle)
        self._point_three.rotate(angle)
        self._point_four.rotate(angle)

    def polar_shift(self, angle, amount):
        self._point_one.polar_shift(angle, amount)
        self._point_two.polar_shift(angle, amount)
        self._point_three.polar_shift(angle, amount)
        self._point_four.polar_shift(angle, amount)

    def cartesian_shift(self, delta_x, delta_y):
        self._point_one.cartesian_shift(delta_x, delta_y)
        self._point_two.cartesian_shift(delta_x, delta_y)
        self._point_three.cartesian_shift(delta_x, delta_y)
        self._point_four.cartesian_shift(delta_x, delta_y)
