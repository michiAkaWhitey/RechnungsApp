from dataclasses import dataclass, field
import numpy as np
from typing import List
import cv2

@dataclass
class FormData:
    date: str
    price: float
    company: str
    tags: List[str]
    img: np.ndarray = field(repr=False)

    def isDefault(self) -> bool:
        '''checks if variable are default values. If so returns True. Otherwise False'''
        if (self.date == "" or self.price == 0.0 or self.company == "" or self.img is None):
            return True
        return False
    
    def toTuple(self) -> tuple:        
        return (self.date, self.price, self.company, ",".join(self.tags), 
                cv2.imencode('.jpg', self.img)[1].tobytes())

