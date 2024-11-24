import os
import zipfile
import io

def parse_tree(file_path):
    """Parse o ficheiro para criar uma estrutura em árvore."""
    tree = {}
    current_path = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.rstrip()
            if not line.strip():  # Ignora linhas vazias
                continue

            indent_level = len(line) - len(line.lstrip())
            node = line.strip()

            # Atualiza o nível atual
            while len(current_path) > indent_level:
                current_path.pop()

            # Adiciona o nó à árvore
            current_tree = tree
            for part in current_path:
                current_tree = current_tree[part]

            if '=' in node:
                name, content = node.split('=', 1)
                current_tree[name] = content.replace('\\n', '\n').replace('\\r', '\r')
            elif '|' in node:
                name, file_path = node.split('|', 1)
                file_path = file_path.strip()
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    current_tree[name] = content
                else:
                    print(f"Aviso: Ficheiro binário '{file_path}' não encontrado!")
                    current_tree[name] = b''  # Ficheiro vazio
            else:
                current_tree[node] = {}
                current_path.append(node)

    return tree

def add_to_zip(zip_obj, tree, base_path=""):
    """Adiciona diretórios e ficheiros ao ficheiro ZIP."""
    for name, content in tree.items():
        zip_path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Diretório
            add_to_zip(zip_obj, content, zip_path)
        else:
            if isinstance(content, bytes):  # Ficheiro binário
                zip_obj.writestr(zip_path, content)
            else:  # Ficheiro de texto
                zip_obj.writestr(zip_path, content)

def main():
    input_file = input("Insira o nome do ficheiro de entrada (.txt): ").strip()
    if not os.path.isfile(input_file):
        print("Ficheiro não encontrado!")
        return

    tree = parse_tree(input_file)
    output_zip = os.path.splitext(input_file)[0] + ".zip"

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zip_obj:
        add_to_zip(zip_obj, tree)

    print(f"Ficheiro ZIP criado: {output_zip}")

if __name__ == "__main__":
    main()

