import java.io.FileReader;
import java.util.*;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import java.util.*;

public class SequenceAnalysis {

    public static void main(String[] args) {
        Scanner reader = new Scanner(System.in);
        analyze(reader.nextLine(),"RFC-10");
    }

    public static void analyze(String inputGeneSeq, String standardType) {
        ArrayList<String> illegalRestrictionSites = new ArrayList<>();
        String geneSequence;
        ArrayList<String> restrictionSites = new ArrayList<>();

        JSONParser jsonParser = new JSONParser();
        JSONObject jsonObject;
        Set<String> jsonCodonTable;

        try {
            jsonObject = (JSONObject) jsonParser.parse(new FileReader("src\\aminoacids.json"));
            geneSequence = inputGeneSeq.trim();
            jsonCodonTable = ((JSONObject) jsonObject.get("codon_table")).keySet();

            if (standardType.equals("RFC-10")) {
                JSONArray jsonArray = (JSONArray) ((JSONObject) jsonObject.get("restriction_sites")).get("RFC-10_restriction_sites");
                if (jsonArray != null) {
                    for (Object o : jsonArray) {
                        restrictionSites.add((String) o);
                    }
                }
            } else if (standardType.equals("RFC-1000")) {
                JSONArray jsonArray = (JSONArray) ((JSONObject) jsonObject.get("restriction_sites")).get("RFC-1000_restriction_sites");
                if (jsonArray != null) {
                    for (Object o : jsonArray) {
                        restrictionSites.add((String) o);
                    }
                }
            }
            if(geneSequence.substring(0,3).equals("ATG")) {
                for (String restrictionSite : restrictionSites) {

                    String sitePattern = restrictionSite.substring(restrictionSite.indexOf(':') + 2);

                    int patternSize = sitePattern.length();
                    int seqSize = geneSequence.length();

                    int i = 0, j;

                    while ((i + patternSize) <= seqSize) {
                        j = patternSize - 1;
                        while (geneSequence.charAt(i + j) == sitePattern.charAt(j)) {
                            j--;
                            if (j < 0) {
                                illegalRestrictionSites.add(restrictionSite + ", index:" + i + ",");
                                j = patternSize - 1;
                                i++;
                            }
                        }
                        i++;
                    }
                }
            }else{
                System.out.println("The coding region should start with an 'ATG' codon!");
                return;
            }

            if (illegalRestrictionSites.size() == 0) {
                System.out.println("No illegal sites for " + standardType);
                return;
            }
            int arrayIndex = 0;

            for (String restrictionSite : illegalRestrictionSites) {

                String sitePattern = restrictionSite.substring(restrictionSite.indexOf(':') + 1,
                        restrictionSite.indexOf(','));
                int index = Integer.parseInt(restrictionSite.substring(restrictionSite.lastIndexOf(':') + 1,
                        restrictionSite.lastIndexOf(',')));

                label1:
                for (int k = 0; k < sitePattern.length() / 3 + ((index % 3 == 0) ? 0 : 1); k++) {

                    for (String key : jsonCodonTable) {

                        String codonGroup;

                        ArrayList<Integer> codonIndexes = new ArrayList<>();
                        codonIndexes.add(0, 0);

                        for (int acid = 0; acid < ((JSONArray) ((JSONObject) jsonObject.get("codon_table"))
                                .get(key)).size(); acid++) {

                            String codon = ((JSONArray) ((JSONObject) jsonObject.get("codon_table"))
                                    .get(key)).get(acid).toString();

                            String changeableCodon = geneSequence.substring(index - index % 3 + k * 3, index - index % 3 + 3 + k * 3);

                            if (codon.equals(changeableCodon)) {
                                codonGroup = key;
                                illegalRestrictionSites.set(arrayIndex, illegalRestrictionSites.get(arrayIndex) + " " + codonGroup + ":");
                                for (int i = 0; i < ((JSONArray) ((JSONObject) jsonObject.get("codon_table"))
                                        .get(key)).size(); i++) {
                                    if (acid != i)
                                        codonIndexes.add(i, i);
                                }
                            } else {
                                continue;
                            }

                            label2:
                            for (int codonIndex = 0; codonIndex < codonIndexes.size(); codonIndex++) {
                                String changedSequence = geneSequence.substring(0, index - index % 3) + ((JSONArray) ((JSONObject) jsonObject.get("codon_table"))
                                        .get(codonGroup)).get(codonIndex).toString() + geneSequence.substring(index + 3 - index % 3);

                                int patternSize = sitePattern.length();

                                int i = index - patternSize;
                                int j;

                                while ((i + patternSize) <= index + patternSize) {
                                    j = patternSize - 1;
                                    while (changedSequence.charAt(i + j) == sitePattern.charAt(j)) {
                                        j--;
                                        if (j < 0) {
                                            continue label2;
                                        }
                                    }
                                    i++;
                                }
                                illegalRestrictionSites.set(arrayIndex, illegalRestrictionSites.get(arrayIndex)
                                        + ((JSONArray) ((JSONObject) jsonObject.get("codon_table")).get(codonGroup)).get(codonIndex) + ",");

                            }
                        }
                    }
                }
                arrayIndex++;
            }
            for (String str: illegalRestrictionSites) {
                System.out.println(str);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
