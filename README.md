Ανάλυση Δικτύου Χαρακτήρων – Game of Thrones

Το παρόν project αφορά την ανάλυση του δικτύου αλληλεπιδράσεων των χαρακτήρων της σειράς Game of Thrones, στο πλαίσιο του μαθήματος HY-484.

Στόχος είναι ο εντοπισμός των πιο σημαντικών χαρακτήρων.

Dataset

Το dataset είναι από το GitHub repository:

https://github.com/mathbeveridge/gameofthrones

Περιλαμβάνει δεδομένα αλληλεπιδράσεων χαρακτήρων χωρισμένα ανά σεζόν.

Δομή Αρχείων


data/
  got-s*-nodes.csv
  got-s*-edges.csv
  got-all-seasons-nodes.csv
  got-all-seasons-edges.csv

merge_nodes.py
merge_edges.py
LoadGraph.py
ReportPics/

Περιγραφή Scripts

merge_nodes.py

    Φορτώνει όλα τα αρχεία nodes ανά σεζόν

    Αφαιρεί διπλότυπους χαρακτήρες

    Δημιουργεί το αρχείο:

    got-all-seasons-nodes.csv

merge_edges.py

    Φορτώνει όλα τα αρχεία edges ανά σεζόν

    Ενώνει ίδιες ακμές

    Αθροίζει τα weights

    Δημιουργεί το αρχείο:

    got-all-seasons-edges.csv

    Σημείωση : Οι ακμές θεωρούνται undirected.

LoadGraph.py

    Κύριο αρχείο ανάλυσης.

    Υλοποιεί:

    Δημιουργία weighted, undirected γράφου

    Υπολογισμό:

    Degree

    Strength

    Betweenness Centrality

    PageRank

    Οπτικοποιήσεις:

    Κατανομές degree & strength

    Top-10 χαρακτήρες ανά metric

    Υπογράφο 40 πιο κεντρικών χαρακτήρων

    Ανάλυση κοινοτήτων με Louvain

    Τα αποτελέσματα αποθηκεύονται στον φάκελο ReportPics/.

Απαιτήσεις

    Python 3.9+

    pandas

    networkx

    matplotlib

    python-louvain


Εκτέλεση
python merge_nodes.py
python merge_edges.py
python LoadGraph.py
