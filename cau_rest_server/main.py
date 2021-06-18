from fastapi import FastAPI
from routers import guess_mark, guess_session

app = FastAPI()

app.include_router(guess_mark.router)
app.include_router(guess_session.router)

#in caso si dovesse cambiare porta o host, togliere #
#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)