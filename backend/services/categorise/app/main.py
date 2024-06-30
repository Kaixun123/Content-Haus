from fastapi import FastAPI

from scraper.scraper import setup_webdriver, search_tiktok, extract_video_metadata, store_data

app = FastAPI()

@app.get("/")
async def root():
    keyword = "funny"  # Replace with desired category keyword
    driver = setup_webdriver()
    page_source = search_tiktok(driver, keyword)
    videos = extract_video_metadata(page_source)
    store_data(videos, f'tiktok_{keyword}_videos.json')
    driver.quit()
    print(f"Scraped {len(videos)} videos for keyword '{keyword}'")
    # return {"message": "Hello World"}