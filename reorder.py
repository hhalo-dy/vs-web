#!/usr/bin/env python3

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

titles = {
    '13630824': '篇章', '13630835': '百万级教育', '13630822': '十方融海',
    '13630818': '四姑娘山', '13630814': '漫威', '13630905': '星崆',
    '13630826': '声音课程', '13630821': '梨花', '13630816': '雪山',
    '13637090': 'PREETO', '13630825': '4K直播', '13630830': '梨游学'
}

# Build the EXACT delimiter string from file content
newline = '\n'
comment_marker = ' -->' + newline + '<div class="portfolio-card"'
comment_start = '<!-- Project '

def find_card_blocks(html):
    blocks = []
    pos = 0
    while True:
        idx = html.find(comment_start, pos)
        if idx == -1:
            break
        # Extract project number from comment
        end_comment = html.find(' -->', idx)
        if end_comment == -1:
            break
        comment_text = html[idx:end_comment]
        pid_m = None
        for candidate in comment_text.split(newline):
            if 'Project ' in candidate:
                import re
                pid_m = re.search(r'Project\s+(\d+)', candidate)
                break
        if not pid_m:
            pos = end_comment + 5
            continue
        pid = int(pid_m.group(1))

        # Find portfolio-card div start
        div_search = html[end_comment + 4:]
        div_idx = div_search.find('<div class="portfolio-card"')
        if div_idx == -1:
            pos = end_comment + 5
            continue

        block_start = idx
        div_start = end_comment + 4 + div_idx

        # Find block end
        end_pattern = '</div>\n</div>\n'
        end_idx = html.find(end_pattern, div_start)
        if end_idx == -1:
            pos = end_comment + 5
            continue
        block_end = end_idx + len(end_pattern)
        block = html[block_start:block_end]

        # Extract aid for title
        import re
        aid_m = re.search(r'aid=(\d+)', block)
        aid = aid_m.group(1) if aid_m else '?'
        title = titles.get(aid, f'?{aid}')

        blocks.append({
            'pid': pid, 'aid': aid, 'title': title,
            'start': block_start, 'end': block_end, 'block': block
        })
        pos = end_comment + 5

    blocks.sort(key=lambda x: x['start'])
    return blocks

cards = find_card_blocks(content)
print(f'Found {len(cards)} cards')
for i, c in enumerate(cards, 1):
    print(f'  {i}. P{c["pid"]} [{c["aid"]}] {c["title"]}')

if len(cards) != 12:
    print(f'\nERROR: Expected 12 cards, found {len(cards)}')
    exit(1)

# Move PREETO after 十方融海
preeto = next(c for c in cards if c['title'] == 'PREETO')
tenfang = next(c for c in cards if c['title'] == '十方融海')
preeto_i = cards.index(preeto)
tenfang_i = cards.index(tenfang)
print(f'\nPREETO at index {preeto_i+1}, 十方融海 at index {tenfang_i+1}')
print(f'Target: insert at position {tenfang_i+2}')

# Remove PREETO
content_no_p = content.replace(preeto['block'], '', 1)

# Find insertion point after 十方融海
insert_pos = content_no_p.find('</div>\n</div>\n', tenfang['start']) + len('</div>\n</div>\n')
print(f'Insert position: char {insert_pos}')
print(f'Context: {repr(content_no_p[insert_pos-5:insert_pos+30])}')

# Insert PREETO
new_content = content_no_p[:insert_pos] + preeto['block'] + content_no_p[insert_pos:]

# Renumber
import re
new_cards = find_card_blocks(new_content)
for new_id, c in enumerate(new_cards, 1):
    old = c['block']
    new = re.sub(r'<!-- Project \d+ -->', f'<!-- Project {new_id} -->', old, count=1)
    new = re.sub(r'data-card-id="\d+"', f'data-card-id="{new_id}"', new, count=1)
    new_content = new_content.replace(old, new, 1)

# Verify
final = find_card_blocks(new_content)
print(f'\nFinal order ({len(final)}):')
for i, c in enumerate(final, 1):
    print(f'  {i}. {c["title"]}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('\nDone!')
