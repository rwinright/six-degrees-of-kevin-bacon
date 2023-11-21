from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests

app = FastAPI()
#Enable connection from all origins

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/degrees/{start_page}")
def get_degrees(start_page: str):
    print("Request received")
    target_page = "Kevin_Bacon"
    visited_pages = set()

    # return {"start_page": start_page}

    def get_links(page):
        response = requests.get(f"https://en.wikipedia.org/wiki/{page}")
        # if the response is 404, throw an error
        if response.status_code == 404:
            raise Exception("Page not found")
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'][6:] for a in soup.find_all('a', href=True) if a['href'].startswith('/wiki/')]
        return links

    def traverse(current_page, depth):
        if current_page == target_page:
            return depth

        visited_pages.add(current_page)

        links = get_links(current_page)
        
        remove_words = ['Main_Page', 'Wikipedia', 'Help', 'File', 'Special', 'Portal', 'Talk', 'Template', 'Template_talk', 'Category', 'Category_talk', 'Draft', 'Draft_talk', 'TimedText', 'Module', 'Module_talk', 'MediaWiki', 'MediaWiki_talk', 'User', 'User_talk', 'Book', 'Book_talk', 'Education_Program', 'Education_Program_talk', 'Gadget', 'Gadget_talk', 'Gadget_definition', 'Gadget_definition_talk', 'Topic', 'Special', 'Talk', 'Template', 'Template_talk', 'Category', 'Category_talk', 'Draft', 'Draft_talk', 'TimedText', 'Module', 'Module_talk', 'MediaWiki', 'MediaWiki_talk', 'User', 'User_talk', 'Book', 'Book_talk', 'Education_Program', 'Education_Program_talk', 'Gadget', 'Gadget_talk', 'Gadget_definition', 'Gadget_definition_talk', 'Topic', ":"]
        
        #remove all links that contain the words in remove_words
        for word in remove_words:
            links = [link for link in links if word not in link]

        print(links)

        if target_page in links:
            return depth + 1
        for link in links:
            if link not in visited_pages:
                result = traverse(link, depth + 1)
                if result is not None:
                    return result

        return None

    degrees = traverse(start_page, 0)
    return {"degrees": degrees} if degrees is not None else {"message": "No connection found"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
