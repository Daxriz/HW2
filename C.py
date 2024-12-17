import argparse
import os
import subprocess
import re

def parse_dependencies(package_path):
    dependencies = set()
    with open(package_path, 'r') as file:
        for line in file:
            match = re.search(r'Depends: (.+)', line)
            if match:
                deps = match.group(1).split(',')
                dependencies.update(dep.strip() for dep in deps)
    return dependencies

def build_mermaid_graph(dependencies, max_depth):
    graph = "graph TD;\n"
    for dep in dependencies:
        graph += f"    {dep};\n"
    return graph

def save_graph_to_file(graph, output_path):
    with open('graph.mmd', 'w') as file:
        file.write(graph)
    
    # Визуализация графа с помощью mermaid-cli
    subprocess.run(['mmdc', '-i', 'graph.mmd', '-o', output_path])

def main():
    parser = argparse.ArgumentParser(description='Visualize package dependencies in Mermaid format.')
    parser.add_argument('--visualizer', required=True, help='Path to the visualizer program.')
    parser.add_argument('--package', required=True, help='Path to the package file.')
    parser.add_argument('--output', required=True, help='Path to the output image file.')
    parser.add_argument('--max-depth', type=int, default=1, help='Maximum depth of dependency analysis.')

    args = parser.parse_args()

    dependencies = parse_dependencies(args.package)
    graph = build_mermaid_graph(dependencies, args.max_depth)
    save_graph_to_file(graph, args.output)

    print("Граф зависимостей успешно создан и сохранен в", args.output)

if __name__ == '__main__':
    main()
