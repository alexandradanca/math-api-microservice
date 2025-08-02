from models.request_model import MathRequest
from services.math_service import MathService
from models.db import SessionLocal, MathRequestDB, Base, engine
import json

# Create tables if not exist
Base.metadata.create_all(bind=engine)

class MathController:
    def __init__(self):
        self.db = SessionLocal()

    def process_request(self, operation, input_data):
        if operation == "pow":
            result = MathService.pow(input_data["base"], input_data["exp"])
        elif operation == "fibonacci":
            result = MathService.fibonacci(input_data["n"])
        elif operation == "factorial":
            result = MathService.factorial(input_data["n"])
        else:
            raise ValueError("Unknown operation")
        req = MathRequest(operation=operation, input_data=input_data, result=result)
        self.save_request(req)
        return req

    def save_request(self, req: MathRequest):
        db_req = MathRequestDB(
            operation=req.operation,
            input_data=json.dumps(req.input_data),
            result=req.result
        )
        self.db.add(db_req)
        self.db.commit()

    def get_history(self):
        all_reqs = self.db.query(MathRequestDB).all()
        return [
            {
                "operation": r.operation,
                "input_data": json.loads(r.input_data),
                "result": r.result
            } for r in all_reqs
        ]
