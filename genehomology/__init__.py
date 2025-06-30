"""
Cross-species homologous gene sequence alignment tool

This package provides tools for homologous gene query and sequence alignment.
"""

from .core import get_gene_description, get_homologues, get_sequence, run_local_blast
from .cli import GeneHomologyCLI
from .utils import filter_blast_reference

__version__ = "0.1.0"
__author__ = "GeneHomology Team"

__all__ = [
    "GeneHomologyCLI", 
    "get_gene_description", 
    "get_homologues", 
    "get_sequence", 
    "run_local_blast",
    "filter_blast_reference"
] 