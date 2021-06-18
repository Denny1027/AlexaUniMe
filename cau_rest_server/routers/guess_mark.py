from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ml_tools import guess_your_marks as g
from auth.auth import get_current_username

router = APIRouter(prefix="/guess_mark", tags=["Guess Mark"])


class UserInfo(BaseModel):
    ponderata: str
    data_imm: str
    data_nascita: str


@router.post("/{aaOrdId}/{cdsId}/{adId}")
async def guess_the_mark(aaOrdId, cdsId, adId, body: UserInfo, isAuth: bool = Depends(get_current_username)):
    res = g.guess(cdsId, aaOrdId, adId, body.ponderata, body.data_imm, body.data_nascita)
    res = round(res['value'])
    if res == -1 or res == -2:
        raise HTTPException(status_code=404, detail="Vote cannot be guessed. Missing ml module or directory.")
    elif res >= 18:
        return {"result": res, "pass": True}
    elif res < 18:
        return {"result": res, "pass": False}
    else:
        raise HTTPException(status_code=403, detail="There is something wrong and the guess cannot be satisfied.")