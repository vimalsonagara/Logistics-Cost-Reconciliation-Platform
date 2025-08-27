from fastapi import APIRouter, UploadFile, File, HTTPException,Form
from backend.core.reader import read_excel
from pathlib import Path
from backend.config import UPLOAD_DIR
from backend.core.reconciler import calculate_company_costs
from backend.core.optimizer import greedy_pack_trucks
import shutil, uuid,time

router = APIRouter()

@router.post("/")
async def upload_excel(total_cost: float= Form(...),file: UploadFile = File(...)):
    print("data received")
    # t1=time.perf_counter()
    if not file.filename.endswith((".xls",".xlsx")):
        raise HTTPException(status_code=400, detail="Only Excel files allowed")
    
    ext = Path(file.filename).suffix
    unique_name = f"{uuid.uuid4().hex}{ext}"
    dest = UPLOAD_DIR / unique_name
    
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        df = read_excel(dest)
        company_costs = calculate_company_costs(df, total_cost)
        util = greedy_pack_trucks(df)
        # t2=time.perf_counter()
        return {
            "total_cost": total_cost,
            "total_load": float(df["assigned_load"].sum()),
            "company_costs": company_costs,
            "Optimization": util,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        try:
            dest.unlink()
        except Exception as cleanup_error:
            print(f"Failed to delete temp file: {dest} -> {cleanup_error}")
