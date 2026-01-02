import dspy
from dspy import streamify
from dspy.streaming import StreamListener
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse

app = FastAPI()

gemini = dspy.LM(model="gemini/gemini-2.5-pro")
dspy.configure(lm=gemini)

class QA(dspy.Signature):
    """Answer questions with detailed explanations."""
    question = dspy.InputField()
    answer = dspy.OutputField()

@app.get('/chat/stream')
async def stream_chat(question: str = Query(..., description="The question to ask")):
    
    async def generate():
        stream_listeners = [
            StreamListener(signature_field_name="reasoning"),
            StreamListener(signature_field_name="answer")
        ]
        
        predictor = dspy.ChainOfThought(QA)
        streaming_predictor = streamify(predictor, stream_listeners=stream_listeners)
        
        has_streamed = False
        
        async for chunk in streaming_predictor(question=question):
            
            if isinstance(chunk, dspy.streaming.StreamResponse):
                has_streamed = True
                yield f"{chunk.chunk}"

            elif isinstance(chunk, dspy.Prediction):
                if not has_streamed:
                    if hasattr(chunk, 'reasoning') and chunk.reasoning:
                         yield f"{chunk.reasoning}"
                    if hasattr(chunk, 'answer') and chunk.answer:
                         yield f"{chunk.answer}"

    return StreamingResponse(generate(), media_type='text/event-stream')