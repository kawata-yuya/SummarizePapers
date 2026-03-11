from glob import glob
from tqdm import tqdm
from pathlib import Path
import os

from summarize_papers import PaperSummarizer

def main():
    
    summarizer = PaperSummarizer(
        api_key=os.getenv('GEMINI_API_KEY'),
        model_name=os.getenv('GEMINI_MODEL'),
        temperature=float(os.getenv('TEMPERATURE')),
        top_p=float(os.getenv('TOP_P')),
        top_k=int(os.getenv('TOP_K')),
        thinking_budget=int(os.getenv('THINKING_BUDGET')),
    )

    pdf_files = list(Path('/app').glob('papers/*.pdf'))

    for pdf_file in tqdm(pdf_files, desc="Summarizing papers", unit="file"):

        tqdm.write(f"Summarizing {pdf_file.name} and saving the summary...")
        _ = summarizer.summarize_paper(pdf_file)




if __name__ == "__main__":
    main()