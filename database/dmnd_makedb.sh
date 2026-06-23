fa=$1
gene=$2
diamond makedb --in $fa -d $gene
