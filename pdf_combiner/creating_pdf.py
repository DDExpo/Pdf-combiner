from pathlib import Path

from fitz import Rect, FileDataError
from fitz import open as f_open

from const import (
    DATE_NAME, PAPER_SIZES, EXTRACT_DATA_DIR)
from utility import (
    get_pair_with_smallest_diff, get_edges_of_content)


def create_combine_pdf(
        ui, pdfs: list[Path], pdf_file_path_origin: Path,
        page_size: str, quantity: int, crope: list[int],
        spacing: float) -> None:

    pdf_file_path: Path = pdf_file_path_origin / (DATE_NAME + '.pdf')
    temp_pdfs_path: list[Path] = []
    copy_pdf: int = 0
    index: int = 0
    problem_pdfs: int = 0
    problem_pdfs_indexies: list[int] = []

    paper_width, paper_height = (PAPER_SIZES[page_size].width,
                                 PAPER_SIZES[page_size].height)

    row_count, col_count = get_pair_with_smallest_diff(quantity)

    elem_width: float = paper_width / row_count
    elem_height: float = paper_height / col_count

    while pdf_file_path.exists():
        copy_pdf += 1
        pdf_file_path = (
            pdf_file_path_origin /
            (DATE_NAME + f'({str(copy_pdf)})' + '.pdf'))

    iterations: int = (len(pdfs) // quantity if len(pdfs) % quantity == 0
                       else len(pdfs) // quantity + 1)

    minllx = minlly = maxurx = maxury = 0
    if not crope.strip():
        minllx, minlly, maxurx, maxury = get_edges_of_content(pdfs[0])
    else:
        minllx, minlly, maxurx, maxury = map(float, crope.split(','))

    for number in range(iterations):
        with f_open() as doc:
            destpage = doc.new_page(-1, width=paper_width,
                                    height=paper_height)
            row = 0
            for _ in range(col_count):
                col = 0
                for _ in range(row_count):
                    if index < len(pdfs):
                        try:
                            with f_open(pdfs[index]) as curr_data:
                                elem_width_s = abs(
                                    (elem_width * spacing) - elem_width
                                    ) // quantity
                                elem_height_s = abs(
                                    (elem_height * spacing) - elem_height
                                    ) // quantity
                                x_cor = col * elem_width
                                y_cor = row * elem_height

                                x_cor = (
                                    x_cor
                                    if x_cor + elem_width <= paper_width
                                    else paper_width-elem_width-5)
                                y_cor = (
                                    y_cor
                                    if y_cor + elem_height <= paper_height
                                    else paper_height-elem_height-5)

                                destpage.show_pdf_page(
                                    Rect(
                                        x_cor, y_cor,
                                        x_cor + (elem_width-elem_width_s),
                                        y_cor + (elem_height-elem_height_s)),
                                    curr_data, 0, keep_proportion=False,
                                    clip=Rect(minllx, minlly, maxurx, maxury)
                                    )

                        except FileDataError:
                            problem_pdfs += 1
                            problem_pdfs_indexies.append(index+1)

                    else:
                        break

                    index += 1
                    col += 1
                row += 1

            new_path = EXTRACT_DATA_DIR / f'temp_{number}.pdf'
            temp_pdfs_path.append(new_path)

            doc.save(new_path, garbage=3, deflate=True)

    with f_open() as doc:
        for pdfs_path in temp_pdfs_path:
            doc.insert_pdf(f_open(pdfs_path))

        doc.save(pdf_file_path, garbage=3, deflate=True)

    if problem_pdfs > 0:
        ui.message_box.warning(
            ui, 'Предупреждение',
            f'Было пропущенно PDF: {problem_pdfs} '
            'так как они сломаны \n'
            f'Их номера: {problem_pdfs_indexies}')
