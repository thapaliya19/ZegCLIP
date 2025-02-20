# dataset settings
dataset_type = "ImageTextMaskDataset"

img_dir = "/mnt/Enterprise/safal/VLM-SEG-2023/CRIS.pytorch/datasets/images/chexlocalize_no_train/"
ann_dir = "/mnt/Enterprise/safal/VLM-SEG-2023/CRIS.pytorch/datasets/masks/chexlocalize_no_train/"

img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True
)
crop_size = (512, 512)

prompt_type = "p0"

class_names = ["background", "chest_pathology"]

prompt_file = "/mnt/Enterprise/safal/VLM-SEG-2023/CRIS.pytorch/datasets/anns/chexlocalize_no_train/testA.json"

train_pipeline = [
    dict(type="LoadImageFromFile"),
    dict(type="LoadAnnotations", reduce_zero_label=True),
    dict(type="Resize", img_scale=(2048, 512), ratio_range=(0.5, 2.0)),
    dict(type="RandomCrop", crop_size=crop_size, cat_max_ratio=0.75),
    dict(type="RandomFlip", prob=0.5),
    dict(type="PhotoMetricDistortion"),
    dict(type="Normalize", **img_norm_cfg),
    dict(type="Pad", size=crop_size, pad_val=0, seg_pad_val=255),
    dict(type="DefaultFormatBundle"),
    dict(type="CustomCollect", keys=["img", "gt_semantic_seg"]),
]
test_pipeline = [
    dict(type="LoadImageFromFile"),
    dict(
        type="MultiScaleFlipAug",
        img_scale=(2048, 512),
        flip=False,
        transforms=[
            dict(type="Resize", keep_ratio=True, min_size=512),
            dict(type="Normalize", **img_norm_cfg),
            dict(type="ImageToTensor", keys=["img"]),
            dict(
                type="CustomCollect",
                keys=["img"],
            ),
        ],
    ),
]
data = dict(
    samples_per_gpu=4,
    workers_per_gpu=4,
    train=dict(
        type=dataset_type,
        prompt_type=prompt_type,
        img_dir=img_dir,
        ann_dir=ann_dir,
        pipeline=train_pipeline,
        prompt_file=prompt_file,
        class_names=class_names,
    ),
    val=dict(
        type=dataset_type,
        prompt_type=prompt_type,
        img_dir=img_dir,
        ann_dir=ann_dir,
        pipeline=test_pipeline,
        prompt_file=prompt_file,
        class_names=class_names,
    ),
    test=dict(
        type=dataset_type,
        prompt_type=prompt_type,
        img_dir=img_dir,
        ann_dir=ann_dir,
        pipeline=test_pipeline,
        prompt_file=prompt_file,
        class_names=class_names,
    ),
)
