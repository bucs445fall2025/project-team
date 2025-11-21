from typing import Annotated
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from routers.auth import getUserId
from utils.yfinance_api import get_stock_info_multi
from db import get_watchlist, insert_watchlist, remove_from_watchlist

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/user/watchlist")
async def getWatchlist(token: Annotated[str, Depends(oauth2_scheme)]):
	user_id = await getUserId(token)
	watchlist = get_watchlist(user_id)
	if len(watchlist) == 0:
		return []
	return get_stock_info_multi(" ".join(watchlist))

@router.get("/user/watchlist/{ticker}")
async def isInWatchlist(ticker: str, token: Annotated[str, Depends(oauth2_scheme)]):
	user_id = await getUserId(token)
	watchlist = get_watchlist(user_id)
	if ticker in watchlist:
		return True
	return False

@router.post("/user/watchlist/{ticker}")
async def addWatchlist(
	ticker: str, token: Annotated[str, Depends(oauth2_scheme)]
):
	user_id = await getUserId(token)
	ticker = ticker.upper()

	try:
		result = insert_watchlist(user_id, ticker)
		return result
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.delete("/user/watchlist/{ticker}")
async def deleteWatchlist(
	ticker: str, token: Annotated[str, Depends(oauth2_scheme)]
):
	user_id = await getUserId(token)
	ticker = ticker.upper()

	try:
		result = remove_from_watchlist(user_id, ticker)
		if not result["success"]:
			raise HTTPException(status_code=404, detail=result["message"])
		return result
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
