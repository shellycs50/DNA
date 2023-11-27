import csv
import sys


# notes:
# takes argv len of 3 (csv, textofdna)
# read csv into memory
# 0 = AGATC 1 = AATG 2= TATC
def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py <database.csv> <profile.txt>")
        sys.exit(1)
    # TODO: Read database file into a variable
    file = open(sys.argv[1])
    reader = csv.DictReader(file)

    # TODO: Read DNA sequence file into a variable
    suspect_list = []
    fieldnames = reader.fieldnames
    for row in reader:
        suspect_dict = {}
        for fieldname in fieldnames:
            suspect_dict[str(fieldname)] = row[fieldname]
        suspect_list.append(suspect_dict)

    # AGATC 1 = AATG 2= TATC
    # TODO: Find longest match of each STR in DNA sequence
    with open(sys.argv[2], "r") as unsub_dna_file:
        unsub_dna = unsub_dna_file.read()
    # works as intended

    fieldnames2 = reader.fieldnames
    fieldnames2.remove("name")
    fieldname_matches = {}
    for field in fieldnames2:
        fieldname_matches[field] = longest_match(unsub_dna, str(field))

    # TODO: Check database for matching profiles
    fieldnamecount = len(fieldnames2)
    match_count = 0
    for suspect in suspect_list:
        for unsubdnatype, unsubdnacount in fieldname_matches.items():
            if int(suspect[unsubdnatype]) == int(unsubdnacount):
                # note that the suspect has to match the unsub fields. the unsub doesn't have to match the suspect fields (if there were more fields analysed for suspects).
                match_count += 1
        if match_count == fieldnamecount:
            print(suspect["name"])
            sys.exit(0)
        else:
            match_count = 0
    print("No Match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):  # repeat subsequence length times
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
