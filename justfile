alias te:=test

# [no-cd]
[working-directory: 'regr_smlp/code']
test:
    uv run smlp_regr.py -w 8 -def n -t all -tol 7

# [no-cd]
[working-directory: 'regr_smlp/code']
toy:
    uv run smlp_regr.py -w 8 -def n -t toy -tol 7

# [no-cd]
[working-directory: 'regr_smlp/code']
ind:
    uv run ../../src/run_smlp.py -data "../data/smlp_toy_num_resp_mult.csv" -out_dir ./ -pref Test34 -mode predict -resp y1,y2 -feat x,p1,p2 -model nn_keras -save_model_config f -mrmr_pred 0 -plots f -pred_plots f -resp_plots f -seed 10 -nn_keras_epochs 20 -nn_keras_seq_api f -log_time f  -new_dat "../data/smlp_toy_num_resp_mult_pred_labeled.csv"

[working-directory: 'regr_smlp/code']
man:
    ../../src/run_smlp.py -data "../data/smlp_toy_basic" -out_dir ../toy_basic -pref Test113 \
    -mode optimize -pareto t -resp y1,y2 -feat x1,x2,p1,p2 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -model_name test113_model -save_model_config t -plots f -seed 10 -log_time f \
    -spec ../specs/smlp_toy_basic.spec 
[working-directory: 'regr_smlp/code']
ana:
    ../../src/run_smlp.py -data "../data/smlp_toy_basic" -out_dir ../toy_basic -pref Test113 \
    -mode subgroups -pareto t -resp y0,y2 -feat x1,x2,p1,p2 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -model_name test113_model -save_model_config t -plots f -seed 10 -log_time f \
    -spec ../specs/smlp_toy_basic.spec 
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
    -spec regr_smlp/specs/smlp_toy_basic.spec -dr

dra amount:
    uv run src/run_smlp.py -data "regr_smlp/data/smlp_toy_basic" -out_dir regr_smlp/toy_basic -pref Test113 \
    -mode train -pareto t -resp y1,y2 -feat x1,x2,p1,p2 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -model_name test113_model -save_model_config t -plots f -seed 10 -log_time f \
    -spec regr_smlp/specs/smlp_toy_basic.spec -dr -dra {{amount}}

exp:
    uv run src/run_smlp.py -data "regr_smlp/data/smlp_toy_num_mult" -out_dir regr_smlp/num_mult -pref Test113 \
    -mode train -pareto t -resp y1,y2 -feat x1,x2,p1,p2 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -plots f -seed 10 -log_time f \
    -spec regr_smlp/specs/smlp_toy_num_resp_mult.spec -dr


