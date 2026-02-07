"""
REPOSITORY TOPOLOGY SCANNER
Substrate-First Analysis for Logic Engine Navigation
"""

import os
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import json

class TopologyScanner:
    """Map repository as navigable city for logic engines"""
    
    CODE_EXTS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cs', '.cpp', '.c', '.h', '.json', '.yaml', '.yml', '.toml'}
    
    IMPORT_PATTERNS = {
        'python': [
            (r'^\s*import\s+([a-zA-Z_][a-zA-Z0-9_\.]*)', 'import'),
            (r'^\s*from\s+([a-zA-Z_][a-zA-Z0-9_\.]*)\s+import', 'from'),
        ],
        'javascript': [
            (r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]', 'es6_import'),
            (r'require\([\'"]([^\'"]+)[\'"]\)', 'require'),
        ],
    }
    
    def __init__(self, root_path):
        self.root = Path(root_path).resolve()
        self.files = {}
        self.dependency_graph = defaultdict(set)
        self.reverse_deps = defaultdict(set)
        
    def scan(self):
        """Execute full topology scan"""
        print(f"\n🏗️  SCANNING: {self.root}\n")
        
        # Census
        self._walk_tree()
        print(f"✓ Census: {len(self.files)} files")
        
        # Dependencies
        self._extract_dependencies()
        print(f"✓ Dependencies extracted")
        
        # Analysis
        report = self._analyze()
        print(f"✓ Analysis complete\n")
        
        return report
    
    def _walk_tree(self):
        """Catalog all files"""
        ignore = {'node_modules', '.git', '__pycache__', 'venv', 'dist', 'build'}
        
        for root, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if d not in ignore]
            
            for fname in files:
                fpath = Path(root) / fname
                rel_path = fpath.relative_to(self.root)
                
                self.files[str(rel_path)] = {
                    'path': fpath,
                    'size': fpath.stat().st_size if fpath.exists() else 0,
                    'ext': fpath.suffix,
                    'imports': set(),
                    'depth': len(rel_path.parts)
                }
    
    def _extract_dependencies(self):
        """Extract import relationships"""
        for rel_path, info in self.files.items():
            if info['ext'] not in self.CODE_EXTS:
                continue
            
            try:
                content = info['path'].read_text(encoding='utf-8', errors='ignore')
                
                # Python imports
                if info['ext'] == '.py':
                    for pattern, _ in self.IMPORT_PATTERNS['python']:
                        for match in re.finditer(pattern, content, re.MULTILINE):
                            imported = match.group(1)
                            info['imports'].add(imported)
                            self.dependency_graph[rel_path].add(imported)
                
                # JS/TS imports  
                elif info['ext'] in {'.js', '.ts', '.jsx', '.tsx'}:
                    for pattern, _ in self.IMPORT_PATTERNS['javascript']:
                        for match in re.finditer(pattern, content, re.MULTILINE):
                            imported = match.group(1)
                            info['imports'].add(imported)
                            self.dependency_graph[rel_path].add(imported)
            except:
                pass
    
    def _analyze(self):
        """Structural analysis"""
        # Calculate fan-in (how many files import this)
        for source, targets in self.dependency_graph.items():
            for target in targets:
                self.reverse_deps[target].add(source)
        
        # Highways (high fan-in)
        highways = sorted(
            [(module, len(importers)) for module, importers in self.reverse_deps.items()],
            key=lambda x: x[1],
            reverse=True
        )[:20]
        
        # Orphans (zero dependencies)
        all_files = set(self.files.keys())
        referenced = set(self.dependency_graph.keys()) | set(self.reverse_deps.keys())
        orphans = all_files - referenced
        
        # File type distribution
        ext_dist = Counter(info['ext'] for info in self.files.values())
        
        # Depth distribution
        depth_dist = Counter(info['depth'] for info in self.files.values())
        
        return {
            'total_files': len(self.files),
            'total_size': sum(f['size'] for f in self.files.values()),
            'file_types': dict(ext_dist),
            'highways': highways,
            'orphans': list(orphans)[:50],
            'depth_distribution': dict(depth_dist),
            'dependency_count': len(self.dependency_graph),
        }
    
    def generate_html_report(self, report, output_path):
        """Generate interactive HTML map"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Topology Report: {self.root.name}</title>
    <style>
        body {{ font-family: monospace; background: #0a0a0a; color: #00ff00; padding: 20px; }}
        h1 {{ color: #00ff00; border-bottom: 2px solid #00ff00; }}
        h2 {{ color: #00dd00; margin-top: 30px; }}
        .metric {{ background: #1a1a1a; padding: 15px; margin: 10px 0; border-left: 3px solid #00ff00; }}
        .highway {{ color: #ffaa00; }}
        .orphan {{ color: #ff5555; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #00ff00; padding: 8px; text-align: left; }}
        th {{ background: #1a1a1a; }}
        .code {{ background: #111; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>🏗️ REPOSITORY TOPOLOGY: {self.root.name}</h1>
    <p>Generated: {datetime.now().isoformat()}</p>
    
    <div class="metric">
        <h2>📊 CENSUS</h2>
        <p>Total Files: {report['total_files']}</p>
        <p>Total Size: {report['total_size']:,} bytes</p>
        <p>Dependencies Mapped: {report['dependency_count']}</p>
    </div>
    
    <div class="metric">
        <h2>🛣️ HIGHWAYS (High Fan-In)</h2>
        <p>Most-imported modules (critical infrastructure):</p>
        <table>
            <tr><th>Module</th><th>Import Count</th></tr>
            {''.join(f'<tr><td class="highway">{mod}</td><td>{count}</td></tr>' for mod, count in report['highways'][:15])}
        </table>
    </div>
    
    <div class="metric">
        <h2>🏚️ ORPHANS (Zero Dependencies)</h2>
        <p>Files with no import relationships (isolated structures):</p>
        <div class="code">
            {'<br>'.join(f'<span class="orphan">{o}</span>' for o in report['orphans'][:30])}
        </div>
    </div>
    
    <div class="metric">
        <h2>📁 FILE TYPE DISTRIBUTION</h2>
        <table>
            <tr><th>Extension</th><th>Count</th></tr>
            {''.join(f'<tr><td>{ext or "(none)"}</td><td>{count}</td></tr>' for ext, count in sorted(report['file_types'].items(), key=lambda x: x[1], reverse=True)[:20])}
        </table>
    </div>
    
    <div class="metric">
        <h2>📏 DEPTH DISTRIBUTION</h2>
        <table>
            <tr><th>Depth</th><th>Files</th></tr>
            {''.join(f'<tr><td>{depth}</td><td>{count}</td></tr>' for depth, count in sorted(report['depth_distribution'].items()))}
        </table>
    </div>
</body>
</html>"""
        
        Path(output_path).write_text(html, encoding='utf-8')
        print(f"✓ Report: {output_path}")


if __name__ == '__main__':
    import sys
    
    repo_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    scanner = TopologyScanner(repo_path)
    report = scanner.scan()
    
    output = Path(repo_path) / 'TOPOLOGY_REPORT.html'
    scanner.generate_html_report(report, output)
    
    print(f"\n📍 Open: {output}")
