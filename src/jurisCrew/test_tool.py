from crewai import Task
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup

class WebScraperInput(BaseModel):
    url: str = Field(..., description="URL to scrape")
    keyword: str | None = Field(default=None, description="Keyword to search for")

class WebScraperTool(BaseTool):
    name: str = "Web Scraper"
    description: str = "Scrapes a webpage and searches for a keyword."

    def _run(self, input: WebScraperInput) -> dict:
        try:
            response = requests.get(input.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text().lower()
            
            if input.keyword:
                occurrences = text.count(input.keyword.lower())
                return {
                    "url": input.url,
                    "keyword": input.keyword,
                    "occurrences": occurrences,
                    "message": f"Found {occurrences} occurrences of '{input.keyword}'"
                }
            
            return {
                "url": input.url,
                "content": text[:500],
                "message": "Full page content fetched."
            }
        except requests.RequestException as e:
            return {"error": f"Failed to fetch the URL: {str(e)}"}

web_scraper_task = Task(
    description="Scrape a webpage and search for a keyword.",
    tool=WebScraperTool(),
    expected_output={"occurrences": int}
)

if __name__ == "__main__":
    result = WebScraperTool().run(WebScraperInput(url="https://doe.sp.gov.br/busca-avancada", keyword="saúde"))
    print(result)