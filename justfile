alias te:=test

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
    -mode train -pareto t -resp o0,o1 -feat CH,RANK,Byte,p0,p1,p2,p3,p4,p5 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -plots f -seed 10 -log_time f \
    -spec bench/intel/specs/s2_rx_anonym.spec -dra {{amount}}

new_set:
    uv run src/run_smlp.py -data "regr_smlp/data/smlp_toy_num_resp_mult.csv" -out_dir project -pref Test113 \
    -mode train -pareto t -resp y1,y2 -feat categ,x,p1,p2 -model dt_sklearn \
    -dt_sklearn_max_depth 15 -mrmr_pred 0 -epsilon 0.05 -delta_rel 0.01 -save_model t \
    -model_name test113_model -save_model_config t -plots f -seed 10 -log_time f \
    -spec regr_smlp/specs/smlp_toy_num_resp_mult.spec -dr -split 0.5

exp_2:
    just new_set -dra 50
