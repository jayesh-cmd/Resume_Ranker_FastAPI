from fastapi import UploadFile
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from utils import extract_text_from_pdf
from sentence_transformers import SentenceTransformer
from functools import lru_cache

model = SentenceTransformer("all-MiniLM-L6-v2")

async def process_resumes(job_description : str , files : List[UploadFile]):
    job_emb = model.encode(job_description)

    results = []
    for file in files:
        pdf_bytes = await file.read()
        resume_text = extract_text_from_pdf(pdf_bytes)
        resume_emb = model.encode(resume_text)
        score = cosine_similarity([job_emb] , [resume_emb])[0][0]

        results.append({
            "filename" : file.filename,
            "score" : round(float(score) , 4)
        })

        ranked = sorted(results, key=lambda x: x["score"], reverse=True)
    return {"ranked_resumes": ranked}