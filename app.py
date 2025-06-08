from glob import glob
from tqdm import tqdm
from pathlib import Path


from summarize_papers import PaperSummarizer

def main():
    summarizer = PaperSummarizer(model_name="fast_test", temperature=0.2)

    workspace_dir = Path(__file__).parent

    for pdf_file in workspace_dir.glob('papers/*.pdf'):

        print(f"Summarizing {pdf_file.name} and saving the summary...")
        summary = summarizer.summarize_paper(pdf_file)
        print(f"\n--- Summary {pdf_file.name} (printed to console) ---")
        print(summary)




if __name__ == "__main__":
    main()