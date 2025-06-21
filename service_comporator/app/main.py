import uvicorn
from fastapi import FastAPI

from schemes import ComparisonRequest, ComparisonResult
from service_comporator.world_comparator import WordComparator

app = FastAPI()


@app.post('/', response_model=ComparisonResult)
async def check_with_comparator(request: ComparisonRequest):
    """
    :param request: word_1: Optional[str] = None, word_2: Optional[str] = None
    :return: Dict[str, Union[Int, Float, Bool]]
    """
    word_1, word_2 = request.word_1, request.word_2
    comparator = WordComparator()
    distance: int = comparator.calculate_distance(word_1, word_2)
    similarity: float = comparator.calculate_similarity(word_1, word_2)
    is_sim: bool = comparator.is_similar(word_1, word_2)
    return {
        "distance": distance,
        "similarity": similarity,
        "is_sim": is_sim
    }


if __name__ == '__main__':
    uvicorn.run(app=app)
