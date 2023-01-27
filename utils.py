from typing import List, Tuple

ProductIDAndQuantity = Tuple[int, int]


def extract_product_id_and_quantity(raw_data: str) -> List[ProductIDAndQuantity]:
    tuple_data = raw_data.split(',')
    formatted_data: List[Tuple[int, int]] = []
    for elem in tuple_data:
        extracted = elem[1:-1]
        pid, qt = extracted.split(':')
        t = (int(pid), int(qt))
        formatted_data.append(t)
    return formatted_data
