# GeneHomology

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

🧬 A Python command-line tool for calculating BLAST homology between cross-species gene and protein sequences

## ✨ Features

- 🔍 **BLAST Homology Calculation** - Calculate BLAST homology scores between cross-species gene and protein sequences
- ⚡ **High-Performance Sequence Alignment** - Support local BLAST+ for gene and protein sequence alignment
- 📊 **Detailed Analysis Reports** - Generate structured alignment results and statistical information
- 📁 **Batch Processing Support** - Support single gene, multiple gene lists, or file input
- 🛠️ **Smart Path Detection** - Automatically detect BLAST+ installation path in the system
- 📝 **Clean Output Format** - Automatically filter redundant information from BLAST results

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- BLAST+ toolkit (required for local sequence alignment)
  - BLAST+ version 2.10.0 or higher recommended
  - Must include `blastp` and `blastn` executables

### BLAST+ Installation

**macOS (Homebrew):**
```bash
brew install blast
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ncbi-blast+
```

**Windows:**
1. Download pre-compiled package from NCBI:
   - Visit: https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/
   - Download: `ncbi-blast-2.16.0+-x64-win64.zip`
2. Extract the zip file
3. Add the extracted folder to your system PATH environment variable
4. Open Command Prompt or PowerShell and verify:
   ```bash
   blastn -version
   ```

**Using conda (Cross-platform):**
```bash
conda install -c bioconda blast
```

**Verify BLAST+ Installation:**
```bash
# Check if BLAST+ is properly installed
which blastp
which blastn

# Test BLAST+ functionality
blastp -version
blastn -version
```
### Installation genehomology

```bash
# Install from source
git clone https://github.com/JingGuo1997/genehomology.git
cd genehomology
pip install -e .
```

### Verify Installation

After installation, verify that both GeneHomology is properly installed:

```bash
# Check GeneHomology installation
genehomology --help

# Test a simple gene homology query
genehomology --speciesQuery homo_sapiens --speciesTarget mus_musculus --gene TBXT --type protein
```

### Basic Usage

```bash
# Compare TBXT gene between human and mouse
genehomology --speciesQuery homo_sapiens --speciesTarget mus_musculus --gene TBXT --type protein

# Batch comparison of multiple genes
genehomology --speciesQuery homo_sapiens --speciesTarget mus_musculus --gene "TBXT,PAX6,BRCA1" --type ALL

# Read gene list from file
genehomology --speciesQuery homo_sapiens --speciesTarget mus_musculus --gene genes.txt --type gene
```

## 📖 Detailed Documentation

### Command Line Arguments

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--speciesQuery` | ✅ | Source species Latin name | `homo_sapiens` |
| `--speciesTarget` | ✅ | Target species Latin name | `mus_musculus` |
| `--gene` | ✅ | Gene symbol | `TBXT` or `TBXT,PAX6` or `genes.txt` |
| `--type` | ✅ | Alignment type | `gene`, `protein`, `ALL` |

### Supported Species

This tool supports all species in the Ensembl database, common species include:

- `homo_sapiens` (Human)
- `mus_musculus` (Mouse)
- `rattus_norvegicus` (Rat)
- `danio_rerio` (Zebrafish)
- `drosophila_melanogaster` (Fruit fly)
- `caenorhabditis_elegans` (Nematode)

### Output File Example

The program generates independent `.out` files for each gene:

```
============================================================
Gene: TBXT
------------------------------------------------------------
Function Description: T-box transcription factor T [Source:HGNC Symbol;Acc:HGNC:11515]
Homology Type: ortholog_one2one
homo_sapiens Gene ID: ENSG00000164458
mus_musculus Gene ID: ENSMUSG00000062327
[homo_sapiens] Protein Sequence Length: 436
[mus_musculus] Protein Sequence Length: 436

[Protein Sequence BLAST Alignment Results]
... BLAST result details ...
```

## 🤝 Contributing

We welcome all forms of contributions!

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- 🐛 [Report Bug](https://github.com/JingGuo1997/genehomology/issues)
- 💡 [Request Feature](https://github.com/JingGuo1997/genehomology/issues)
- 📖 [Documentation](https://github.com/JingGuo1997/genehomology/wiki)

## ⭐ If this project helps you, please give us a star! 
