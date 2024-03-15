from typing import Union


class UnitNumber:  # TODO: build upon float/int

    def __init__ (self, val: Union[int, float], unit: str = None):
        raise NotImplementedError
        self.val = val
        self.unit = unit
    
    def __repr__ (self):
        return f'[{self.unit}] {self.val}'
