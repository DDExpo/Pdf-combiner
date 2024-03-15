import subprocess

import fitz

from const import BASE_DIR


def get_edges_of_content(pdf_path: str) -> tuple[float, float, float, float]:

    doc = fitz.open(pdf_path)
    page = doc[0]

    minllx, minlly, maxurx, maxury = (float('inf'), float('inf'),
                                      float('-inf'), float('-inf'))

    for _, cords in page.get_bboxlog():
        minllx, minlly, maxurx, maxury = (
            min(minllx, cords[0]), min(minlly, cords[1]),
            max(maxurx, cords[2]), max(maxury, cords[3])
            )

    return (minllx/2, 0, maxurx, maxury)


def get_pair_with_smallest_diff(num: int) -> tuple[int, int]:

    factors: list[tuple[int, int]] = []

    for i in range(1, int(num ** 0.5) + 1):
        if num % i == 0:
            factors.append((i, num // i))

    min_diff = float('inf')
    closest_pair: tuple[int, int] = None

    for pair in factors:
        diff = abs(pair[0] - pair[1])
        if diff < min_diff:
            min_diff = diff
            closest_pair = pair

    return closest_pair


def check_dirs_ifnot_create(directories: list[str]) -> None:

    for directory in directories:
        path_to_dir = BASE_DIR / directory

        if path_to_dir.exists():
            return

        path_to_dir.mkdir(parents=True, exist_ok=True)
        return


def delete_all_data(path_data: str) -> None:

    subprocess.run(["del", "/Q", f"{path_data}\\*"], shell=True)
