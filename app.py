from glob import glob
from tqdm import tqdm
from pathlib import Path


from summarize_papers import PaperSummarizer

def main():
    summarizer = PaperSummarizer(model_name="fast_test", temperature=0.2)

    workspace_dir = Path(__file__).parent
    pdf_files = list(workspace_dir.glob('papers/*.pdf'))

    for pdf_file in tqdm(pdf_files, desc="Summarizing papers", unit="file"):

        tqdm.write(f"Summarizing {pdf_file.name} and saving the summary...")
        _ = summarizer.summarize_paper(pdf_file)




if __name__ == "__main__":
    main()