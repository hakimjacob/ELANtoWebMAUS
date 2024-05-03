import os

#
#
# Edit these variables
#
#

# Sessions/speakers info
sessions = {
    # "BJM02-152": {
        #"01": ["S1", "S2"],
        #"02": ["S1", "S2"]
    # },
     # "BJM02-157": {
        # "02": ["S1", "S2"],
        # "04": ["S1", "S2"]
    # },
     # "BJM02-167": {
        # "01": ["S1", "S2"],
        # "02": ["S1", "S2"],
        # "03": ["S1", "S2"]
    # },
     # "BJM02-169": {
        # "01": ["S1", "S2"],
        # "02": ["S1", "S2"],
        # "03": ["S1", "S2"]
    # }
    "BJM02-143": {
        "02": ["S1", "S2"]
     }
}

# Input filepath
# - eaf files are expected to be located at:
#   INPUT_FILEPATH/SESSION_ID/SESSION_ID-SESSION_PORTION.eaf
input_filepath = "C:/Users/jake/Desktop/fieldwork_23/Task-2"

#
#
#
#
#

def to_webmaus_format(annotation):
    annotation = annotation.lower()  # Convert to lowercase
    annotation = annotation.replace(".", "").replace(",", "").replace("?", "").replace("-", "") # Remove hyphens
    annotation_parts = annotation.split(" ")
    for index in range(len(annotation_parts)):
        ipa_annotation_part = annotation_parts[index]
        ipa_annotation_part = ipa_annotation_part.replace("ng", "ŋ").replace("ny", "ɲ").replace("kh", "χ").replace("e", "ə").replace("y", "j").replace("c", "ʧ").replace("j", "ʤ").replace("g", "ɡ")
        if len(annotation) > 0 and ipa_annotation_part[-1:] == "k":
            ipa_annotation_part = ipa_annotation_part[:-1] + "ʔ"
        if len(annotation) > 1 and ipa_annotation_part[-2:-1] == "i":
            ipa_annotation_part = ipa_annotation_part[:-2] + "ɪ" + ipa_annotation_part[-1:]
        if len(annotation) > 1 and ipa_annotation_part[-2:-1] == "u":
            ipa_annotation_part = ipa_annotation_part[:-2] + "ʊ" + ipa_annotation_part[-1:]
        annotation_parts[index] = annotation_parts[index] + ";" + " ".join(list(ipa_annotation_part)).replace("ʧ", "tʃ").replace("ʤ", "dʒ")
    return "\n".join(annotation_parts) + "\n"

# Iterate through each session_id/session_portion/speaker combination
for session_id in sessions.keys():
    # For each session, either create split-files folder or delete everything in it
    output_filepath = f'{input_filepath}/{session_id}/split-files'
    if not os.path.isdir(output_filepath):
        os.mkdir(output_filepath)
    else:
        for file in os.listdir(output_filepath):
            file_to_delete = os.path.join(output_filepath, file)
            if os.path.isfile(file_to_delete):
                os.remove(file_to_delete)

    for session_portion in sessions[session_id].keys():
        for speaker in sessions[session_id][session_portion]:
            # Opens transcription file and output notes file
            elan_file = open(f'{input_filepath}/{session_id}/{session_id}-{session_portion}.eaf', "r")

            # { time_slot_id : time_slot_value }
            # Dictionary that maps slot ids to their actual millisecond values
            time_slots = {}
            # { annotation_id : (tier_id, start_time_slot, end_time_slot) }
            # Dictionary that maps annotation ids to their respective tier and start/end time slots
            annotation_ids = {}
            # { (tier_id, annotation_id) : { (tier_id, annotation_id) : annotation} }
            # Nested dictionary for containing annotation values
            # - Each top (key, value) pair is a top tier annotation.
            #   Each (key, value) pair in the first layer's value is an
            #   identifier for the sub tier (also can be top tier) mapped to its annotation
            annotations = {}

            in_annotation = False
            time_ref = False
            annotation_id = annotation_ref = time_slot_ref1 = time_slot_ref2 = annotation_value = current_tier = ""
            for line in elan_file:
                # Operations for each searched string:
                # - <TIME_SLOT:         grab time_slot_id w/ time_slot_value, save together
                # - TIER_ID:            grab tier_id
                # - </ANNOTATION:       
                #                       mark no longer in annotation, mark time_ref no longer grabbed
                # - ANNOTATION_ID:      grab annotation_id
                # - ANNOTATION_REF:     grab annotation_ref
                # - TIME_SLOT_REF1:     grab time_slot_ref1, mark time_ref as grabbed
                # - TIME_SLOT_REF2:     grab time_slot_ref2
                # - <ANNOTATION_VALUE:  grab annotation value
                # - <ANNOTATION:        mark currently in annotation

                if "<TIME_SLOT" in line:
    # Check if "=" exists in the line before accessing its index
                    if "=" in line:
                        line = line[line.index("=") + 1:]
        # Check if "\"" exists in the line before accessing its index
                        if "\"" in line:
                            time_slot_id = line[line.index("\"") + 1:]
                            time_slot_id = time_slot_id[:time_slot_id.index("\"")]
                            line = line[line.index("=") + 1:]
            # Check if "\"" exists in the line before accessing its index
                        if "\"" in line:
                            time_slot_value = line[line.index("\"") + 1:]
                            time_slot_value = time_slot_value[:time_slot_value.index("\"")]
                
                # Check if the time value is empty (contains only whitespace)
                        if time_slot_value.strip():
                    # Add the time slot ID and value to the dictionary
                           time_slots[time_slot_id] = time_slot_value
                        else:
                            print("Error: Could not find closing quotation mark (\") for time slot value.")
                    else:
                        print("Error: Could not find opening quotation mark (\") for time slot ID.")
                else:
                    print("Error: Could not find equals sign (=) in line.")
                    
                if "TIER_ID=\"" in line:
                    tier_id = line[line.index("TIER_ID=\"") + len("TIER_ID=\""):]
                    tier_id = tier_id[:tier_id.index("\"")]
                if "</ANNOTATION>" in line and tier_id == speaker:
                    # If time ref was grabbed (i.e. in a top tier)
                    # - save annotation_id and annotation with respective information
                    # - grab audio clip
                    if time_ref:
                        annotation_value_for_filename = annotation_value.replace(".", "").replace(",", "").replace("?", "").replace("!", "").replace(" ", "_")

                        annotation_ids[annotation_id] = (tier_id, time_slot_ref1, time_slot_ref2)
                        annotations[(tier_id, annotation_id)] = {(tier_id, annotation_id) : annotation_value}
                        os.system(f'ffmpeg -i {input_filepath}/{session_id}/{session_id}-{session_portion}_{speaker}.wav -ss {int(time_slots[time_slot_ref1]) / 1000.0} -to {int(time_slots[time_slot_ref2]) / 1000.0} {output_filepath}/{session_id}-{session_portion}_{speaker}_{annotation_id}_{annotation_value_for_filename}.wav')

                        note_file = open(f'{output_filepath}/{session_id}-{session_portion}_{speaker}_{annotation_id}_{annotation_value_for_filename}.csv', "w", encoding='utf-8')
                        note_file.write(f'{to_webmaus_format(annotation_value)}')
                        note_file.close()
                    # If time ref was not grabbed (i.e., in a sub tier)
                    # - save annotation_id and annotation with respective information (some grabbed from parent)
                    else:
                        parent_tier_id, time_slot_ref1, time_slot_ref2 = annotation_ids[annotation_ref]
                        annotations[(parent_tier_id, annotation_ref)][(tier_id, annotation_id)] = annotation_value
                        annotation_ids[annotation_id] = (tier_id, time_slot_ref1, time_slot_ref2)
                        annotations[(tier_id, annotation_id)] = {(tier_id, annotation_id) : annotation_value}

                    # Mark that annotation closed and time no longer referenced
                    in_annotation = False
                    time_ref = False

                if in_annotation and "ANNOTATION_ID=\"" in line:
                    annotation_id = line[line.index("ANNOTATION_ID=\"") + len("ANNOTATION_ID=\""):]
                    annotation_id = annotation_id[:annotation_id.index("\"")]
                if in_annotation and "ANNOTATION_REF=\"" in line:
                    annotation_ref = line[line.index("ANNOTATION_REF=\"") + len("ANNOTATION_REF=\""):]
                    annotation_ref = annotation_ref[:annotation_ref.index("\"")]
                if in_annotation and "TIME_SLOT_REF1=\"" in line:
                    time_slot_ref1 = line[line.index("TIME_SLOT_REF1=\"") + len("TIME_SLOT_REF1=\""):]
                    time_slot_ref1 = time_slot_ref1[:time_slot_ref1.index("\"")]
                    time_ref = True
                if in_annotation and "TIME_SLOT_REF2=\"" in line:
                    time_slot_ref2 = line[line.index("TIME_SLOT_REF2=\"") + len("TIME_SLOT_REF2=\""):]
                    time_slot_ref2 = time_slot_ref2[:time_slot_ref2.index("\"")]
                if in_annotation and "<ANNOTATION_VALUE>" in line:
                    annotation_value = line[line.index("<ANNOTATION_VALUE>") + len("<ANNOTATION_VALUE>"):]
                    annotation_value = annotation_value[:annotation_value.index("<")]
                if "<ANNOTATION>" in line:
                    in_annotation = True

            # After processing all lines of file, iterate through each annotation id, write
            # its identifier, a semicolon, and the annotation value
            """
            for annotation_id in annotation_ids:
                note_file.write(f'{session_id}-{session_portion}_{annotation_id}')
                for annotation in annotations[(annotation_ids[annotation_id][0], annotation_id)].keys():
                    note_file.write(f';{annotations[(annotation_ids[annotation_id][0], annotation_id)][annotation].replace(";", ",")}')
                note_file.write("\n")
            """
