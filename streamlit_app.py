import streamlit as st
import os
from genehomology.cli import GeneHomologyCLI

st.title("genehomology:Batch Cross-species Homologous Gene and Protein Sequence Alignment Tool")

st.markdown("""
本工具支持批量跨物种基因/蛋白序列同源性比对。
""")

species_list = [
    "homo_sapiens", "mus_musculus", "macaca_fascicularis", "rattus_norvegicus",
    "danio_rerio", "drosophila_melanogaster", "caenorhabditis_elegans", "custom"
]

# 源物种
species_query_sel = st.selectbox("Source species", species_list, index=0)
if species_query_sel == "custom":
    species_query = st.text_input("Custom source species (e.g. gallus_gallus)", key="custom_query")
else:
    species_query = species_query_sel

# 目标物种
species_target_sel = st.selectbox("Target species", species_list, index=1)
if species_target_sel == "custom":
    species_target = st.text_input("Custom target species (e.g. xenopus_tropicalis)", key="custom_target")
else:
    species_target = species_target_sel

gene = st.text_area("Gene symbol（comma separated, or upload file）")
compare_type = st.selectbox("Compare type", ["gene", "protein", "ALL"])

gene_file = st.file_uploader("Upload gene list file（txt, one gene per line）", type=["txt"])

if st.button("Start Running"):
    if gene_file is not None:
        # 保存上传的文件
        with open("uploaded_genes.txt", "wb") as f:
            f.write(gene_file.read())
        gene_input = "uploaded_genes.txt"
    else:
        gene_input = gene.strip()
    if not (species_query and species_target and gene_input and compare_type):
        st.error("Please fill in all parameters!")
    else:
        with st.spinner("Calculating... Please wait"):
            cli = GeneHomologyCLI(species_query, species_target, gene_input, compare_type)
            cli.run()
        st.success("Alignment completed!")
        # 提供结果文件下载链接
        out_files = [f for f in os.listdir() if f.endswith('.out')]
        for out_file in out_files:
            with open(out_file, "rb") as f:
                st.download_button(
                    label=f"下载 {out_file}",
                    data=f,
                    file_name=out_file,
                    mime="text/plain"
                )