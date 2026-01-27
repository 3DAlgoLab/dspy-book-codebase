from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import mlflow
from mlflow.entities import AssessmentSource, AssessmentSourceType
from datetime import datetime
from typing import Optional, Literal
import dspy
from dotenv import load_dotenv

load_dotenv()

# Configure dspy
lm = dspy.LM("gemini/gemini-2.5-flash")
dspy.configure(lm=lm)

app = FastAPI()

@app.get("/")
async def serve_qa():
    return FileResponse("qa.html")

# Set MLflow tracking URI
mlflow.set_tracking_uri("http://localhost:5000")  # Your MLflow server

class QueryRequest(BaseModel):
    question: str
    user_id: str

class FeedbackRequest(BaseModel):
    trace_id: str  # <1>
    feedback: Literal["thumbs_up", "thumbs_down"]
    user_id: str
    rationale: Optional[str] = None
    corrected_answer: Optional[str] = None

@app.post("/ask")
@mlflow.trace(name="qa_endpoint", span_type="CHAIN")  # <2>
async def ask_question(request: QueryRequest):
    """Main Q&A endpoint that creates MLflow trace"""
    
    # Your LLM inference logic here (automatically traced)
    answer = generate_answer(request.question)
    
    # <3>
    trace_id = mlflow.get_current_active_span().request_id
    
    return {
        "trace_id": trace_id,  # <4>
        "question": request.question,
        "answer": answer
    }

class QASignature(dspy.Signature):
    """Answer the user question helpfuly and concisely."""
    question = dspy.InputField()
    answer = dspy.OutputField()

@mlflow.trace(name="llm_generation", span_type="LLM")
def generate_answer(question: str) -> str:
    """Your LLM inference logic - automatically traced"""
    # proper dspy call
    predictor = dspy.ChainOfThought(QASignature)
    response = predictor(question=question)
    return response.answer

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Capture user feedback and log to MLflow using trace_id"""
    
    try:
        # Determine feedback value
        is_positive = feedback.feedback == "thumbs_up"
        rationale = feedback.rationale or (
            "User indicated response was helpful" if is_positive 
            else "User indicated response was not helpful"
        )
        
        # <5>
        mlflow.log_feedback(
            trace_id=feedback.trace_id,  # <6>
            name="user_satisfaction",
            value=is_positive,
            rationale=rationale,
            source=AssessmentSource(  # <7>
                source_type=AssessmentSourceType.HUMAN,
                source_id=feedback.user_id
            )
        )
        
        # <8>
        if not is_positive and feedback.corrected_answer:
            mlflow.log_feedback(
                trace_id=feedback.trace_id,
                name="corrected_answer",
                value=feedback.corrected_answer,
                rationale="User provided corrected answer for review",
                source=AssessmentSource(
                    source_type=AssessmentSourceType.HUMAN,
                    source_id=feedback.user_id
                )
            )
        
        return {
            "status": "success",
            "message": "Feedback logged successfully",
            "trace_id": feedback.trace_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to log feedback: {str(e)}"
        )

@app.get("/feedback/review-queue")
async def get_review_queue():
    """Get all traces with negative feedback for expert review"""
    
    # <9>
    traces = mlflow.search_traces(
        experiment_names=["default"],  # Your experiment name
        filter_string="assessments.user_satisfaction.value = false"  # <10>
    )
    
    review_items = []
    for trace in traces:
        # Extract feedback details
        user_satisfaction = trace.data.assessments.get("user_satisfaction", {})
        corrected_answer = trace.data.assessments.get("corrected_answer", {})
        
        review_items.append({
            "trace_id": trace.info.request_id,
            "question": trace.data.request,
            "answer": trace.data.response,
            "corrected_answer": corrected_answer.get("value"),
            "user_id": user_satisfaction.get("source", {}).get("source_id"),
            "rationale": user_satisfaction.get("rationale"),
            "timestamp": trace.info.timestamp_ms
        })
    
    return {"review_queue": review_items, "count": len(review_items)}
