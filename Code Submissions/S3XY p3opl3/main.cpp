#include <string.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <memory>
#include <set>
#include <algorithm>

// Min length of restricted sequence
int MIN_SEQ_LENGTH = 4;

class AminoAcids {
private:
// Codon is 3 letter sequence, name is the name of the acid
std::map<std::string, std::string> codonToName;
std::map<std::string, std::vector<std::string> > nameToCodons;

// Divides line by delimeter and returns "pos" sequence substring
std::string parseLine(std::string &line, int pos) {
    int delimeterNum = 0;
    char delimeter = ',';
    std::string ret = "";
    for(int i = 0; i < line.size(); i++) {
        if(line[i] == delimeter) {
            delimeterNum++;
            continue;
        }
        if(delimeterNum == pos) {
            ret += line[i];
        }
        if(delimeterNum > pos) {
            break;
        }
    }
    return ret;
}
public:
    AminoAcids(std::string filename) {
        std::ifstream AminoAcidsFile(filename);
        std::string aminoAcid;
        while (getline (AminoAcidsFile, aminoAcid)) {
            std::string codon = parseLine(aminoAcid, 0);
            std::string name = parseLine(aminoAcid, 1);
            codonToName[codon] = name;
            nameToCodons[name].push_back(codon);
        }
    }
    std::vector<std::string> getAlternativeCodons(std::string & codon) {
        std::string &s = codonToName[codon];
        std::vector<std::string> codons = nameToCodons[s];
        std::vector<std::string> filteredCodons;
        for(int i = 0; i < codons.size(); i++) {
            if(codons[i] != codon) {
                filteredCodons.push_back(codons[i]);
            }
        }
        return filteredCodons;
    }
    std::string getCodonName(std::string & codon) {
        return codonToName[codon];
    }
};

class RestrictionEnzymes {
// [[sequence, name],...]
std::vector<std::pair<std::string, std::string> > sequences;

std::string parseSeqName(std::string & line) {
    std::string seqName = "";
    for(int i = line.size() - 1; i >= 0; i--) {
        if(line[i] == ' ') {
            break;
        }
        seqName += line[i];
    }
    std::reverse(seqName.begin(), seqName.end());
    return seqName;
}

void insertSequences(std::string & line, std::string & enzymeName) {
    std::string currSequence = "";
    std::vector<std::string> result;
    bool start = false;
    for(int i = line.size() - 1; i >= 0; i--) {
        if(line[i] == ',') {
            start = true;
            continue;
        }
        if(line[i] == ' ' && currSequence.size() != 0) {
            start = false;
            std::reverse(currSequence.begin(), currSequence.end());
            if(currSequence.size() >= MIN_SEQ_LENGTH) {
                sequences.push_back(std::make_pair(currSequence, enzymeName));
            }
            currSequence.clear();
            continue;
        }
        if(start)
            currSequence += line[i];
    }
}

public:
    RestrictionEnzymes(std::string filename, std::string selectedRestrictionsFilename = "") {
        std::string fileLine;
        std::set<std::string> selectedRestrictions;

        if(selectedRestrictionsFilename.size() > 0) {
            std::ifstream SelectedFile(selectedRestrictionsFilename);
            while (getline (SelectedFile, fileLine)) {
                selectedRestrictions.insert(fileLine);
            }
        }

        std::ifstream AminoAcidsFile(filename);
        std::string curSeqName = "";
        while (getline (AminoAcidsFile, fileLine)) {
            std::string lineType = "";
            lineType += (char)fileLine[0];
            lineType += (char)fileLine[1];
            if(lineType == "ID") {
                curSeqName = parseSeqName(fileLine);
            }
            if(lineType == "RS") {
                // Name already known by the time we reach sequences
                if(selectedRestrictions.size() == 0
                || selectedRestrictions.find(curSeqName) != selectedRestrictions.end()) {
                    insertSequences(fileLine, curSeqName);
                    curSeqName.clear();
                }
            }
        }
    }
    std::vector<std::pair<std::string, std::string> > getEnzymes() {
        return sequences;
    }
};

// Return the matching enzyme sequence number starting from specified index
int getMatchingRestrictionSequence(std::string & dnaSequence
    , std::vector<std::pair<std::string, std::string> > & restrictionEnzymes
    , int startIndex
    , int endIndex
    , int currIndex) {
    for(int j = 0; j < restrictionEnzymes.size(); j++) {
        std::string & enzyme = restrictionEnzymes[j].first;
        int endSubIndex = currIndex + enzyme.size();
        bool matching = true;
        if(endSubIndex > endIndex) {
            continue;
        }
        for(int k = currIndex; k < endSubIndex; k++) {
            if(dnaSequence[k] != enzyme[k - currIndex]) {
                matching = false;
                break;
            }
        }
        if(matching) {
            return j;
        }
    }
    return -1;
}

// Returns index and string within sequence to which replace it
std::pair<int, std::string> replaceRestrictedSequence(std::string & dnaSequence
    , std::shared_ptr<AminoAcids> acids
    , std::vector<std::pair<std::string, std::string> > & restrictionEnzymes
    , int start
    , int end
    , int sequenceIndex
    , int restrictionStart
    , int restrictionEnd
) {
    for(int i = restrictionStart; i < restrictionEnd; i++) {
        if((i - start) % 3 == 0) {
            std::string acid;
            acid += dnaSequence[i];
            acid += dnaSequence[i + 1];
            acid += dnaSequence[i + 2];
            std::vector< std::string > alternatives = acids->getAlternativeCodons(acid);
            if(alternatives.size() > 0) {
                return std::make_pair(i, alternatives[0]);
            }
        }
    }
    return std::make_pair(-1, "");
}


int main(int argc, char *argv[]) {
    std::string inputDnaFile;
    std::string outputFile;
    std::string selectedRestrictionsFile;
    if(argc == 4){
        inputDnaFile = std::string(argv[1]);
        outputFile = std::string(argv[2]);
        selectedRestrictionsFile = std::string(argv[3]);
    } else {
        std::cerr << "Need to specify files for DNA sequence, output, and selected restrictions\n";
        return 0;
    }
    // Amino Acids. Source: http://www.hgmd.cf.ac.uk/docs/cd_amino.html
    std::shared_ptr<AminoAcids> acids(new AminoAcids("acids.txt"));
    std::string codonExample = "TCT";
    std::vector<std::string> codons = acids->getAlternativeCodons(codonExample);

    // Restriction Sites (from 5' to 3'). Source:http://rebase.neb.com/rebase/link_bairochc
    std::shared_ptr<RestrictionEnzymes> enzymesObj(new RestrictionEnzymes("restrictions.txt", selectedRestrictionsFile));
    std::vector<std::pair<std::string, std::string> > restrictionEnzymes = enzymesObj->getEnzymes();

    // O(n * c * m), n - DNA, m - length of restr seq, c - num of rest seq
    std::string dnaSequence = "";
    std::ifstream DNAFile(inputDnaFile);
    char byte;
    while (DNAFile.get(byte)) {
        dnaSequence.push_back(byte);
    }

    // Start codon is one, but end codon is multiple
    std::string startCodon = "ATG";
    std::string endCodonName = "Termination";

    // Our DNA seqience will be between [startIndex, endIndex)
    int startIndex = -1;
    int endIndex = -1;

    // Determine indexes
    for(int i = 0; i < dnaSequence.size(); i++) {
        if(i + 2 >= dnaSequence.size()) {
            break;
        }
        std::string codon = "";
        codon += dnaSequence[i];
        codon += dnaSequence[i + 1];
        codon += dnaSequence[i + 2];
        if(codon == startCodon && startIndex == -1) {
            startIndex = i + 3;
        } else if(startIndex > -1 && (i - startIndex) % 3 == 0 && acids->getCodonName(codon) == endCodonName) {
            endIndex = i;
            break;
        }
    }
    if(startIndex == -1) {
        // No start/end codons
        startIndex = 0;
        endIndex = dnaSequence.size();
    }
    std::vector< std::pair<int, std::string> > result;
    std::vector< std::string > result_enzyme_names;
    std::vector< std::string > result_enzyme_sequence;
    std::vector< int> result_enzyme_index;
    for(int i = startIndex; i < endIndex; i++) {
        int sequenceIndex = getMatchingRestrictionSequence(dnaSequence, restrictionEnzymes, startIndex, endIndex, i);
        if(sequenceIndex != -1) {
            int restrictionSize = restrictionEnzymes[sequenceIndex].first.size();
            std::pair<int, std::string> replacement;
            replacement = replaceRestrictedSequence(
                dnaSequence,
                acids,
                restrictionEnzymes,
                startIndex,
                endIndex,
                sequenceIndex,
                i,
                i + restrictionSize
            );
            result.push_back(replacement);
            result_enzyme_names.push_back(restrictionEnzymes[sequenceIndex].second);
            result_enzyme_sequence.push_back(restrictionEnzymes[sequenceIndex].first);
            result_enzyme_index.push_back(i);
            if(replacement.first != -1) {
                i = i + restrictionSize - 1;
            }
        }
    }

    std::ofstream resultFile;
    resultFile.open(outputFile);
    for(int i = 0; i < result.size(); i++) {
        resultFile << result[i].first << "," << result[i].second
                   << "," << result_enzyme_names[i] << "," << result_enzyme_sequence[i] 
                   << "," << result_enzyme_index[i] << std::endl;
    }
    resultFile.close();

    std::cout << "Done!" << std::endl;

    return 0;
}
