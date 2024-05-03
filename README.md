# ELAN to WebMAUS Converter
## Created by Blaine Billings and modified by Jacob Hakim
This simple Python script takes a long, annotated ELAN file and corresponding .wav file (or batch of ELAN/.wav files) and:
- slices audio into chunks corresponding to each annotation
- creates a .csv for each annotation in the format required for WebMAUS (with IPA, NOT SAMPA)
- saves .csv and .wav pairs together in a new directory labelled "split-files" under the original parent directory

## How to use this script
1. Edit the "input_filepath" variable to match the directory containing all your files to be processed
   - Note: the script expects one parent directory with subfolders for each recording session, with .eaf and .wav files
   - There can be multiple recordings and transcription files per session, but it is expected they share a session ID, e.g. "XYZ-100-01", "XYZ-100-02"
     
2. Modify the "sessions" variables for your folders containing ELAN and corresponding audio files to be processed. For example:
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
 - This script will process two session folders, "BJM02-152" and "BJM02-157"
 - In the first folder, it will process two ELAN files, "BJM02-152-01.eaf" and "BJM02-152-02.eaf"
   - Two tiers from each .eaf will be processed: "S1" and "S2"
   - IMPORTANT: the corresponding .wav file for each tier to be processed should be named according to the name of the ELAN file, with the tier name appended following an underscore, e.g. "BJM02-152-01_S1.wav", "BJM02-152-01_S2.wav"
 - In the second folder, it will process tiers "S1" and "S2" from two ELAN files, "BJM02-157-02.eaf" and "BJM02-157-04.eaf"
 - This code can be repeated/altered for any number of sessions, session portions, and tiers to be processed.

3. Modify the "to_webmaus_format(annotation)" function to reflect the orthography/IPA conventions of your language. (The current rules reflect the IPA transcriptions for Nasal orthography.)
   - These rules can be specified for characters in certain syllables, as shown in lines 52 - 57 (**more instructions forthcoming**)

4. The code will create a directory "split-files" within each session directory specified at the start of the script. It will contain .wav and .csv pairs to be uploaded to WebMAUS.
   
5. Drag all files in a split-files folder into [WebMAUS](https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/WebMAUSGeneral). Change "Input Encoding" in the Service Options Menu to "IPA (UTF-8)".
   -Note: you open the "Expert Options" dropdown menu and change "Output Encoding" to "IPA" if you would rather have IPA annotations in the output TextGrids.

6. Once all .wav/.csv pairs have been uploaded, the WebMAUS service should run with no errors (provided the IPA encoding in the script was specified correctly) and output a .zip file of TextGrid files with force-aligned segments for each word in your annotation.
