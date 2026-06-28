import argparse
import sys

from bbm import __version__
from bbm.config import load_env_file

load_env_file()


def _add_common_auth(p):
    p.add_argument('--repo', '-r', action='append', help='Repository name (can be repeated)')
    p.add_argument('--dry-run', action='store_true', help='Simulate without making changes')


def main():
    parser = argparse.ArgumentParser(
        prog='bbm',
        description='Bitbucket Repository Manager — CLI/TUI suite for Bitbucket Cloud',
    )
    parser.add_argument('--version', '-V', action='store_true', help='Show version')

    subparsers = parser.add_subparsers(dest='command')

    # ── permissions ──────────────────────────────────────────────────────────
    p = subparsers.add_parser('permissions', help='Manage repository permissions')
    perm_sub = p.add_subparsers(dest='action')

    list_p = perm_sub.add_parser('list', help='List current permissions for repos')
    list_p.add_argument('--repo', '-r', action='append', required=True)

    grant_p = perm_sub.add_parser('grant', help='Grant permission to a user or group')
    grant_p.add_argument('--user', required=True)
    grant_p.add_argument('--role', required=True, choices=['READ', 'WRITE', 'ADMIN'])
    grant_p.add_argument('--repo', '-r', action='append', required=True)
    grant_p.add_argument('--group', action='store_true')
    grant_p.add_argument('--dry-run', action='store_true')

    revoke_p = perm_sub.add_parser('revoke', help='Revoke permission from a user or group')
    revoke_p.add_argument('--user', required=True)
    revoke_p.add_argument('--repo', '-r', action='append', required=True)
    revoke_p.add_argument('--group', action='store_true')
    revoke_p.add_argument('--dry-run', action='store_true')

    copy_p = perm_sub.add_parser('copy', help='Copy permissions from one repo to others')
    copy_p.add_argument('--from', dest='source', required=True)
    copy_p.add_argument('--to', '-t', action='append', required=True)
    copy_p.add_argument('--dry-run', action='store_true')

    sync_p = perm_sub.add_parser('sync', help='Sync permissions from a CSV file')
    sync_p.add_argument('--file', '-f', required=True)
    sync_p.add_argument('--dry-run', action='store_true')

    # ── pr ────────────────────────────────────────────────────────────────────
    p = subparsers.add_parser('pr', help='Manage pull requests')
    pr_sub = p.add_subparsers(dest='action')

    aa = pr_sub.add_parser('auto-approve', help='Auto-approve PRs based on rules')
    aa.add_argument('--rules', help='Path to rules YAML file')
    aa.add_argument('--repo', '-r', action='append', help='Limit to specific repos')
    aa.add_argument('--dry-run', action='store_true')

    rl = pr_sub.add_parser('rules', help='List PR approval rules')
    rl.add_argument('--rules', help='Path to rules YAML file')

    ch = pr_sub.add_parser('check', help='Check a specific PR against rules')
    ch.add_argument('--pr', type=int, required=True)
    ch.add_argument('--repo', '-r', required=True)
    ch.add_argument('--rules', help='Path to rules YAML file')

    # ── migrate ───────────────────────────────────────────────────────────────
    p = subparsers.add_parser('migrate', help='Migrate repos between workspaces')
    mig_sub = p.add_subparsers(dest='action')

    mp = mig_sub.add_parser('plan', help='Show migration plan')
    mp.add_argument('--repo', '-r', action='append', required=True)
    mp.add_argument('--target-workspace', required=True)
    mp.add_argument('--dry-run', action='store_true')

    mr = mig_sub.add_parser('run', help='Execute migration')
    mr.add_argument('--repo', '-r', action='append', required=True)
    mr.add_argument('--target-workspace', required=True)
    mr.add_argument('--force', action='store_true', help='Overwrite if destination exists')
    mr.add_argument('--yes', '-y', action='store_true', help='Skip confirmation prompt')

    ms = mig_sub.add_parser('status', help='Show migration history')

    # ── archive ───────────────────────────────────────────────────────────────
    p = subparsers.add_parser('archive', help='Manage archived repos')
    arc_sub = p.add_subparsers(dest='action')

    arc_scan = arc_sub.add_parser('scan', help='Scan for candidates to archive')
    arc_scan.add_argument('--days', type=int, help='Min days since last commit')
    arc_scan.add_argument('--rules', help='Path to archive rules YAML')

    arc_run = arc_sub.add_parser('run', help='Archive repos')
    arc_run.add_argument('--repo', '-r', action='append', help='Repos to archive')
    arc_run.add_argument('--days', type=int, help='Min days since last commit')
    arc_run.add_argument('--rules', help='Path to archive rules YAML')
    arc_run.add_argument('--dry-run', action='store_true')
    arc_run.add_argument('--yes', '-y', action='store_true')

    arc_restore = arc_sub.add_parser('restore', help='Restore an archived repo')
    arc_restore.add_argument('--repo', required=True)

    arc_list = arc_sub.add_parser('list', help='List archived repos')

    # ── deps ──────────────────────────────────────────────────────────────────
    p = subparsers.add_parser('deps', help='Analyze cross-repo dependencies')
    deps_sub = p.add_subparsers(dest='action')

    ds = deps_sub.add_parser('scan', help='Scan dependencies of repos')
    ds.add_argument('--repo', '-r', action='append')
    ds.add_argument('--all', action='store_true')
    ds.add_argument('--refresh', action='store_true')

    dt = deps_sub.add_parser('tree', help='Show dependency tree')
    dt.add_argument('--repo', required=True)

    do = deps_sub.add_parser('orphans', help='Find repos with no dependencies')

    dc = deps_sub.add_parser('cycles', help='Detect circular dependencies')

    di = deps_sub.add_parser('impact', help='Show impact of removing a repo')
    di.add_argument('--repo', required=True)

    args = parser.parse_args()

    if args.version:
        print(f"bbm v{__version__}")
        return

    if not args.command:
        from bbm.tui import main as tui_main
        tui_main()
        return

    cmd_map = {
        'permissions': ('bbm.permissions', 'handle_permissions'),
        'pr': ('bbm.pr_approval', 'handle_pr'),
        'migrate': ('bbm.migration', 'handle_migrate'),
        'archive': ('bbm.archiving', 'handle_archive'),
        'deps': ('bbm.deps', 'handle_deps'),
    }

    if args.command in cmd_map:
        mod_path, func_name = cmd_map[args.command]
        module = __import__(mod_path, fromlist=[func_name])
        handler = getattr(module, func_name)
        handler(args)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
