from pathlib import Path

import fitz

from const import (
    DATE_NAME, PAPER_SIZES, EXTRACT_DATA_DIR)
from utility import (
    get_pair_with_smallest_diff, get_edges_of_content)


def create_combine_pdf(ui, pdfs: list[Path], pdf_file_path_origin: Path,
                       page_size: str, quantity: int) -> None:

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
    minllx, minlly, maxurx, maxury = get_edges_of_content(pdfs[0])

    for number in range(iterations):
        with fitz.open() as doc:
            destpage = doc.new_page(-1, width=paper_width,
                                    height=paper_height)
            row = 0
            for _ in range(col_count):
                col = 0
                for _ in range(row_count):
                    if index < len(pdfs):
                        try:
                            with fitz.open(pdfs[index]) as curr_data:
                                x_cor = col * elem_width
                                y_cor = row * elem_height
                                destpage.show_pdf_page(
                                    fitz.Rect(
                                        x_cor, y_cor, x_cor + elem_width,
                                        y_cor + elem_height),
                                    curr_data, 0, keep_proportion=False,
                                    clip=fitz.Rect(minllx, minlly,
                                                   maxurx, maxury)
                                    )

                        except fitz.FileDataError:
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

    with fitz.open() as doc:
        for pdfs_path in temp_pdfs_path:
            doc.insert_pdf(fitz.open(pdfs_path))

        doc.save(pdf_file_path, garbage=3, deflate=True)

    if problem_pdfs > 0:
        ui.message_box.warning(
            ui, 'Предупреждение',
            f'Было пропущенно PDF: {problem_pdfs} '
            'так как они сломаны \n'
            f'Их номера: {problem_pdfs_indexies}')
