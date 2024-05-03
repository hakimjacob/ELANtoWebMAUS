# ELAN to WebMAUS Converter
This simple Python script takes a long, annotated ELAN file and corresponding .wav file (or batch of ELAN/.wav files) and:
- slices audio into chunks corresponding to each annotation
- creates a .csv for each annotation in the format required for WebMAUS (with IPA, NOT SAMPA)
- saves .csv and .wav pairs together in a new directory labelled "split-files" under the original parent directory

## How to use this script
1. Edit the "input_filepath" variable to match the directory containing all your files to be processed
   - Note: the script expects one parent directory with subfolders for each recording session, with .eaf and .wav files
   - There can be multiple recordings and transcription files per session, but it is expected they share a session ID, e.g. "XYZ-100-01", "XYZ-100-02"
3. Modify the "sessions" variables for your folders containing ELAN and corresponding audio files to be processed. For example:
```
sessions = {
    "BJM02-152": {
        "01": ["S1", "S2"],
        "02": ["S1", "S2"]
    },
     "BJM02-157": {
        "02": ["S1", "S2"],
        "04": ["S1", "S2"]
    }
}
```
 - This script will process two session folders, "
