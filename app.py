from glob import glob
from tqdm import tqdm
from pathlib import Path
import yaml

from summarize_papers import PaperSummarizer

def main():
    workspace_dir = Path(__file__).parent
    yaml_file_path = workspace_dir / "config/setting.yaml"

    settings = yaml.load(open(yaml_file_path), Loader=yaml.FullLoader)

    if not(  isinstance(settings.get('model_name'), str) and 
            (isinstance(settings.get('temperature'), float) or isinstance(settings.get('temperature'), int))):
        raise ValueError("Invalid settings in the YAML file. Please check 'model_name' and 'temperature'.")
    else:
        model_name = settings.get('model_name')
        temperature = settings.get('temperature')
    
    summarizer = PaperSummarizer(model_name=model_name, temperature=temperature)

    pdf_files = list(workspace_dir.glob('papers/*.pdf'))

    for pdf_file in tqdm(pdf_files, desc="Summarizing papers", unit="file"):

        tqdm.write(f"Summarizing {pdf_file.name} and saving the summary...")
        _ = summarizer.summarize_paper(pdf_file)




if __name__ == "__main__":
    main()