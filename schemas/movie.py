from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=2, max_length=15)
    overview: str = Field(min_length=2, max_length=500)
    year: int = Field(le=2025)
    rating: float = Field(ge = 0, le=10)
    category: str = Field(min_length=3, max_length=15)
    
    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'title': 'Mi película',
                'overview': 'Vista previa',
                'year': 2025,
                'rating': 10,
                'category': 'Acción'
            }
        }
