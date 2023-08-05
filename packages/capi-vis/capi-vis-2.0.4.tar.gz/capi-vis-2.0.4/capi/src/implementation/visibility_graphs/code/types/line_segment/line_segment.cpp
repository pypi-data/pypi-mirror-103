//
// Created by James.Balajan on 31/03/2021.
//

#include <stdexcept>

#include "constants/constants.hpp"
#include "line_segment.hpp"

Coordinate LineSegment::get_endpoint_1() const { return _endpoint_1; }

Coordinate LineSegment::get_endpoint_2() const { return _endpoint_2; }

Coordinate LineSegment::get_adjacent_to(const Coordinate &point) const {
    if (point == _endpoint_1) {
        return _endpoint_2;
    } else if (point == _endpoint_2) {
        return _endpoint_1;
    } else {
        throw std::runtime_error("Point queried in get_adjacent_to is not part of edge");
    }
}

std::optional<Coordinate> LineSegment::intersection_with_segment(const LineSegment &line_segment) const {
    /*
     * We use Cramer's rule to solve for scalars lambda_1 and lambda_2,
     * given the parametric representation of the line segment
     * x = lambda_1(a1 - b1) + b1 where lambda_1 goes from [0, 1] (a, b represent the segment endpoints)
     * and parametric representation of the ray
     * x = lambda_2*(a2 - b2) + b2 where lambda_2 goes from [0, 1]
     */

    const auto d = _endpoint_1 - _endpoint_2;
    const auto segment_vector = line_segment._endpoint_1 - line_segment._endpoint_2;
    const auto segment_start = line_segment._endpoint_2;
    if (d.parallel(segment_vector)) {
        const auto endpoint_1_matches =
            _endpoint_1 == line_segment._endpoint_1 || _endpoint_1 == line_segment._endpoint_2;
        const auto endpoint_2_matches =
            _endpoint_2 == line_segment._endpoint_1 || _endpoint_2 == line_segment._endpoint_2;

        if (endpoint_1_matches) {
            return _endpoint_1;
        } else if (endpoint_2_matches) {
            return _endpoint_2;
        } else {
            return {};
        }
    }

    const auto e = segment_start - _endpoint_2;
    const auto determinant =
        (d.get_longitude() * segment_vector.get_latitude()) - (d.get_latitude() * segment_vector.get_longitude());
    const auto lambda_1 =
        ((e.get_longitude() * segment_vector.get_latitude()) - (e.get_latitude() * segment_vector.get_longitude())) /
        determinant;
    const auto lambda_2 =
        (-(d.get_longitude() * e.get_latitude()) + (d.get_latitude() * e.get_longitude())) / determinant;

    if (lambda_1 < -EPSILON_TOLERANCE_SQUARED || lambda_1 > (1 + EPSILON_TOLERANCE_SQUARED) ||
        lambda_2 < -EPSILON_TOLERANCE_SQUARED || lambda_2 > (1 + EPSILON_TOLERANCE_SQUARED)) {
        return {};
    }

    return segment_start + (segment_vector * lambda_2);
}

Coordinate LineSegment::get_tangent_vector() const { return _endpoint_2 - _endpoint_1; }

Orientation LineSegment::orientation_of_point_to_segment(const Coordinate &point) const {
    const auto signed_area = (_endpoint_2.get_longitude() - _endpoint_1.get_longitude()) *
                                 (point.get_latitude() - _endpoint_1.get_latitude()) -
                             (_endpoint_2.get_latitude() - _endpoint_1.get_latitude()) *
                                 (point.get_longitude() - _endpoint_1.get_longitude());
    if (signed_area > 0) {
        return Orientation::COUNTER_CLOCKWISE;
    }
    if (signed_area < 0) {
        return Orientation::CLOCKWISE;
    }
    return Orientation::COLLINEAR;
}

bool LineSegment::on_segment(const Coordinate &point) const {
    const auto point_orientation = orientation_of_point_to_segment(point);

    if (point_orientation != Orientation::COLLINEAR) {
        return false;
    }

    return ((_endpoint_1.get_longitude() <= point.get_longitude() &&
             point.get_longitude() <= _endpoint_2.get_longitude()) ||
            (_endpoint_2.get_longitude() <= point.get_longitude() &&
             point.get_longitude() <= _endpoint_1.get_longitude())) &&
           ((_endpoint_1.get_latitude() <= point.get_latitude() &&
             point.get_latitude() <= _endpoint_2.get_latitude()) ||
            (_endpoint_2.get_latitude() <= point.get_latitude() && point.get_latitude() <= _endpoint_1.get_latitude()));
}

bool LineSegment::operator==(const LineSegment &other) const {
    return ((_endpoint_1 == other._endpoint_1) && (_endpoint_2 == other._endpoint_2)) ||
           ((_endpoint_1 == other._endpoint_2) && (_endpoint_2 == other._endpoint_1));
}

bool LineSegment::operator!=(const LineSegment &other) const { return !((*this) == other); }
