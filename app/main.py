from fastapi import FastAPI

app = FastAPI(title="Pharmacy Inventory API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/branches")
def get_branches():
    return ["Manila Main Branch", "Quezon City Hub"]