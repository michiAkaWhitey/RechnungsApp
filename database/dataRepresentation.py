from dataclasses import dataclass, field
import numpy as np
from typing import List
import cv2
from datetime import date

@dataclass
class Bill:
    date: date
    price: float
    company: str
    tags: List[str]
    img: np.ndarray = field(repr=False)
    
    def toTuple(self) -> tuple:        
        return (self.date, self.price, self.company, ",".join(self.tags), 
                cv2.imencode('.jpg', self.img)[1].tobytes())

