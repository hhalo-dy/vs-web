#!/usr/bin/env python3
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

titles = {
    '13630824': '篇章', '13630835': '百万级教育', '13630822': '十方融海',
    '13630818': '四姑娘山', '13630814': '漫威', '13630905': '星崆',
    '13630826': '声音课程', '13630821': '梨花', '13630816': '雪山',
    '13637090': 'PREETO', '13630825': '4K直播', '13630830': '梨游学'
}

# Use actual newline character
pat = re.compile(r'<!-- Project ([0-9]+) -->' + '\n' + r'<div class="portfolio-card"')
matches = list(pat.finditer(content))
print(f'Found {len(matches)} card matches')
