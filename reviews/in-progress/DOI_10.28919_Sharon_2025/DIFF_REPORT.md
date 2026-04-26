import sys
import json
import re
import yaml
from pathlib import Path
from datetime import datetime
from difflib import unified_diff


def load_team_members(repo_root='.'):
    mapping_path = Path(repo_root) / 'team_members.yml'
    if not mapping_path.exists():
        return {}
    with open(mapping_path, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('members', {})


def resolve_github_username(name, members):
    return members.get(name.strip(), name.strip())


def parse_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    cells = []
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown' and i == 0:
            source = ''.join(cell['source'])
            cells.append({
                'index': i,
                'type': 'markdown',
                'source': source,
                'code': None,
                'changed_reasons': [],
                'dispute_reasons': []
            })
            continue
        if cell['cell_type'] != 'code':
            continue
        source = ''.join(cell['source'])
        if not source.strip():
            continue
        source_cite = None
        changed_reasons = []
        dispute_reasons = []
        code_lines = []
        for line in source.splitlines():
            if re.search(r'#\s*SOURCE:', line, re.IGNORECASE):
                source_cite = re.sub(r'#\s*SOURCE:\s*', '', line, flags=re.IGNORECASE).strip()
            elif re.search(r'#\s*DISPUTE:\s*(.*)', line, re.IGNORECASE):
                match = re.search(r'#\s*DISPUTE:\s*(.*)', line, re.IGNORECASE)
                reason = match.group(1).strip()
                if reason:
                    dispute_reasons.append(reason)
                code_part = line[:match.start()].rstrip()
                if code_part.strip():
                    code_lines.append(code_part)
            elif re.search(r'#\s*CHANGED:\s*(.*)', line, re.IGNORECASE):
                match = re.search(r'#\s*CHANGED:\s*(.*)', line, re.IGNORECASE)
                reason = match.group(1).strip()
                if reason:
                    changed_reasons.append(reason)
                code_part = line[:match.start()].rstrip()
                if code_part.strip():
                    code_lines.append(code_part)
            else:
                code_lines.append(line)
        cells.append({
            'index': i,
            'type': 'code',
            'source': source,
            'code': '\n'.join(code_lines).strip(),
            'source_cite': source_cite,
            'changed_reasons': changed_reasons,
            'dispute_reasons': dispute_reasons
        })
    return cells


def parse_metadata(path):
    with open(path, 'r') as f:
        content = f.read()
    meta = {}
    for line in content.splitlines():
        if ':' in line:
            key, _, value = line.partition(':')
            meta[key.strip()] = value.strip().strip('"')
    return meta


def extract_markdown_fields(source):
    fields = {}
    for line in source.splitlines():
        if ':' in line:
            key, _, value = line.partition(':')
            fields[key.strip()] = value.strip()
    return fields


def get_line_diff(r1_source, r2_source):
    r1_lines = r1_source.splitlines()
    r2_lines = r2_source.splitlines()
    diff = list(unified_diff(
        r1_lines,
        r2_lines,
        lineterm='',
        fromfile='curator',
        tofile='reviewer',
        n=2
    ))
    removed = [l[1:].strip() for l in diff if l.startswith('-') and not l.startswith('---')]
    added = [l[1:].strip() for l in diff if l.startswith('+') and not l.startswith('+++')]
    return removed, added, diff


def generate_report(folder_path, repo_root='.'):
    folder = Path(folder_path)
    meta_path = folder / 'review_metadata.yml'

    if not meta_path.exists():
        print(f'No review_metadata.yml found in {folder}')
        return

    members = load_team_members(repo_root)
    meta = parse_metadata(meta_path)
    original_name = meta.get('original_notebook', '').strip()
    review_name = meta.get('review_copy_notebook', '').strip()
    reviewer = meta.get('reviewer', 'unknown').strip()

    original_path = folder / 'original' / original_name
    review_path = folder / 'review-copy' / review_name

    if not original_path.exists():
        print(f'Original notebook not found: {original_path}')
        return
    if not review_path.exists():
        print(f'Review notebook not found: {review_path}')
        return

    r1_cells = parse_notebook(original_path)
    r2_cells = parse_notebook(review_path)

    r1_meta = {}
    r2_meta = {}
    if r1_cells and r1_cells[0]['type'] == 'markdown':
        r1_meta = extract_markdown_fields(r1_cells[0]['source'])
    if r2_cells and r2_cells[0]['type'] == 'markdown':
        r2_meta = extract_markdown_fields(r2_cells[0]['source'])

    curator_name = r1_meta.get('Curator', 'unknown')
    curator_github = resolve_github_username(curator_name, members)
    title = r1_meta.get('Title', 'Unknown paper')
    doi = r1_meta.get('DOI', '')
    figure = r1_meta.get('Figure', '')
    r1_outcome = r1_meta.get('Outcome', '')
    r2_outcome = r2_meta.get('Outcome', '')
    r1_notes = r1_meta.get('Notes', '')
    r2_notes = r2_meta.get('Notes', '')

    r1_code = [c for c in r1_cells if c['type'] == 'code']
    r2_code = [c for c in r2_cells if c['type'] == 'code']

    agreed = []
    disagreed = []
    disputed = []
    total_changes = 0

    for c1, c2 in zip(r1_code, r2_code):
        if c1['code'] == c2['code']:
            agreed.append(c1)
        else:
            removed, added, raw_diff = get_line_diff(c1['source'], c2['source'])
            reasons = c2['changed_reasons']
            disputes = c2['dispute_reasons']
            total_changes += max(len(removed), len(added), 1)
            entry = {
                'cell': c1['index'],
                'source_cite': c1['source_cite'] or c2['source_cite'] or 'no citation',
                'removed': removed,
                'added': added,
                'raw_diff': raw_diff,
                'reasons': reasons,
                'disputes': disputes
            }
            disagreed.append(entry)
            if disputes:
                disputed.append(entry)

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        f'# Diff report - {title}',
        f'',
        f'**Curator:** @{curator_github}  ',
        f'**Reviewer:** @{reviewer}  ',
        f'**DOI:** {doi}  ',
        f'**Figure:** {figure}  ',
        f'**Generated:** {now}  ',
        f'',
        f'---',
        f'',
        f'## Summary',
        f'',
        f'| | Count |',
        f'|---|---|',
        f'| Cells compared | {len(r1_code)} |',
        f'| Cells agreed | {len(agreed)} |',
        f'| Cells with differences | {len(disagreed)} |',
        f'| Total lines changed | {total_changes} |',
        f'| Cells with disputes | {len(disputed)} |',
        f'',
    ]

    if r1_outcome != r2_outcome or r1_notes != r2_notes:
        lines += [
            f'## Metadata changes',
            f'',
            f'| Field | Curator | Reviewer |',
            f'|---|---|---|',
            f'| Outcome | {r1_outcome} | {r2_outcome} |',
            f'| Notes | {r1_notes} | {r2_notes} |',
            f'',
            f'---',
            f'',
        ]

    lines += [f'## Agreements ({len(agreed)} cells)', f'']
    if agreed:
        lines.append('The following cells matched exactly between curator and reviewer.')
        lines.append('')
    else:
        lines.append('No agreements found.')
        lines.append('')

    lines += [f'---', f'', f'## Differences ({total_changes} lines changed across {len(disagreed)} cells)', f'']

    for d in disagreed:
        has_dispute = len(d['disputes']) > 0
        dispute_flag = ' - DISPUTED' if has_dispute else ''
        lines += [
            f"### Cell {d['cell']} - {d['source_cite']}{dispute_flag}",
            f'',
        ]

        # Show diff with 2 lines of context
        lines += ['```diff']
        for l in d['raw_diff']:
            if not l.startswith('---') and not l.startswith('+++'):
                lines.append(l)
        lines += ['```', '']

        # Reviewer reasons
        if d['reasons']:
            lines.append(f'**Reviewer reasons ({len(d["reasons"])}):**')
            lines.append('')
            for i, reason in enumerate(d['reasons'], 1):
                lines.append(f'{i}. {reason}')
            lines.append('')
        else:
            lines.append('**Reviewer reason:** not provided')
            lines.append('')

        # Curator disputes
        if d['disputes']:
            lines.append(f'**Curator disputes ({len(d["disputes"])}):**')
            lines.append('')
            for i, dispute in enumerate(d['disputes'], 1):
                lines.append(f'{i}. {dispute}')
            lines.append('')
            lines.append('> This cell is disputed. Reviewer should review the curator dispute and update their notebook or provide additional evidence.')
            lines.append('')

    # Disputed section for easy scanning
    if disputed:
        lines += [
            f'---',
            f'',
            f'## Disputed cells ({len(disputed)})',
            f'',
            f'These cells have been disputed by the curator. They need to be resolved before /complete can be used.',
            f'',
        ]
        for d in disputed:
            lines.append(f'- Cell {d["cell"]} ({d["source_cite"]})')
            for dispute in d['disputes']:
                lines.append(f'  - Curator: {dispute}')
        lines.append('')

    # Curator notification
    lines += [
        f'---',
        f'',
        f'## Curator notification',
        f'',
        f'@{curator_github} - your submission has been second reviewed by @{reviewer}.',
        f'',
    ]
    if total_changes == 0:
        lines.append('All cells agreed - no differences found.')
        lines.append('')
        lines.append('Comment `/complete` to move this to completed.')
    else:
        lines.append(f'{total_changes} line(s) changed across {len(disagreed)} cell(s):')
        lines.append('')
        for d in disagreed:
            for i, (rem, add) in enumerate(zip(d['removed'], d['added'])):
                reason = d['reasons'][i] if i < len(d['reasons']) else 'no reason provided'
                lines.append(f'- `{rem}` changed to `{add}` - {reason}')
            if len(d['added']) > len(d['removed']):
                for add in d['added'][len(d['removed']):]:
                    lines.append(f'- added `{add}`')
            if len(d['removed']) > len(d['added']):
                for rem in d['removed'][len(d['added']):]:
                    lines.append(f'- removed `{rem}`')
            if d['disputes']:
                lines.append(f'  - You have disputed this change. The reviewer will be asked to respond.')
        lines.append('')
        if disputed:
            lines.append(f'You have disputed {len(disputed)} cell(s). Add your reasons using `#DISPUTE: reason` in the reviewer notebook and comment `/approve` again to regenerate this report.')
        else:
            lines.append('If you agree with the changes comment `/complete` to finalize.')
            lines.append('If you disagree open the reviewer notebook, add `#DISPUTE: reason` above the disputed line, and comment on this issue.')
            lines.append('The reviewer can update their notebook and comment `/approve` again to regenerate this report.')

    lines.append('')

    report_path = folder / 'DIFF_REPORT.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'Report written to {report_path}')
    print(f'{len(agreed)} agreements, {total_changes} lines changed across {len(disagreed)} cells, {len(disputed)} disputed')
    print(f'curator_github:{curator_github}')

    return {
        'curator': curator_github,
        'title': title,
        'total_changes': total_changes,
        'disagreed': disagreed,
        'disputed': disputed
    }


if __name__ == '__main__':
    folder = sys.argv[1] if len(sys.argv) > 1 else 'reviews/completed/10_1007s00332.023_copy'
    generate_report(folder)