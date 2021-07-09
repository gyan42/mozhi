from typing import List

IOU_THRESHOLD = 0.5

def find_iou(coord1,
             coord2,
             inter_object=False,
             columns_group=False) -> List:
    """
    Finds the intersecting bounding boxes by finding
       the highest x and y ranges of the 2 coordinates
       and determine the intersection by deciding weather
       the new xmin > xmax or the new ymin > ymax.
       For non image objects, includes finding the intersection
       area to a threshold to determine intersection
    @param coord1: list of coordinates of 1st object
    @param coord2: list of coordinates of 2nd object
    @param inter_object: check for cleaning between different overlapping
                         objects.
    @param columns_group: If the intersection finding is needed in columns
                          grouping use case
    @return: [True/False, point1 area, point2 area]
    """
    iou_xmin = max(coord1[0], coord2[0])
    iou_ymin = max(coord1[1], coord2[1])
    iou_xmax = min(coord1[2], coord2[2])
    iou_ymax = min(coord1[3], coord2[3])

    # no intersection
    if iou_xmax - iou_xmin <= 0 or iou_ymax - iou_ymin <= 0:
        return [False]

    intersection_area = (iou_xmax - iou_xmin) * (iou_ymax - iou_ymin)
    point1_area = (coord1[2] - coord1[0]) * (coord1[3] - coord1[1])
    point2_area = (coord2[2] - coord2[0]) * (coord2[3] - coord2[1])
    iou = (intersection_area
           / (point1_area + point2_area - intersection_area))

    # find if given 2 objects intersects or not
    if columns_group:
        if ((point1_area + point2_area - intersection_area == 0)
                or iou > 0):
            return [True, abs(iou_xmax - iou_xmin), abs(iou_ymax - iou_ymin)]
        return [True, abs(iou_xmax - iou_xmin), abs(iou_ymax - iou_ymin)]

    # -if iou check is for inter object overlap removal check only for
    # intersection.
    # -if not for inter objects overlap check for iou >= threshold
    # -if the intersection area covers more than 50% of the smaller object
    if ((point1_area + point2_area - intersection_area == 0)
            or (inter_object and iou > 0)
            or (iou >= IOU_THRESHOLD)
            or (iou <= IOU_THRESHOLD
                and
                (intersection_area /
                 min(point1_area, point2_area)) >= 0.50)):
        return [True, point1_area, point2_area]

    return [False]


class Rectangle(object):
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.x1 = left
        self.y1 = top
        self.x2 = left + width
        self.y2 = top + height

    def __repr__(self):
        return f"{(self.x1,self.y1)} {(self.x2,self.y2)}"

    def do_overlap(self, other):
        return find_iou(coord1=[self.x1, self.y1, self.x2, self.y2], coord2=[other.x1, other.y1, other.x2, other.y2])


if __name__ == "__main__":
    # print(Rectangle(0, 10, 10, 0) == Rectangle(5, 5, 15, 0))
    print(Rectangle(57, 9, 49, 20))
    print(Rectangle(54, 6, 56, 27))
    print(Rectangle(57, 9, 49, 20).do_overlap(Rectangle(54, 6, 56, 27)))