from pathlib import Path


from ray.util.sgd.utils import BATCH_SIZE
from ray import tune

from fluid.trainer import TorchTrainer
import workloads.common as com
from workloads.common import wlm as workload
from workloads import grid_search_space as space



DATA_PATH, RESULTS_PATH = com.detect_paths()
EXP_NAME = com.remove_prefix(Path(__file__).stem, 'tune_')


def create_grid_search_space(exp_no):
    method_name='space.create_grid_wlm_'+str(exp_no)
    mutations = eval(method_name)()
    return {
        key: tune.sample_from(val)
        for key, val in mutations.items()
    }
 
    
def setup_tune_scheduler(exp_no):
    search_space =  create_grid_search_space(exp_no)
    sync_to_driver = not RESULTS_PATH.startswith('/nfs')

    return dict(
        config=search_space,
        resources_per_trial={
            "gpu": 1
        },
        sync_to_driver=sync_to_driver,
        local_dir=RESULTS_PATH,
        name = EXP_NAME+str(exp_no),
    )
    


def main():
    exp, sd = com.init_ray() 

    MyTrainable = TorchTrainer.as_trainable(
        data_creator=workload.data_creator,
        model_creator=workload.model_creator,
        loss_creator=workload.loss_creator,
        optimizer_creator=workload.optimizer_creator,
        training_operator_cls=workload.WLMOperator,
        config={
            'seed': sd,
            'extra_fluid_trial_resources': {}
        }
    )


    params = {
        # **com.run_options(__file__),
        # 'stop': workload.create_stopper(),
        **setup_tune_scheduler(exp),
    }

    analysis = tune.run(
        MyTrainable,
        stop={"training_iteration": 128},
        **params
    )

    dfs = analysis.trial_dataframes
    for logdir, df in dfs.items():
        ld = Path(logdir)
        df.to_csv(ld / 'trail_dataframe.csv')


if __name__ == '__main__':
    main()
