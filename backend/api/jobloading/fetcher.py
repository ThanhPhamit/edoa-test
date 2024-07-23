import requests
import logging
import re
import asyncio
import time

from bs4 import BeautifulSoup
from pyppeteer import launch
from .result import JobLoadingResult

urls_for_scraping_fetch = [
    r'^https://herp\.careers/[^/]+/[^/]+/[^/]+/?$',
    r'^https://agent\.herp\.cloud/[^/]+/[^/]+/requisitions/id/[^/]+/?$',
    r'^https://open\.talentio\.com/[^/]+/[^/]+/[^/]+/[^/]+/pages/[^/]+/?$',
]

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'

def fetch_from_url(source_url: str, result: JobLoadingResult) -> str:
    if any([re.match(pattern, source_url) for pattern in urls_for_scraping_fetch]):
        result.set_telemetry('fetch_method', 'Scraping')
        return asyncio.run(fetch_by_scraping_async(source_url, result))
    else:
        result.set_telemetry('fetch_method', 'REST GET')
        return fetch_by_rest_get(source_url, result)

def fetch_by_rest_get(source_url: str, result: JobLoadingResult) -> str:
    logging.info(f'Fetching {source_url} by REST GET')
    response = requests.get(source_url, headers={"User-Agent": user_agent})
    logging.info(f'GET {source_url} {response.status_code}')
    response.raise_for_status()
    html_content = response.text
    return process_html_content(html_content, source_url, result)

async def fetch_by_scraping_async(source_url: str, result: JobLoadingResult) -> str:
    logging.info(f'Fetching {source_url} by scraping')
    start_time = time.time()
    browser = await launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox'],
        logLevel=logging.WARNING
    )
    try:
        page = await browser.newPage()
        await page.setUserAgent(user_agent)
        await page.goto(source_url)
        time.sleep(1)
        html_content = await page.content()

        scraping_time = round(time.time() - start_time)
        result.set_telemetry('scraping_time', scraping_time)
        logging.info(f'Fetched {source_url} by scraping in {scraping_time} seconds')

        return process_html_content(html_content, source_url, result)
    finally:
        await browser.close()

def process_html_content(html_content: str, source_url: str, result: JobLoadingResult) -> str:
    
    html = BeautifulSoup(html_content, 'html.parser')
    result.add_telemetry_html_processing('original', len(html_content))

    # HTMLの分量を減らす. タグの構造は解析に有用である場合があるため残す.
    # 後行順の深さ優先探索で情報を削除していく
    def drop(target_tag, remove_tags, remove_attrs):
        for child in target_tag.find_all(recursive=False):
            drop(child, remove_tags, remove_attrs) # 後行順
        # 処理
        if target_tag.name and (target_tag.name.lower() in remove_tags): # 肥大化する情報の薄いタグは削除
            target_tag.extract()
        for attr in remove_attrs: # 肥大化しやすい属性は削除
            if target_tag.has_attr(attr):
                del target_tag[attr]
        if not target_tag.contents and not target_tag.text.strip() and not target_tag.attrs: # 内容も属性もない空のタグは削除
            target_tag.extract()

    drop(html, ['link', 'style', 'svg', 'img'], ['id', 'class', 'style'])
    processed_content = str(html)
    result.add_telemetry_html_processing('remove tags/atributes: [link, style, svg, img], [id, class, style]', len(processed_content))

    # HTMLの場合、Tokenは文字数の約80%. promptとcompletion合わせて16000トークンに収めることを考慮
    max_content_length_html = 14000

    if (len(processed_content) > max_content_length_html):
        logging.info('The web content is too long. Meta and script tags are removed.')
        drop(html, ['meta', 'script'], [])
        processed_content = str(html)
        result.add_telemetry_html_processing('remove tags: [meta, script]', len(processed_content))
    
    if (len(processed_content) <= max_content_length_html):
        logging.info(f'Processed HTML for {source_url}: {len(html_content)} -> {len(processed_content)}')
        return processed_content

    # テキストコンテンツの場合、Tokenは文字数の約120%. promptとcompletion合わせて16000トークンに収めることを考慮
    max_content_length_text = 10000

    if (len(processed_content) > max_content_length_text):
        # HTML構造を取り除き、テキストのみに変換（マーカーで構造をできるだけ保持）
        logging.info('The web content is too long. HTML structure is removed.')
        processed_content = html.get_text(' # ', strip=True)
        result.add_telemetry_html_processing('remove HTML structure', len(processed_content))
    
    if (len(processed_content) > max_content_length_text):
        # 構造マーカーを取り除いて妥協
        logging.info('The web content is too long. Structure markers are removed.')
        processed_content = html.get_text(' ', strip=True)
        result.add_telemetry_html_processing('remove structure markers', len(processed_content))
    
    if (len(processed_content) > max_content_length_text):
        # それでも最大文字数を超える場合は、末尾を削る
        logging.warning('The web content is too long. The content is trimmed to max_content_length characters')
        processed_content = processed_content[:max_content_length_text]
        result.add_telemetry_html_processing('trim content', len(processed_content))

    logging.info(f'Processed HTML for {source_url}: {len(html_content)} -> {len(processed_content)}')
    return processed_content