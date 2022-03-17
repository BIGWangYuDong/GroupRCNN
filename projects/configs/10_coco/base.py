samples_per_gpu = 2
workers_per_gpu = 5
eval_interval = 12

full_ann_ratio = 0.1

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(
        type='AutoAugment',
        policies=[
            [
                dict(type='Resize',
                     img_scale=[(480, 1333), (512, 1333), (544, 1333),
                                (576, 1333), (608, 1333), (640, 1333),
                                (672, 1333), (704, 1333), (736, 1333),
                                (768, 1333), (800, 1333)],
                     multiscale_mode='value',
                     keep_ratio=True)
            ],
            [
                dict(type='Resize',
                     img_scale=[(400, 1333), (500, 1333), (600, 1333)],
                     multiscale_mode='value',
                     keep_ratio=True),
                # process points annotation
                dict(type='PointRandomCrop',
                     crop_type='absolute_range',
                     crop_size=(384, 600),
                     allow_negative_crop=False),
                dict(type='Resize',
                     img_scale=[(480, 1333), (512, 1333), (544, 1333),
                                (576, 1333), (608, 1333), (640, 1333),
                                (672, 1333), (704, 1333), (736, 1333),
                                (768, 1333), (800, 1333)],
                     multiscale_mode='value',
                     override=True,
                     keep_ratio=True)
            ]
        ]),
    dict(type='Normalize',
         mean=[123.675, 116.28, 103.53],
         std=[58.395, 57.12, 57.375],
         to_rgb=True),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'])
]
data = dict(
    samples_per_gpu=samples_per_gpu,
    workers_per_gpu=workers_per_gpu,
    train=dict(type='PointCocoDataset',
               full_ann_ratio=0.1,
               ann_file='data/coco/annotations/instances_train2017.json',
               img_prefix='data/coco/train2017/',
               pipeline=train_pipeline),
    val=dict(type='PointCocoDataset',
             ann_file='data/coco/annotations/instances_val2017.json',
             img_prefix='data/coco/val2017/',
             pipeline=[
                 dict(type='LoadImageFromFile'),
                 dict(type='LoadAnnotations', with_bbox=True),
                 dict(type='MultiScaleFlipAug',
                      img_scale=(1333, 800),
                      flip=False,
                      transforms=[
                          dict(type='Resize', keep_ratio=True),
                          dict(type='RandomFlip'),
                          dict(type='Normalize',
                               mean=[123.675, 116.28, 103.53],
                               std=[58.395, 57.12, 57.375],
                               to_rgb=True),
                          dict(type='Pad', size_divisor=32),
                          dict(type='DefaultFormatBundle'),
                          dict(type='Collect',
                               keys=['img', 'gt_bboxes', 'gt_labels'])
                      ])
             ]),
    test=dict(type='PointCocoDataset',
              ann_file='data/coco/annotations/instances_train2017.json',
              img_prefix='data/coco/train2017/',
              pipeline=[
                  dict(type='LoadImageFromFile'),
                  dict(type='LoadAnnotations', with_bbox=True),
                  dict(type='MultiScaleFlipAug',
                       img_scale=(1333, 800),
                       flip=False,
                       transforms=[
                           dict(type='Resize', keep_ratio=True),
                           dict(type='RandomFlip'),
                           dict(type='Normalize',
                                mean=[123.675, 116.28, 103.53],
                                std=[58.395, 57.12, 57.375],
                                to_rgb=True),
                           dict(type='Pad', size_divisor=32),
                           dict(type='DefaultFormatBundle'),
                           dict(type='Collect',
                                keys=['img', 'gt_bboxes', 'gt_labels'])
                       ])
              ]))
evaluation = dict(interval=eval_interval, metric='bbox')
optimizer = dict(type='SGD', lr=0.02, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=dict(max_norm=35, norm_type=2))
lr_config = dict(policy='step',
                 warmup='linear',
                 warmup_iters=500,
                 warmup_ratio=0.001,
                 step=[16, 22])
runner = dict(type='EpochBasedRunner', max_epochs=24)
checkpoint_config = dict(interval=24)
log_config = dict(interval=50, hooks=[dict(type='TextLoggerHook')])
custom_hooks = [dict(type='NumClassCheckHook')]
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = None
resume_from = None
workflow = [('train', 1)]
work_dir = './work_dirs/cascade_rcnn_r50_fpn_1x_coco'
gpu_ids = range(0, 1)
