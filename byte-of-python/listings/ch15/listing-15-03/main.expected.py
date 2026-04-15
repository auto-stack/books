def sort_by_y(points):
    # Python can use a lambda for a concise one-liner
    points.sort(key=lambda i: i["y"])
    return points


def main():
    points = [{"x": 2, "y": 3}, {"x": 4, "y": 1}]
    sorted_points = sort_by_y(points)
    print(sorted_points)


if __name__ == "__main__":
    main()
