base:
    uv run src/run_smlp.py -data "regr_smlp/data/smlp_toy_basic" -out_dir project -pref Test113 \
    -mode train -pareto t -resp y1,y2 -feat x1,x2,p1,p2 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -model_name test113_model -save_model_config t -plots f -seed 10 -log_time f \
    -spec regr_smlp/specs/smlp_toy_basic.spec
dr:
    uv run src/run_smlp.py -data "regr_smlp/data/smlp_toy_basic" -out_dir project -pref Test113 \
    -mode train -pareto t -resp y1,y2 -feat x1,x2,p1,p2 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -model_name test113_model -save_model_config t -plots f -seed 10 -log_time f \
    -spec regr_smlp/specs/smlp_toy_basic.spec -dr -split 0.5

dra amount:
    uv run src/run_smlp.py -data "regr_smlp/data/smlp_toy_basic" -out_dir project -pref Test113 \
    -mode verify -pareto t -resp y1,y2 -feat x1,x2,p1,p2 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -model_name test113_model -save_model_config t -plots f -seed 10 -log_time f \
    -spec regr_smlp/specs/smlp_toy_basic.spec -dr -dra {{amount}} -split 0.5

exp:
    uv run src/run_smlp.py -data "regr_smlp/data/smlp_toy_num_mult" -out_dir regr_smlp/num_mult -pref Test113 \
    -mode train -pareto t -resp y1,y2 -feat x1,x2,p1,p2 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -plots f -seed 10 -log_time f \
    -spec regr_smlp/specs/smlp_toy_num_resp_mult.spec -dr

intela amount:
    uv run src/run_smlp.py -data "bench/intel/data/read_bowtie_anonym.csv" -out_dir project -pref Test113 \
    -mode train -pareto t -resp o0,o1,o2,o3 -feat p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -plots f -seed 10 -log_time f \
    -spec bench/intel/specs/read_bowtie_anonym.spec -dr -dra {{amount}}

intel:
    uv run src/run_smlp.py -data "bench/intel/data/read_bowtie_anonym.csv" -out_dir project -pref Test113 \
    -mode train -pareto t -resp o0,o1,o2,o3 -feat p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -plots f -seed 10 -log_time f \
    -spec bench/intel/specs/read_bowtie_anonym.spec -dr

largea amount:
    uv run src/run_smlp.py -data "bench/intel/data/s2_rx_anonym.csv" -out_dir project -pref Test113 \
    -mode verify -pareto t -resp o0,o1 -feat CH,RANK,Byte,p0,p1,p2,p3,p4,p5 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -plots f -seed 10 -log_time f \
    -spec bench/intel/specs/s2_rx_anonym.spec -dra {{amount}}

largeann amount:
    uv run src/run_smlp.py -data "bench/intel/data/s2_rx_anonym.csv" -out_dir project -pref Test4 \
    -mode predict -pareto t -resp o0,o1 -feat CH,RANK,Byte,p0,p1,p2,p3,p4,p5 -model nn_keras -nn_keras_weights_precision 2 \
    -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -plots f -seed 10 -log_time f \
    -nn_keras_epochs 20 -nn_keras_seq_api f \
    -spec bench/intel/specs/s2_rx_anonym.spec -dra {{amount}}

largeann_test:
    uv run src/run_smlp.py -data "bench/intel/data/s2_rx_anonym.csv" -new_dat "bench/intel/data/s2_rx_anonym.csv" \
    -out_dir project -pref Test4 \
    -mode predict -pareto t -resp o0,o1 -feat CH,RANK,Byte,p0,p1,p2,p3,p4,p5 -model nn_keras -nn_keras_weights_precision 2 \
    -save_model_config f -mrmr_pred 0 -plots f -pred_plots f -resp_plots f -seed 10 \
    -log_time t -nn_keras_epochs 20 -nn_keras_seq_api f

[working-directory: 'regr_smlp/code']
works:
    ../../src/run_smlp.py -data "../data/smlp_toy_num_resp_mult.csv" -out_dir ./ \
    -pref Test4 -mode predict -resp y2 -feat x,p1,p2 -model nn_keras -nn_keras_weights_precision 2 \
    -save_model_config f -mrmr_pred 0 -plots f -pred_plots f -resp_plots f -seed 10 \
    -log_time f -nn_keras_epochs 20 -nn_keras_seq_api f -new_dat "../data/smlp_toy_num_resp_mult_pred_labeled.csv"


works-base-resp dim wg pr:
    ./src/run_smlp.py -data "regr_smlp/data/smlp_toy_num_resp_mult.csv" -out_dir ./project \
    -pref Test113 -mode predict -resp y1,y2 -feat categ,x,p1,p2 -model nn_keras -nn_keras_weights_precision 2 \
    -save_model_config t -mrmr_pred 0 -plots f -pred_plots f -resp_plots f -seed 10 -split 0.5 \
    -log_time f -nn_keras_epochs 20 -nn_keras_seq_api f -new_dat "regr_smlp/data/smlp_toy_num_resp_mult.csv" \
    -dr -dra {{dim}} -wg {{wg}} --nn_keras_weights_precision {{pr}} -split 0.5

works-base dim wg pr:
    ./src/run_smlp.py -data "regr_smlp/data/smlp_toy_basic" -out_dir ./project \
    -pref Test113 -mode predict -resp y1,y2 -feat x1,x2,p1,p2 -model nn_keras -nn_keras_weights_precision 2 \
    -save_model_config t -mrmr_pred 0 -plots f -pred_plots f -resp_plots f -seed 10 -split 0.5 \
    -log_time f -nn_keras_epochs 20 -nn_keras_seq_api f -new_dat "regr_smlp/data/smlp_toy_basic" \
    -dr -dra {{dim}} -wg {{wg}} --nn_keras_weights_precision {{pr}} -split 0.5

optimize:
    ./src/run_smlp.py -data "regr_smlp/data/smlp_toy_basic" -out_dir ./project -pref Test113 \
    -mode optimize -pareto t -use_model t -resp y1,y2 -feat x1,x2,p1,p2 -save_model f \
     -mrmr_pred 0 -plots f -seed 10 -model_name  Test113_smlp_toy_num_resp_mult \
    -log_time f -spec regr_smlp/specs/smlp_toy_system_stable_constant_synth_feasible.spec -model nn_keras \
    -spec regr_smlp/specs/smlp_toy_basic.spec -split 0.5

[working-directory: 'regr_smlp/code']
works-dra amount:
    ../../src/run_smlp.py -data "../data/smlp_toy_num_resp_mult.csv" -out_dir ./ \
    -pref Test4 -mode predict -resp y2 -feat x,p1,p2 -model nn_keras -nn_keras_weights_precision 2 \
    -save_model_config f -mrmr_pred 0 -plots f -pred_plots f -resp_plots f -seed 10 \
    -log_time f -nn_keras_epochs 20 -nn_keras_seq_api f -new_dat "../data/smlp_toy_num_resp_mult_pred_labeled.csv" -dra {{amount}}

[working-directory: 'regr_smlp/code']
works-log:
    ../../src/run_smlp.py -data "../data/smlp_toy_num_resp_mult.csv" -out_dir ./ \
    -pref Test4 -mode predict -resp y2 -feat x,p1,p2 -model nn_keras -nn_keras_weights_precision 2 \
    -save_model_config f -mrmr_pred 0 -plots f -pred_plots f -resp_plots f -seed 10 \
    -log_time t -nn_keras_epochs 20 -nn_keras_seq_api f -new_dat "../data/smlp_toy_num_resp_mult_pred_labeled.csv"
