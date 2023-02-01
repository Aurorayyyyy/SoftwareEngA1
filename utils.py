from typing import List, Tuple

from models.machines import VendingMachine
from models.stocks import VendingMCProduct

ProductIDAndQuantity = Tuple[int, int]


def extract_product_id_and_quantity(raw_data: str) -> List[ProductIDAndQuantity]:
    tuple_data = raw_data.split(",")
    formatted_data: List[Tuple[int, int]] = []
    for elem in tuple_data:
        extracted = elem[1:-1]
        pid, qt = extracted.split(":")
        t = (int(pid), int(qt))
        formatted_data.append(t)
    return formatted_data


def get_formatting_list_of_product_id(
    machine: VendingMachine, raw_list: List[Tuple[int, int]]
) -> List[int]:
    return_list: List[int] = []
    for elem in raw_list:
        product_id, product_quantity = elem
        relation = VendingMCProduct.get(machine.id, product_id)
        if relation:
            machine.edit_product_in_machine(product_id, product_quantity)
            return_list.append(product_id)
        else:
            machine.add_product_to_the_stock(product_id, product_quantity)
            return_list.append(product_id)
    return return_list
