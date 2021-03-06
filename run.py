import pandas as pd
import os
import sys
from Scripts.generate_examples import text_to_tsv
from Scripts.join_tsv_with_preds import join_tsv_with_preds



def main(argv):
    input_dir = argv[0]
    output_dir = argv[1]
    question_file = argv[2]
    model_path = argv[3]
    weights_file = argv[4]
    print("Input directory is %s"%input_dir)
    print("Output directory is %s" % output_dir)
    print("Question file is %s" % question_file)
    
    print("Transforming data to tsv ...\n\n\n")
    tsv_fpaths = text_to_tsv(input_dir, output_dir, question_file)
    
    for fpath in tsv_fpaths:
        print("\n\nGetting Predictions for %s ..."%fpath)
        output_path = fpath[:-4] + "_predictions.json"
        
        prediction_command = "allennlp predict %s %s --output-file %s --weights-file %s --include-package allennlp_ccqa_extension.dataset_readers.ccqa_datasetreader --include-package allennlp_ccqa_extension.models.basic_classifier_modified --use-dataset-reader --silent --batch-size 8" %(model_path, fpath, output_path, weights_file)
        
        # use allennlp to predict
        os.system(prediction_command)
        print("Done predicting for  ...")

        print("Joining predictions output (%s) with original generated tsv (%s) ...\n\n"%(output_path, fpath))
        # join 
        join_tsv_with_preds(fpath, output_path, output_dir)
        
        
    print("All done!")



if __name__ == "__main__":
    main(sys.argv[1:])