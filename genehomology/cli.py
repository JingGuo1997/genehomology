import argparse
import os
from .core import get_gene_description, get_homologues, get_sequence, run_local_blast
from .utils import filter_blast_reference

class GeneHomologyCLI:
    def __init__(self, species_query, species_target, gene_input, compare_type):
        self.species_query = species_query
        self.species_target = species_target
        self.compare_type = compare_type
        self.gene_list = self.parse_gene_input(gene_input)

    def parse_gene_input(self, gene_input):
        # If it's a file path, read the file
        if os.path.isfile(gene_input):
            with open(gene_input, 'r') as f:
                genes = [line.strip() for line in f if line.strip()]
        else:
            # Comma-separated string
            genes = [g.strip() for g in gene_input.split(',') if g.strip()]
        return genes

    def run(self):
        for idx, gene in enumerate(self.gene_list, 1):
            output_lines = []
            output_lines.append("=" * 60)
            output_lines.append(f"Gene: {gene}")
            output_lines.append("-" * 60)
            description = get_gene_description(gene, self.species_query)
            output_lines.append(f"Function Description: {description if description else 'None'}")

            result = get_homologues(gene, self.species_query, self.species_target)
            if not result:
                output_lines.append("No homologous gene information found\n")
                with open(f"{gene}.out", "w", encoding="utf-8") as f:
                    f.write('\n'.join(output_lines))
                continue

            output_lines.append(f"Homology Type: {result['type']}")
            output_lines.append(f"{self.species_query} Gene ID: {result['source_species']['gene_id']}")
            output_lines.append(f"{self.species_target} Gene ID: {result['target_species']['gene_id']}")

            gene_seq1 = get_sequence("gene", result['source_species']['gene_id'])
            gene_seq2 = get_sequence("gene", result['target_species']['gene_id'])
            protein_seq1 = get_sequence("protein", result['source_species']['protein_id'])
            protein_seq2 = get_sequence("protein", result['target_species']['protein_id'])

            if self.compare_type == "ALL":
                output_lines.append(f"\n[{self.species_query}] Longest Transcript Length: {len(gene_seq1) if gene_seq1 else 'N/A'}")
                output_lines.append(f"[{self.species_target}] Longest Transcript Length: {len(gene_seq2) if gene_seq2 else 'N/A'}")
                output_lines.append(f"[{self.species_query}] Protein Sequence Length: {len(protein_seq1) if protein_seq1 else 'N/A'}")
                output_lines.append(f"[{self.species_target}] Protein Sequence Length: {len(protein_seq2) if protein_seq2 else 'N/A'}")
                if protein_seq1 and protein_seq2:
                    output_lines.append("\n[Protein Sequence BLAST Alignment Results]")
                    blast_result = run_local_blast(protein_seq1, protein_seq2, result['source_species']['protein_id'], result['target_species']['protein_id'], "protein")
                    output_lines.append(filter_blast_reference(str(blast_result)))
                if gene_seq1 and gene_seq2:
                    output_lines.append("\n[Longest Transcript Sequence BLAST Alignment Results]")
                    blast_result = run_local_blast(gene_seq1, gene_seq2, result['source_species']['gene_id'], result['target_species']['gene_id'], "gene")
                    output_lines.append(filter_blast_reference(str(blast_result)))
            elif self.compare_type == "protein":
                output_lines.append(f"[{self.species_query}] Protein Sequence Length: {len(protein_seq1) if protein_seq1 else 'N/A'}")
                output_lines.append(f"[{self.species_target}] Protein Sequence Length: {len(protein_seq2) if protein_seq2 else 'N/A'}")
                if protein_seq1 and protein_seq2:
                    output_lines.append("\n[Protein Sequence BLAST Alignment Results]")
                    blast_result = run_local_blast(protein_seq1, protein_seq2, result['source_species']['protein_id'], result['target_species']['protein_id'], "protein")
                    output_lines.append(filter_blast_reference(str(blast_result)))
            elif self.compare_type == "gene":
                output_lines.append(f"[{self.species_query}] Longest Transcript Length: {len(gene_seq1) if gene_seq1 else 'N/A'}")
                output_lines.append(f"[{self.species_target}] Longest Transcript Length: {len(gene_seq2) if gene_seq2 else 'N/A'}")
                if gene_seq1 and gene_seq2:
                    output_lines.append("\n[Longest Transcript Sequence BLAST Alignment Results]")
                    blast_result = run_local_blast(gene_seq1, gene_seq2, result['source_species']['gene_id'], result['target_species']['gene_id'], "gene")
                    output_lines.append(filter_blast_reference(str(blast_result)))
            else:
                output_lines.append("Type parameter error, must be gene, protein, or ALL")

            # Write to file
            with open(f"{gene}.out", "w", encoding="utf-8") as f:
                f.write('\n'.join(output_lines))
        print("All gene analysis results have been written to separate .out files.")


def main():
    parser = argparse.ArgumentParser(
        description="Cross-species homologous gene sequence alignment CLI tool"
    )
    parser.add_argument('--speciesQuery', required=True, help='Source species Latin name, e.g., homo_sapiens')
    parser.add_argument('--speciesTarget', required=True, help='Target species Latin name, e.g., mus_musculus')
    parser.add_argument('--gene', required=True, help='Gene symbol (comma-separated or txt file path)')
    parser.add_argument('--type', required=True, help='Alignment type: gene, protein, or ALL; default is ALL')
    args = parser.parse_args()

    cli = GeneHomologyCLI(args.speciesQuery, args.speciesTarget, args.gene, args.type)
    cli.run()

if __name__ == "__main__":
    main() 