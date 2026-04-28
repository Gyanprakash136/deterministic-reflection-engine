import json
import os
import sys

def validate_tree(file_path):
    print(f"--- Validating Reflection Tree: {file_path} ---")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    nodes = data.get('nodes', [])
    node_ids = {n['id'] for n in nodes}
    errors = []
    warnings = []

    # 1. Check for START and END
    if 'START' not in node_ids:
        errors.append("Missing 'START' node.")
    if 'END' not in node_ids:
        errors.append("Missing 'END' node.")

    for node in nodes:
        nid = node.get('id')
        ntype = node.get('type')
        
        # 2. Check for missing 'next' or children
        if ntype not in ['end']:
            if ntype == 'decision':
                logic = node.get('logic', {})
                conditions = logic.get('conditions', [])
                if not conditions:
                    errors.append(f"Decision node '{nid}' has no conditions.")
                for cond in conditions:
                    target = cond.get('then')
                    if target not in node_ids:
                        errors.append(f"Decision node '{nid}' points to non-existent target '{target}'.")
            else:
                target = node.get('next')
                if not target:
                    errors.append(f"Node '{nid}' of type '{ntype}' is missing a 'next' target.")
                elif target not in node_ids:
                    errors.append(f"Node '{nid}' points to non-existent target '{target}'.")

        # 3. Check for interpolation consistency
        text = node.get('text', '')
        import re
        placeholders = re.findall(r'\{(\w+)\.(\w+)\}', text)
        for p_node, p_prop in placeholders:
            if p_node not in node_ids and p_node not in ['axis1', 'axis2', 'axis3']:
                errors.append(f"Node '{nid}' contains interpolation for non-existent node '{p_node}'.")

    # 4. Check for orphaned nodes (unreachable from START)
    reachable = set()
    def walk(node_id):
        if node_id in reachable: return
        reachable.add(node_id)
        node = next((n for n in nodes if n['id'] == node_id), None)
        if not node: return
        
        if node['type'] == 'decision':
            for cond in node['logic']['conditions']:
                walk(cond['then'])
        elif 'next' in node and node['next']:
            walk(node['next'])

    walk('START')
    orphans = node_ids - reachable
    if orphans:
        warnings.append(f"Orphaned nodes (unreachable from START): {orphans}")

    # Results
    if errors:
        print("\n❌ ERRORS FOUND:")
        for err in errors: print(f"  - {err}")
    else:
        print("\n✅ NO STRUCTURAL ERRORS")

    if warnings:
        print("\n⚠️ WARNINGS:")
        for warn in warnings: print(f"  - {warn}")

    print("\n--- Validation Complete ---")
    return len(errors) == 0

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), 'reflection-tree.json')
    success = validate_tree(path)
    sys.exit(0 if success else 1)
