from torch.utils.data import DataLoader

from models.sgan.data.trajectories import TrajectoryDataset, seq_collate

def data_loader(args, path, phase='train'):
    dset = TrajectoryDataset(
        path,
        obs_len=args.obs_len,
        pred_len=args.pred_len,
        skip=args.skip,
        delim=args.delim)

    if phase == 'train':
        loader = DataLoader(
            dset,
            batch_size=args.batch_size,
            shuffle=True,
            num_workers=args.loader_num_workers,
            collate_fn=seq_collate)
    else:
        loader = DataLoader(
            dset,
            batch_size=args.batch_size,
            shuffle=False,
            num_workers=args.loader_num_workers,
            collate_fn=seq_collate)
    return dset, loader
