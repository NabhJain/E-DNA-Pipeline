import streamlit as st
import streamlit.components.v1 as components

def get_pdb_for_taxid(taxid):
    """Return a list of PDB IDs for a given TaxID (or a default)."""
    mapping = {
        '511145': ['1ECL','1ECO','2E2M'],  # E. coli
        '9606': ['1HHO','1AON'],           # Homo sapiens
        '10090': ['1MBO','1MSM'],          # Mus musculus
        '559292': ['1YEA','2YEA']          # S. cerevisiae
    }
    return mapping.get(str(taxid), ['1CRN'])

def display_3d_structure(pdb_id):
    """Embed 3Dmol.js viewer in Streamlit."""
    pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    html = f"""
    <div id="container" style="width: 100%; height: 600px;"></div>
    <script src="https://3Dmol.csb.pitt.edu/build/3Dmol-min.js"></script>
    <script>
    var element = document.getElementById("container");
    var viewer = $3Dmol.createViewer(element, {{backgroundColor: "white"}});
    $.get("{pdb_url}", function(data) {{
        viewer.addModel(data, "pdb");
        viewer.setStyle({{}}, {{cartoon: {{color: "spectrum"}}}});
        viewer.zoomTo();
        viewer.render();
    }});
    </script>
    """
    components.html(html, height=650)
