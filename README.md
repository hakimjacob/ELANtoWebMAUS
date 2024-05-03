# ELAN to WebMAUS Converter
This simple Python script takes a long, annotated ELAN file and corresponding .wav file (or batch of ELAN/.wav files) and:
-slices audio into chunks corresponding to each annotation
-creates a .csv for each annotation in the format required for WebMAUS (with IPA, NOT SAMPA)
-saves .csv and .wav pairs together in a new directory labelled "split-files" under the original parent directory

