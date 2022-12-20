class ARGS():
    def __init__(self):

        self.arch = 'vit_tiny'
        self.patch_size = 8
        self.out_dim = 30000
        self.norm_last_layer = True
        self.momentum_teacher = 0.996
        self.use_bn_in_head = False
        self.warmup_teacher_temp = 0.04
        self.teacher_temp = 0.04
        self.warmup_teacher_temp_epochs = 0
        self.use_fp16 = True
        self.weight_decay = 0.04
        self.weight_decay_end = 0.4
        self.clip_grad = 3.0
        self.batch_size_per_gpu = 16
        self.epochs = 100
        self.freeze_last_layer = 1
        self.lr = 0.0005
        self.warmup_epochs = 10
        self.min_lr = 1e-6
        self.optimizer = 'adamw'
        self.drop_path_rate = 0.1
        self.global_crops_scale = (0.4, 1)
        self.local_crops_number = 8
        self.local_crops_scale = (0.05, 0.4)
        self.data_path = ''
        self.output_dir = ''
        self.saveckp_freq = ''
        self.seed = 12
        self.num_workers = 5
        self.dist_url = 'env://'
        self.local_rank = 0
