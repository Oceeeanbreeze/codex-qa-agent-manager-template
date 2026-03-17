import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REQUIRED_DATASETS = {
    'routing': ['id', 'prompt', 'expected_route', 'expected_roles'],
    'retrieval': ['id', 'role', 'query', 'expected_paths'],
    'reviewer': ['id', 'change_summary', 'expected_findings'],
    'coverage': ['id', 'feature', 'expected_layers'],
    'browser_validation': ['id', 'surface', 'expected_browser_checks'],
}


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def load_evals_config(path: Path) -> dict[str, Any]:
    config = load_yaml(path) or {}
    if not isinstance(config, dict):
        raise SystemExit(f'Invalid evals config at {path}')
    return config


def validate_case(case: dict[str, Any], required_fields: list[str]) -> list[str]:
    missing = []
    for field in required_fields:
        value = case.get(field)
        if value is None:
            missing.append(field)
            continue
        if isinstance(value, str) and not value.strip():
            missing.append(field)
            continue
        if isinstance(value, list) and not value:
            missing.append(field)
    return missing


def dataset_case_count_gate(config: dict[str, Any], dataset_name: str) -> int:
    defaults = config.get('quality_gates', {}) if isinstance(config.get('quality_gates'), dict) else {}
    minimums = defaults.get('minimum_case_counts', {}) if isinstance(defaults.get('minimum_case_counts'), dict) else {}
    value = minimums.get(dataset_name, 1)
    try:
        return max(int(value), 1)
    except (TypeError, ValueError):
        return 1


def build_dataset_report(dataset_name: str, dataset_path: Path, config: dict[str, Any]) -> dict[str, Any]:
    required_fields = REQUIRED_DATASETS[dataset_name]
    result = {
        'dataset': dataset_name,
        'path': str(dataset_path),
        'status': 'ready',
        'total_cases': 0,
        'valid_cases': 0,
        'invalid_cases': [],
        'categories': {},
        'minimum_required_cases': dataset_case_count_gate(config, dataset_name),
    }

    if not dataset_path.exists():
        result['status'] = 'missing'
        return result

    payload = load_yaml(dataset_path) or {}
    if not isinstance(payload, dict):
        result['status'] = 'invalid'
        result['invalid_cases'].append({'case_id': '<dataset>', 'missing_fields': ['root mapping']})
        return result

    cases = payload.get('cases', [])
    if not isinstance(cases, list):
        result['status'] = 'invalid'
        result['invalid_cases'].append({'case_id': '<dataset>', 'missing_fields': ['cases list']})
        return result

    result['total_cases'] = len(cases)
    category_counter: Counter[str] = Counter()

    for idx, raw_case in enumerate(cases, start=1):
        if not isinstance(raw_case, dict):
            result['invalid_cases'].append({'case_id': f'<case-{idx}>', 'missing_fields': ['mapping structure']})
            continue
        case_id = raw_case.get('id', f'<case-{idx}>')
        missing_fields = validate_case(raw_case, required_fields)
        if missing_fields:
            result['invalid_cases'].append({'case_id': case_id, 'missing_fields': missing_fields})
            continue
        result['valid_cases'] += 1
        category_counter.update(ensure_list(raw_case.get('category')))

    if category_counter:
        result['categories'] = dict(sorted(category_counter.items()))

    if result['invalid_cases']:
        result['status'] = 'degraded'
    if result['total_cases'] < result['minimum_required_cases']:
        result['status'] = 'degraded'
        result['case_count_gate_failed'] = True
    else:
        result['case_count_gate_failed'] = False
    if result['total_cases'] == 0:
        result['status'] = 'empty'
    return result


def build_summary(dataset_reports: list[dict[str, Any]]) -> dict[str, Any]:
    summary = Counter(report['status'] for report in dataset_reports)
    total_cases = sum(report['total_cases'] for report in dataset_reports)
    valid_cases = sum(report['valid_cases'] for report in dataset_reports)
    return {
        'ready': summary.get('ready', 0),
        'degraded': summary.get('degraded', 0),
        'empty': summary.get('empty', 0),
        'missing': summary.get('missing', 0),
        'invalid': summary.get('invalid', 0),
        'datasets_total': len(dataset_reports),
        'cases_total': total_cases,
        'cases_valid': valid_cases,
        'dataset_readiness_ratio': round((summary.get('ready', 0) / len(dataset_reports)) if dataset_reports else 0.0, 3),
    }


def build_gate_status(config: dict[str, Any], summary: dict[str, Any], dataset_reports: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = config.get('metrics', {}) if isinstance(config.get('metrics'), dict) else {}
    quality_gates = config.get('quality_gates', {}) if isinstance(config.get('quality_gates'), dict) else {}
    dataset_target = quality_gates.get('dataset_readiness_target', 1.0)
    valid_case_target = quality_gates.get('valid_case_ratio_target', 1.0)
    try:
        dataset_target = float(dataset_target)
    except (TypeError, ValueError):
        dataset_target = 1.0
    try:
        valid_case_target = float(valid_case_target)
    except (TypeError, ValueError):
        valid_case_target = 1.0

    valid_case_ratio = round((summary['cases_valid'] / summary['cases_total']) if summary['cases_total'] else 0.0, 3)
    failing_datasets = [report['dataset'] for report in dataset_reports if report['status'] in {'missing', 'invalid', 'empty', 'degraded'}]
    return {
        'status': 'pass' if summary['dataset_readiness_ratio'] >= dataset_target and valid_case_ratio >= valid_case_target and not failing_datasets else 'fail',
        'dataset_readiness_ratio': summary['dataset_readiness_ratio'],
        'dataset_readiness_target': dataset_target,
        'valid_case_ratio': valid_case_ratio,
        'valid_case_ratio_target': valid_case_target,
        'tracked_metric_targets': metrics,
        'failing_datasets': failing_datasets,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        '# Evals Report',
        '',
        f"- Captured at: `{report['captured_at']}`",
        f"- Config: `{report['config_path']}`",
        f"- Overall gate: `{report['gates']['status']}`",
        f"- Dataset readiness ratio: `{report['gates']['dataset_readiness_ratio']}` / target `{report['gates']['dataset_readiness_target']}`",
        f"- Valid case ratio: `{report['gates']['valid_case_ratio']}` / target `{report['gates']['valid_case_ratio_target']}`",
        '',
        '## Summary',
        '',
        f"- Datasets total: `{report['summary']['datasets_total']}`",
        f"- Ready: `{report['summary']['ready']}`",
        f"- Degraded: `{report['summary']['degraded']}`",
        f"- Empty: `{report['summary']['empty']}`",
        f"- Missing: `{report['summary']['missing']}`",
        f"- Invalid: `{report['summary']['invalid']}`",
        f"- Cases total: `{report['summary']['cases_total']}`",
        f"- Cases valid: `{report['summary']['cases_valid']}`",
        '',
        '## Dataset status',
        '',
    ]

    for dataset in report['datasets']:
        lines.append(f"### {dataset['dataset']}")
        lines.append(f"- Status: `{dataset['status']}`")
        lines.append(f"- Path: `{dataset['path']}`")
        lines.append(f"- Cases: `{dataset['total_cases']}` total, `{dataset['valid_cases']}` valid")
        lines.append(f"- Minimum required cases: `{dataset['minimum_required_cases']}`")
        if dataset['categories']:
            categories = ', '.join(f"{key}: {value}" for key, value in dataset['categories'].items())
            lines.append(f"- Categories: `{categories}`")
        if dataset['invalid_cases']:
            lines.append('- Invalid cases:')
            for invalid in dataset['invalid_cases']:
                missing = ', '.join(invalid['missing_fields'])
                lines.append(f"  - `{invalid['case_id']}` missing `{missing}`")
        lines.append('')

    if report['gates']['failing_datasets']:
        failing = ', '.join(report['gates']['failing_datasets'])
        lines.extend([
            '## Failing datasets',
            '',
            f"- `{failing}`",
            '',
        ])

    lines.extend([
        '## Operator next step',
        '',
        '- Add or fix the failing dataset cases before using evals as a scale-up gate.',
        '- When dataset readiness is green, layer live scoring or reviewer spot-checks on top of the same golden sets.',
    ])
    return '\n'.join(lines) + '\n'


def write_report(output_dir: Path, report: dict[str, Any]) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    json_path = output_dir / f'evals-report-{stamp}.json'
    md_path = output_dir / f'evals-report-{stamp}.md'
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(report), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--output-dir', default='')
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    config = load_evals_config(config_path)
    dataset_map = config.get('datasets', {})
    if not isinstance(dataset_map, dict):
        raise SystemExit('Evals config must contain a datasets mapping.')

    dataset_reports = []
    for dataset_name in REQUIRED_DATASETS:
        raw_path = dataset_map.get(dataset_name)
        dataset_path = (config_path.parent.parent / raw_path).resolve() if raw_path else Path('')
        dataset_reports.append(build_dataset_report(dataset_name, dataset_path, config))

    summary = build_summary(dataset_reports)
    gates = build_gate_status(config, summary, dataset_reports)
    output_dir = Path(args.output_dir).resolve() if args.output_dir else (config_path.parent.parent / config.get('reports', {}).get('directory', 'reports/evals')).resolve()
    report = {
        'captured_at': datetime.now(timezone.utc).isoformat(),
        'config_path': str(config_path),
        'datasets': dataset_reports,
        'summary': summary,
        'gates': gates,
    }
    report_paths = write_report(output_dir, report)
    report['report_paths'] = report_paths

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.strict and gates['status'] != 'pass':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
