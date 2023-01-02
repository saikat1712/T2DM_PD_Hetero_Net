# T2DM_PD_Hetero_Net
First download the T2DM_hetero and PD_hetero datasets (from the given link in the supplementary file).
Run the code for HAN model using the following command (for T2DM_hetero_data) :

python main.py -m HAN -d T2DM_hetero_data -t link_prediction -g -1 --use_best_config --load_from_pretrained

(-g = 0 for GPU and -1 for CPU running criteria)
