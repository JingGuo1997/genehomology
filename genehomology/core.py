import requests
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os
import subprocess
import shutil
import tempfile

ENSEMBL_SERVER = "https://rest.ensembl.org"
HEADERS = {"Content-Type": "application/json"}

# 0. Get gene description information
def get_gene_description(symbol: str, species: str):
    """
    Given gene symbol and species, get description information
    """
    url = f"{ENSEMBL_SERVER}/lookup/symbol/{species}/{symbol}?content-type=application/json"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("description")
    except Exception as e:
        print(f"Failed to get description information: {e}")
        return None

# 1. Get homologous gene information, supports homology type selection
def get_homologues(symbol: str, species1: str, species2: str):
    """
    Find homologous genes between two species and return gene ID and protein ID information
    
    Parameters:
        symbol (str): Gene symbol, e.g., 'TBXT'
        species1 (str): Source species Latin name, e.g., 'homo_sapiens'
        species2 (str): Target species Latin name, e.g., 'mus_musculus'
    
    Returns:
        dict: Dictionary containing gene ID and protein ID information for both species
    """
    ext = f"/homology/symbol/{species1}/{symbol}?target_species={species2}&type=orthologues&format=full"
    
    try:
        resp = requests.get(ENSEMBL_SERVER + ext, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        # Check if homologous gene data exists
        if not data.get("data") or not data["data"][0].get("homologies"):
            return None
        
        # Extract homologous gene information
        homology = data["data"][0]["homologies"][0]  # Get the first homology relationship
        source = homology["source"]
        target = homology["target"]
        
        result = {
            "type":homology["type"],
            "source_species": {
                "species": source["species"],
                "gene_id": source["id"],
                "protein_id": source["protein_id"]
            },
            "target_species": {
                "species": target["species"],
                "gene_id": target["id"],
                "protein_id": target["protein_id"]
            }
        }
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    
# 2. Get gene/protein sequence
def get_sequence(id_type: str, id_value: str):
    """
    Get sequence information for Ensembl gene or protein

    Parameters:
        id_type (str): 'gene', 'protein', or 'ALL'
        id_value (str): Ensembl ID
    Returns:
        str or dict: Sequence string, or {'gene': ..., 'protein': ...}
    """
    if id_type == "gene":
        url = f"{ENSEMBL_SERVER}/lookup/id/{id_value}?expand=1"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            transcripts = data.get("Transcript", [])
            if not transcripts:
                print("No transcript information found")
                return None
            transcripts = sorted(transcripts, key=lambda t: t.get("end", 0) - t.get("start", 0), reverse=True)
            longest_transcript_id = transcripts[0]["id"]
            seq_url = f"{ENSEMBL_SERVER}/sequence/id/{longest_transcript_id}?type=cdna"
            seq_resp = requests.get(seq_url, headers=HEADERS, timeout=15)
            seq_resp.raise_for_status()
            return seq_resp.json().get("seq")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
    elif id_type == "protein":
        ext = f"/sequence/id/{id_value}?type=protein"
        try:
            resp = requests.get(ENSEMBL_SERVER + ext, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            return resp.json().get("seq")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
    else:
        raise ValueError("ValueError")

def find_blast_executable(program):
    """
    Find the executable path for BLAST program
    """
    # Common BLAST installation paths
    common_paths = [
        f"/opt/homebrew/bin/{program}",  # macOS Homebrew
        f"/usr/local/bin/{program}",     # General local installation
        f"/usr/bin/{program}",           # System installation
        f"/opt/blast/bin/{program}"      # BLAST official installation path
    ]
    
    # First try to find using which command
    try:
        result = subprocess.run(['which', program], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except:
        pass
    
    # Then check common paths
    for path in common_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    
    # Finally try to use program name directly (assuming it's in PATH)
    return program

# 3. BLAST alignment
def run_local_blast(seq1, seq2, seq1_id, seq2_id, type):
    """
    Perform local BLAST alignment on two sequences
    
    Parameters:
        seq1 (str or dict): First sequence or sequence dictionary
        seq2 (str or dict): Second sequence or sequence dictionary
        seq1_id (str): ID of the first sequence
        seq2_id (str): ID of the second sequence
        type (str): Alignment type, 'gene', 'protein'
    Returns:
        str or dict: BLAST result string, or {'gene': ..., 'protein': ...}
    """
    if type == "ALL":
        result = {}
        result['protein'] = run_local_blast(seq1['protein'], seq2['protein'], seq1_id, seq2_id, "protein")
        result['gene'] = run_local_blast(seq1['gene'], seq2['gene'], seq1_id, seq2_id, "gene")
        return result

    # Use temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        query_file = os.path.join(temp_dir, f"query_{seq1_id}_{type}.fasta")
        subject_file = os.path.join(temp_dir, f"subject_{seq2_id}_{type}.fasta")
        
        try:
            # Create sequence files
            seq1_record = SeqRecord(Seq(seq1), id=seq1_id, description="query sequence")
            seq2_record = SeqRecord(Seq(seq2), id=seq2_id, description="subject sequence")
            SeqIO.write(seq1_record, query_file, "fasta")
            SeqIO.write(seq2_record, subject_file, "fasta")
            
            # Build BLAST command
            if type == "protein":
                blast_cmd = find_blast_executable("blastp")
            elif type == "gene":
                blast_cmd = find_blast_executable("blastn")
            else:
                raise ValueError(f"Unsupported alignment type: {type}")
            
            # Run BLAST command
            cmd = [
                blast_cmd,
                "-query", query_file,
                "-subject", subject_file,
                "-outfmt", "0",
                "-evalue", "0.001",
                "-num_threads", "4"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(result.stdout)
                return result.stdout
            else:
                error_msg = f"BLAST alignment failed: {result.stderr}"
                print(error_msg)
                return error_msg
        
        except FileNotFoundError:
            error_msg = f"BLAST program not found: {blast_cmd}. Please ensure BLAST+ is installed"
            print(error_msg)
            return error_msg
        except subprocess.TimeoutExpired:
            error_msg = "BLAST alignment timeout"
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"BLAST alignment failed: {e}"
            print(error_msg)
            return error_msg 