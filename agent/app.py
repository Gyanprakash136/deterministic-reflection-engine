import streamlit as st
import json
import os


def apply_custom_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Inter:wght@400;500;700&display=swap');
    
    .stApp {
        background-color: #0f172a;
        background-image: 
            radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.1) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(251, 191, 36, 0.05) 0px, transparent 50%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    .main-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 3rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin: 2rem 0;
    }
    
    h1 {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        text-align: center;
    }
    
    .node-text {
        font-size: 1.25rem;
        line-height: 1.6;
        color: #94a3b8;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .stButton>button {
        width: 100%;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        color: #f8fafc;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: rgba(16, 185, 129, 0.1);
        border-color: #10b981;
        transform: scale(1.02);
    }
    
    .progress-bar-container {
        width: 100%;
        height: 6px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        margin-bottom: 2rem;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: #10b981;
        border-radius: 3px;
        transition: width 0.5s ease;
    }
    
    .summary-card {
        background: rgba(0, 0, 0, 0.2);
        padding: 2rem;
        border-radius: 16px;
        border-left: 4px solid #fbbf24;
    }
    
    .summary-label {
        color: #fbbf24;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def load_tree():
    path = os.path.join(os.path.dirname(__file__), '..', 'tree', 'reflection-tree.json')
    with open(path, 'r') as f:
        return json.load(f)

def interpolate(text, tree_data, state):
    if not text: return ""
    
   
    import re
    def replace_node(match):
        node_id, property = match.groups()
        answer = state['answers'].get(node_id)
        if not answer: return match.group(0)
        return answer.get(property, match.group(0))
    
    text = re.sub(r'\{(\w+)\.(\w+)\}', replace_node, text)
    
    # Interpolate axis dominance
    def replace_axis(match):
        axis_num = match.group(1)
        axis = state[f'axis{axis_num}']
        keys = list(axis.keys())
        return keys[0] if axis[keys[0]] >= axis[keys[1]] else keys[1]
    
    text = re.sub(r'\{axis(\d)\.dominant\}', replace_axis, text)
    return text

def evaluate_logic(logic, state):
    import re
    for condition in logic['conditions']:
        if condition['if'] == 'true':
            return condition['then']
        
        expr = condition['if']
        
        expr = expr.replace('||', ' or ').replace('&&', ' and ')
        
        
        expr = re.sub(r'state\.axis(\d)\.(\w+)', lambda m: str(state[f'axis{m.group(1)}'][m.group(2)]), expr)

        expr = re.sub(r'(\w+)\.value', lambda m: f"'{state['answers'].get(m.group(1), {}).get('value', '')}'", expr)
        expr = re.sub(r'(\w+)\.text', lambda m: f"'{state['answers'].get(m.group(1), {}).get('text', '')}'", expr)
        
        try:
            if eval(expr):
                return condition['then']
        except Exception as e:
            st.error(f"Logic Error: {e} | Expr: {expr}")
    return None

def main():
    st.set_page_config(page_title="The Daily Reflection Tree", layout="centered")
    apply_custom_styles()
    
    tree_data = load_tree()
    nodes = tree_data['nodes']
    
    if 'current_node_id' not in st.session_state:
        st.session_state.current_node_id = 'START'
        st.session_state.state = {
            'answers': {},
            'axis1': {'internal': 0, 'external': 0},
            'axis2': {'contribution': 0, 'entitlement': 0},
            'axis3': {'self': 0, 'altro': 0}
        }

    current_node = next((n for n in nodes if n['id'] == st.session_state.current_node_id), None)
    
    if not current_node:
        st.error(f"Node {st.session_state.current_node_id} not found.")
        return


    if current_node['type'] == 'decision':
        next_id = evaluate_logic(current_node['logic'], st.session_state.state)
        st.session_state.current_node_id = next_id
        st.rerun()


    node_index = next((i for i, n in enumerate(nodes) if n['id'] == st.session_state.current_node_id), 0)
    progress = (node_index + 1) / len(nodes)
    st.markdown(f"""
    <div class="progress-bar-container">
        <div class="progress-bar-fill" style="width: {progress*100}%"></div>
    </div>
    """, unsafe_allow_html=True)

    # Logo handling with base64 for reliability
    import base64
    logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            logo_html = f'<img src="data:image/png;base64,{data}" style="width: 80px; filter: drop-shadow(0 0 10px rgba(16, 185, 129, 0.5));" />'
    else:
        logo_html = '<img src="https://img.icons8.com/color/96/tree--v1.png" style="width: 80px;" />'

    st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
            {logo_html}
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<h1>The Daily Reflection Tree</h1>", unsafe_allow_html=True)
    

    with st.container():
        st.markdown(f'<div class="node-text">{interpolate(current_node["text"], tree_data, st.session_state.state)}</div>', unsafe_allow_html=True)
        
        if current_node['type'] == 'question':
            cols = st.columns(2) if len(current_node['options']) > 2 else [st.container()]
            for i, option in enumerate(current_node['options']):
                col = cols[i % len(cols)]
                if col.button(option['text'], key=f"opt_{i}"):

                    st.session_state.state['answers'][current_node['id']] = {'text': option['text'], 'value': option['value']}
                    if 'signal' in option:
                        axis, pole = option['signal'].split(':')
                        st.session_state.state[axis][pole] += 1
                    
                    st.session_state.current_node_id = current_node['next']
                    st.rerun()
        
        elif current_node['type'] in ['start', 'bridge', 'reflection']:
            if st.button("Continue" if current_node['type'] == 'reflection' else "Begin" if current_node['type'] == 'start' else "Next Axis"):
                st.session_state.current_node_id = current_node['next']
                st.rerun()
                
        elif current_node['type'] == 'summary':
            st.markdown('<div class="summary-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="summary-label">Axis 1: Locus of Control</div>', unsafe_allow_html=True)
            st.markdown(f'<div>You operated with an <b>{interpolate("{axis1.dominant}", tree_data, st.session_state.state)}</b> locus today.</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="summary-label" style="margin-top:1rem">Axis 2: Orientation</div>', unsafe_allow_html=True)
            st.markdown(f'<div>Your primary mode was <b>{interpolate("{axis2.dominant}", tree_data, st.session_state.state)}</b>.</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="summary-label" style="margin-top:1rem">Axis 3: Radius of Concern</div>', unsafe_allow_html=True)
            st.markdown(f'<div>You maintained a <b>{interpolate("{axis3.dominant}", tree_data, st.session_state.state)}</b> radius.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Finish Session"):
                st.session_state.current_node_id = current_node['next']
                st.rerun()
                
        elif current_node['type'] == 'end':
            if st.button("Start New Reflection"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()

if __name__ == "__main__":
    main()
