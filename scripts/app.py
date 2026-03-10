import streamlit as st
import pandas as pd
import joblib
import os
import requests
import py3Dmol
import streamlit.components.v1 as components
# app.py
import predict_new_sequences
import predict_new_sequences
import base64
import os
# -----------------------------
# Helper function: Set background image
# -----------------------------
def set_background(image_path):
    """
    Set a background image for Streamlit app.
    """
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            encoded = f.read()
        b64_encoded = base64.b64encode(encoded).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{b64_encoded}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(f"Background image '{image_path}' not found.")

# -----------------------------
# Call the helper function here
# -----------------------------
# Replace "assets/background.jpg" with your actual image path
set_background("assets/background.jpeg")

# -----------------------------
# Function to set background image
# -----------------------------
def set_background(image_path):
    """
    Set a background image for Streamlit app.
    """
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            encoded = f.read()
        b64_encoded = base64.b64encode(encoded).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{b64_encoded}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(f"Background image {image_path} not found.")

# -----------------------------
# Helper function to render PDB
# -----------------------------
def render_pdb(pdb_id):
    """Download PDB file and render in Streamlit using py3Dmol"""
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    r = requests.get(url)
    if r.status_code == 200:
        pdb_block = r.text
        viewer = py3Dmol.view(width=800, height=500)
        viewer.addModel(pdb_block, "pdb")
        viewer.setStyle({"cartoon": {"color": "spectrum"}})
        viewer.zoomTo()
        viewer_html = viewer._make_html()
        components.html(viewer_html, height=500, width=800)
    else:
        st.error(f"Could not fetch PDB structure {pdb_id}")

# -----------------------------
# Manual PDB mapping for test species
# -----------------------------
manual_pdb_mapping = {
    "Flavipsychrobacter stenotrophus": "6G5Q",
    "Mixta intestinalis": "4YAJ",
    "Siccibacter colletis": "1BNA"
}

# -----------------------------
# Streamlit page setup
# -----------------------------
#st.set_page_config(page_title="eDNA Explorer", layout="wide")
#st.title("CodeBlooded.AI")
st.set_page_config(page_title="eDNA Explorer", layout="wide")

# Center the title using Markdown + HTML
st.markdown(
    "<h1 style='text-align: center;'>CodeBlooded.AI – AI Pipeline for eDNA Taxonomy & Biodiversity Exploration</h1>",
    unsafe_allow_html=True
)



tab1, tab2, tab3, tab4 = st.tabs([
    "Existing Results",
    "Predict New Sequences",
    "Model Info",
    "3D Molecular Structures"
])

# -----------------------------
# Tab 1: Existing BLAST Results
# -----------------------------
with tab1:
    st.header("Existing BLAST Results")
    try:
        df = pd.read_csv("results/blast_hits_parsed.csv")
        st.dataframe(df)
        st.download_button("Download Results", "results/blast_hits_parsed.csv")
    except:
        st.warning("No existing BLAST results found. Run the pipeline first.")

# -----------------------------
# Tab 2: Predict New Sequences
# -----------------------------
with tab2:
    st.header("Predict New Sequences")
    uploaded_file = st.file_uploader("Upload FASTA/FASTQ file", type=['fasta','fastq','fa','fq'])

    if uploaded_file is not None:
        os.makedirs("raw_data", exist_ok=True)
        temp_path = os.path.join("raw_data", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("Predict Taxonomy"):
            with st.spinner("Running prediction..."):
                try:
                    # Import function
                    from predict_new_sequences import predict_new_sequences

                    # Run prediction
                    #results = predict_new_sequences(temp_path, "results/new_predictions.csv")
                    results = predict_new_sequences(temp_path, "results/new_predictions.csv")

                    if results.empty:
                        st.warning("No hits found for uploaded sequences.")
                    else:
                        # Assign manual PDB IDs if missing
                        results['pdb_id'] = results.apply(
                            lambda row: row['pdb_id'] if row['pdb_id'] else manual_pdb_mapping.get(row['predicted_species']),
                            axis=1
                        )

                        st.success("Prediction completed!")
                        st.dataframe(results[['sequence_id','predicted_species','pdb_id']])
                        #st.dataframe(results[['qseqid','predicted_taxid','predicted_species','pdb_id']])
                        #st.download_button(
                        #    "Download Predictions",
                        #    "results/new_predictions.csv",
                        #    "taxonomy_predictions.csv"
                        #)
                        st.download_button(
                            "Download Predictions",
                            "results/new_predictions.csv",
                            "taxonomy_predictions.csv"
                    )

                        # Save results in session for Tab 4
                        st.session_state['prediction_results'] = results

                except Exception as e:
                    st.error(f"Prediction failed: {e}")
# -----------------------------
# Tab 3: Model & Pipeline Information
# -----------------------------
with tab3:
    st.header("Model & Pipeline Information")
    
    # -----------------------------
    # Model Details & Statistics
    # -----------------------------
    try:
        model = joblib.load("models/rf_model.pkl")
        st.subheader("Trained Model Details & Statistics")
        st.write(f"- **Model type:** Random Forest")
        st.write(f"- **Number of trees:** {model.n_estimators}")
        st.write(f"- **Number of classes trained:** {len(model.classes_)}")

    except Exception as e:
        st.warning(f"No trained model found or failed to load. Error: {e}")
    
    # -----------------------------
    # Short Pipeline/System Description
    # -----------------------------
    st.subheader("eDNA Classification Pipeline Overview")
    
    pipeline_short = """
    The eDNA Explorer system classifies environmental DNA sequences to predict species 
    and provide molecular insights. It accepts FASTA/FASTQ sequences, performs taxonomy 
    prediction using a Random Forest model, optionally integrates BLAST searches, 
    visualizes 3D molecular structures, and displays curated species information.
    """
    
    st.markdown(pipeline_short)

# -----------------------------
# Helper function to fetch PDB info
# -----------------------------
def fetch_pdb_info(pdb_id):
    """Fetch PDB metadata including description/title, method, and taxonomy for a given PDB ID"""
    import requests
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Description / Title
        description = data.get("rcsb_entry_info", {}).get("description")
        if not description:
            description = data.get("struct", {}).get("title", "No description available.")
        # Experimental Method
        exptl = data.get("exptl", [])
        method = exptl[0].get("method") if exptl else "Unknown"
        # Taxonomy info
        tax_info = []
        orgs = data.get("rcsb_entity_source_organism", [])
        for org in orgs:
            org_name = org.get("scientific_name", "Unknown")
            family = org.get("family", "Unknown")
            genus = org.get("genus", "Unknown")
            species = org.get("species", "Unknown")
            tax_info.append({
                "scientific_name": org_name,
                "family": family,
                "genus": genus,
                "species": species
            })
        return description, method, tax_info
    else:
        return "Failed to fetch info", "Unknown", []
# -----------------------------
# Required imports
# -----------------------------
import requests
from Bio import Entrez
import streamlit as st

Entrez.email = "nabhjain8015@gmail.com"  # NCBI requires an email

# -----------------------------
# Helper function: Fetch PDB metadata
# -----------------------------
def fetch_pdb_info(pdb_id):
    """Fetch PDB metadata including description/title, method, and taxonomy"""
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        description = data.get("rcsb_entry_info", {}).get("description") or data.get("struct", {}).get("title", "No description available.")
        exptl = data.get("exptl", [])
        method = exptl[0].get("method") if exptl else "Unknown"
        tax_info = []
        orgs = data.get("rcsb_entity_source_organism", [])
        for org in orgs:
            org_name = org.get("scientific_name", "Unknown")
            family = org.get("family", "Unknown")
            genus = org.get("genus", "Unknown")
            species = org.get("species", "Unknown")
            tax_info.append({
                "scientific_name": org_name,
                "family": family,
                "genus": genus,
                "species": species
            })
        return description, method, tax_info
    else:
        return "Failed to fetch info", "Unknown", []

# -----------------------------
# Helper function: Fetch NCBI lineage via Entrez
# -----------------------------
def fetch_ncbi_lineage(scientific_name):
    try:
        handle = Entrez.esearch(db="taxonomy", term=scientific_name)
        record = Entrez.read(handle)
        if record["IdList"]:
            taxid = record["IdList"][0]
            handle2 = Entrez.efetch(db="taxonomy", id=taxid, retmode="xml")
            data = Entrez.read(handle2)[0]
            
            lineage_dict = {rank: "Unknown" for rank in ["superkingdom","phylum","class","order","family","genus","species"]}
            lineage_dict["species"] = data.get("ScientificName", "Unknown")
            
            for lineage_item in data.get("LineageEx", []):
                rank = lineage_item.get("Rank")
                name = lineage_item.get("ScientificName")
                if rank in lineage_dict:
                    lineage_dict[rank] = name
            return lineage_dict
        else:
            return {rank: "Unknown" for rank in ["superkingdom","phylum","class","order","family","genus","species"]}
    except:
        return {rank: "Unknown" for rank in ["superkingdom","phylum","class","order","family","genus","species"]}

# -----------------------------
# Helper function: Fetch environmental info from BacDive
# -----------------------------
def fetch_bacdive_info(scientific_name, api_key="YOUR_BACDIVE_API_KEY"):
    headers = {"Accept": "application/json", "X-API-KEY": api_key}
    url = f"https://bacdive.dsmz.de/api/bacdive/taxonomy/{scientific_name}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            temp = data.get("temperature_range", "Unknown")
            pH = data.get("pH_range", "Unknown")
            habitat = data.get("habitat", "Unknown")
            pathogenicity = data.get("pathogenicity", "Unknown")
            return temp, pH, habitat, pathogenicity
        else:
            return "Unknown", "Unknown", "Unknown", "Unknown"
    except:
        return "Unknown", "Unknown", "Unknown", "Unknown"

# -----------------------------
# Helper function: Classify temperature
# -----------------------------
def classify_temperature(temp):
    try:
        temp = float(temp)
        if temp < 15: return "Psychrophile"
        elif 15 <= temp < 20: return "Psychrotolerant"
        elif 20 <= temp <= 45: return "Mesophile"
        elif 45 < temp <= 80: return "Thermophile"
        else: return "Hyperthermophile"
    except:
        return "Unknown"
# -----------------------------
# Manual species descriptions (detailed)
# -----------------------------
species_descriptions = {
    "Flavipsychrobacter stenotrophus": (
        "**General Description:** Flavipsychrobacter stenotrophus is a psychrophilic "
        "marine bacterium isolated from cold and nutrient-limited environments, "
        "particularly in polar and deep-sea ecosystems. It belongs to the family "
        "Flavobacteriaceae and is adapted to low-temperature survival with diverse "
        "metabolic capabilities.\n\n"
        "**Taxonomy:** Domain: Bacteria | Phylum: Bacteroidota | Class: Flavobacteriia | "
        "Order: Flavobacteriales | Family: Flavobacteriaceae.\n\n"
        "**Morphology & Physiology:** Gram-negative, rod-shaped, aerobic; adapted to cold "
        "environments with enzymes optimized for low-temperature catalysis.\n\n"
        "**Ecology & Habitat:** Frequently found in polar oceans, marine sediments, and "
        "other cold aquatic ecosystems; contributes to nutrient recycling in oligotrophic "
        "conditions.\n\n"
        "**Relevance:** Studied for cold-active enzymes with potential in biotechnology, "
        "including food processing, bioremediation in cold regions, and enzymatic industries."
    ),

    "Mixta intestinalis": (
        "**General Description:** Mixta intestinalis is a facultatively anaerobic, "
        "Gram-negative bacterium belonging to the family Enterobacteriaceae. It is "
        "part of the gut microbiota in humans and animals, with potential roles in "
        "digestion, but can also act as an opportunistic pathogen.\n\n"
        "**Taxonomy:** Domain: Bacteria | Phylum: Pseudomonadota | Class: Gammaproteobacteria | "
        "Order: Enterobacterales | Family: Enterobacteriaceae.\n\n"
        "**Morphology & Physiology:** Rod-shaped, motile with peritrichous flagella, "
        "facultatively anaerobic, capable of fermenting a wide range of carbohydrates.\n\n"
        "**Ecology & Habitat:** Commonly isolated from intestinal tracts of mammals, "
        "soil, water, and occasionally clinical samples; interacts within gut microbial communities.\n\n"
        "**Relevance:** Important for understanding gut ecology and host–microbe interactions; "
        "studied for antimicrobial resistance and its role in opportunistic infections."
    ),

    "Siccibacter colletis": (
        "**General Description:** Siccibacter colletis is a Gram-negative bacterium "
        "in the family Enterobacteriaceae, frequently associated with plants, "
        "soil, and environmental niches. It has been studied for plant-microbe "
        "interactions and possible beneficial or pathogenic roles.\n\n"
        "**Taxonomy:** Domain: Bacteria | Phylum: Pseudomonadota | Class: Gammaproteobacteria | "
        "Order: Enterobacterales | Family: Enterobacteriaceae.\n\n"
        "**Morphology & Physiology:** Rod-shaped, facultatively anaerobic, oxidase-negative, "
        "and catalase-positive; capable of adapting to both plant and environmental niches.\n\n"
        "**Ecology & Habitat:** Found in association with crops and plant rhizospheres, "
        "also isolated from soil and water environments.\n\n"
        "**Relevance:** Studied for potential applications in agriculture, including "
        "plant growth promotion and biocontrol; its exact role (beneficial vs. opportunistic) "
        "remains under research."
    )
}
# -----------------------------
# Tab 4: 3D Molecular Visualization & Biological Info
# -----------------------------
with tab4:
    st.header("3D Molecular Structures & Species Description")

    if 'prediction_results' in st.session_state:
        results = st.session_state['prediction_results']
        predicted_species = results['predicted_species'].unique()
        selected_species = st.selectbox("Select predicted species:", predicted_species)

        if selected_species:
            # Get PDB IDs for species
            pdb_ids = results[results['predicted_species'] == selected_species]['pdb_id'].dropna().unique()
            if len(pdb_ids) == 0:
                st.warning(f"No PDB structures found for {selected_species}")
            else:
                for pdb_id in pdb_ids:
                    with st.container():
                        st.markdown(f"### PDB: {pdb_id}")
                        st.markdown(f"**Species:** {selected_species}")

                        # Render 3D structure
                        render_pdb(pdb_id)

                        # -----------------------------
                        # Show only manually added description
                        # -----------------------------
                        if selected_species in species_descriptions:
                            st.markdown("**About this species:**")
                            st.info(species_descriptions[selected_species])
    else:
        st.info("Predict sequences first to visualize 3D molecular structures.")
