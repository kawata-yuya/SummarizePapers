from google import genai
from google.genai import types
import pathlib
import json
import uuid # UUIDモジュールを追加
import os   # OSモジュールを追加
from datetime import datetime
import shutil

class PaperSummarizer:
    """
    A class to summarize PDF research papers using the Google Gemini API and save summaries.
    """

    # _MODELS = {
    #     "2.5_flash": "gemini-2.5-flash-preview-05-20",
    #     "2.5_pro": "gemini-2.5-pro-preview-06-05",
    #     "test": "gemini-2.0-flash",
    #     "fast_test": "gemini-2.0-flash-lite",
    # }
    _PROMPT_FILE = '/app/config/prompt.txt'

    def __init__(self,
                 api_key: str,
                 model_name: str,
                 temperature: float,
                 top_p: float,
                 top_k: int,
                 thinking_budget: int,
                 ):
        """
        Initializes the PaperSummarizer with a specific Gemini model and generation configuration.

        Args:
            api_key: GEMINI_API_KEY
            model_name (str): Use ai model's name.
            temperature (float): Controls the randomness of the output.
            top_p (float): The nucleus sampling probability.
            top_k (int): The number of highest probability tokens to keep for top-k sampling.
            thinking_budget (int): The number of thinking tokens.
        """

        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.thinking_budget = thinking_budget
        self._api_key = api_key
        self._prompt = self._load_prompt()
        self._client = genai.Client(api_key=self._api_key)

        now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self._output_dir = f'output/{now_str}' # 出力ディレクトリを追加
        self._move_pdf_dir = f'output/{now_str}/pdf' # 出力ディレクトリを追加
        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(self._output_dir, exist_ok=True)
        os.makedirs(self._move_pdf_dir, exist_ok=True)

    def _load_prompt(self) -> str:
        """Loads the prompt text from the specified file."""
        try:
            with open(self._PROMPT_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found at {self._PROMPT_FILE}")

    def summarize_paper(self, filepath: pathlib.Path) -> str:
        """
        Summarizes a PDF paper using the configured Gemini model and saves it to a Markdown file.

        Args:
            filepath (str): The path to the PDF file to summarize.

        Returns:
            str: The summarized text from the Gemini model.

        Raises:
            FileNotFoundError: If the specified PDF file does not exist.
            Exception: For any errors during the API call or file saving.
        """
        pdf_path = pathlib.Path(filepath)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found at: {filepath}")

        try:
            response = self._client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Part.from_bytes(
                        data=pdf_path.read_bytes(),
                        mime_type='application/pdf',
                    ),
                    self._prompt
                ],
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    topP=self.top_p,
                    topK=self.top_k,
                    thinking_config=types.ThinkingConfig(thinking_budget=self.thinking_budget),
                )
            )
            summary_text = response.text

            # UUID5 を生成し、ファイル名を決定
            # ファイルパスを名前空間として使用し、常に同じファイルからは同じUUIDが生成される
            namespace = uuid.NAMESPACE_URL
            uid = uuid.uuid5(namespace, filepath.name)
            summary_filename = f"{uid}.md"
            output_filepath = os.path.join(self._output_dir, summary_filename)

            # Markdownファイルとして保存
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(f"<!--\nuuid: {uid}\nfilename: {filepath.name}\nmodel_name: {self.model_name}\n-->\n\n")
                f.write(summary_text)

            print(f"Summary saved to: {output_filepath}")

            pdf_new_path = pathlib.Path(self._move_pdf_dir) / pdf_path.name
            shutil.copy2(pdf_path, pdf_new_path)

            return summary_text
        except Exception as e:
            raise Exception(f"An error occurred during summarization or file saving: {e}")

# --- Example Usage ---
if __name__ == "__main__":
    try:
        summarizer = PaperSummarizer(model_name="fast_test", temperature=0.2)

        print("Summarizing paper1.pdf and saving the summary...")
        summary1 = summarizer.summarize_paper("papers/data.pdf")
        print("\n--- Summary 1 (printed to console) ---")
        print(summary1)

        # 別の論文を要約する場合も、同じ summarizer オブジェクトを再利用できる
        # print("\nSummarizing paper2.pdf and saving the summary...")
        # summary2 = summarizer.summarize_paper("papers/another_data.pdf")
        # print("\n--- Summary 2 (printed to console) ---")
        # print(summary2)

    except (FileNotFoundError, KeyError, ValueError, Exception) as e:
        print(f"Error: {e}")