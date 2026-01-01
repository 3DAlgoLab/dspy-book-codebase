import dspy
from dspy import streamify
from dspy.streaming import StreamListener  # <1> Import StreamListener
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse

app = FastAPI()

# Configure DSPy
gemini = dspy.LM(model="gemini/gemini-2.5-pro")
dspy.configure(lm=gemini)

class QA(dspy.Signature):
    """Answer questions with detailed explanations."""
    question = dspy.InputField()
    answer = dspy.OutputField()

@app.get('/chat/stream')
async def stream_chat(question: str = Query(..., description="The question to ask")):
    
    async def generate():
        # 1. Define listeners for the fields you want to stream.
        #    This automatically handles the parsing of "[[ ## ... ## ]]" delimiters.
        stream_listeners = [
            StreamListener(signature_field_name="reasoning"),
            StreamListener(signature_field_name="answer")
        ]
        
        # 2. Pass the listeners to streamify
        predictor = dspy.ChainOfThought(QA)
        streaming_predictor = streamify(predictor, stream_listeners=stream_listeners)
        
        # 3. Iterate over the stream
        async for chunk in streaming_predictor(question=question):
            
            # Case A: It's a streaming chunk (Text)
            if isinstance(chunk, dspy.streaming.StreamResponse):
                # chunk.signature_field_name tells you if it is 'reasoning' or 'answer'
                # chunk.chunk contains the clean text (no delimiters)
                yield f"{chunk.chunk}"
            
            # Case B: It's the final Prediction object (Summary)
            elif isinstance(chunk, dspy.Prediction):
                # Optional: You can do something with the final complete object here
                pass

    return StreamingResponse(generate(), media_type='text/event-stream')