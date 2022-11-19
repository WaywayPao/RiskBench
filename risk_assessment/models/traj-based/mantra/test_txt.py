import argparse
import evaluate_txt
import evaluate_batch
import mantra
import multiprocessing as mp
import sys
import threading as td

def parse_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cuda", default=True)
    parser.add_argument("--batch_size", type=int, default=256)
    parser.add_argument("--past_len", type=int, default=20)
    parser.add_argument("--future_len", type=int, default=30)
    parser.add_argument("--preds", type=int, default=1)

    parser.add_argument("--model", default='pretrained_models/MANTRA/model_MANTRA')
    parser.add_argument("--visualize_dataset", default=False)
    parser.add_argument("--saved_memory", default=True)
    parser.add_argument("--memories_path", default='pretrained_models/MANTRA/memories/')
    parser.add_argument("--withIRM", default=False, help='generate predictions with/without IRM')
    parser.add_argument("--saveImages", default='None',
                        help=
                        '''
                        Save in test folder examples of dataset with predictions generated by MANTRA.
                        If None, it does not save anything.
                        If 'All', it saves all examples.
                        If 'Subset', it saves examples defined in index_qualitative.py (handpicked significant samples)
                        ''')

    parser.add_argument("--dataset_file", default="", help="dataset file")
    parser.add_argument("--info", type=str, default='', help='Name of evaluation. '
                                                             'It will use for name of the test folder.')
    return parser.parse_args()

def multi(config, core):
    v = evaluate_batch.Validator(config)
    #v = evaluate_txt.Validator(config)
    v.test_model(core)

def main(config):
    #cpu_count = mp.cpu_count() #16
    cpu_count = 1
    process_list = []
    print(cpu_count)
    for i in range(cpu_count):
        #process_list.append(td.Thread(target = multi, args = (config, i + 1)))
        process_list.append(mp.Process(target = multi, args = (config, i + 1)))
        process_list[i].start()
    for i in range(cpu_count):
        process_list[i].join()
    #v = evaluate_txt.Validator(config)
    #print('start evaluation')
    #v.test_model()


if __name__ == "__main__":
    config = parse_config()
    main(config)
