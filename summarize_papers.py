from google import genai
from google.genai import types
import pathlib
import json
import uuid # UUIDモジュールを追加
import os   # OSモジュールを追加
from datetime import datetime

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
    _API_KEY_FILE = './gemini_api_key.json'
    _PROMPT_FILE = './prompt.txt'

    def __init__(self, model_name: str, temperature: float = 0.2):
        """
        Initializes the PaperSummarizer with a specific Gemini model and generation configuration.

        Args:
            model_name (str): Use ai model's name.
            temperature (float): Controls the randomness of the output.
        """

        self.model_name = model_name
        self.temperature = temperature
        self._api_key = self._load_api_key()
        self._prompt = self._load_prompt()
        self._client = genai.Client(api_key=self._api_key)

        now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self._output_dir = f'output/{now_str}' # 出力ディレクトリを追加
        self._move_pdf_dir = f'output/{now_str}/pdf' # 出力ディレクトリを追加
        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(self._output_dir, exist_ok=True)
        os.makedirs(self._move_pdf_dir, exist_ok=True)

    def _load_api_key(self) -> str:
        """Loads the API key from the specified JSON file."""
        try:
            with open(self._API_KEY_FILE, 'r') as f:
                return json.load(f)['key']
        except FileNotFoundError:
            raise FileNotFoundError(f"API key file not found at {self._API_KEY_FILE}")
        except KeyError:
            raise KeyError(f"API key not found in {self._API_KEY_FILE}. Make sure it has a 'key' field.")

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
                    thinking_config=types.ThinkingConfig(thinking_budget=-1),
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
                f.write(f"uuid: {uid}\nfilename: {filepath.name}\n\n---\n\n")
                f.write(summary_text)

            print(f"Summary saved to: {output_filepath}")

            pdf_new_path = pathlib.Path(self._move_pdf_dir) / pdf_path.name
            pdf_path.rename(pdf_new_path)

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