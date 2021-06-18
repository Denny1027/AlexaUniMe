from fastapi import APIRouter, Depends, HTTPException
from ml_tools import guess_number_of_students as g
from utils import utils as u
from auth.auth import get_current_username


router = APIRouter(prefix="/session_students", tags=["Number of students in session exam"])


@router.get("/{cdsId}/{adId}")
async def check_if_exist(cdsId: str, adId: int, isAuth: bool = Depends(get_current_username)):
    var = g.guess_subscriber(cdsId, adId, u.get_path())

    if var:
        return var
    else:
        raise HTTPException(status_code=404, detail="No data found.")