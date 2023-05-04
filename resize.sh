

cp -r "$DATASET_PATH" "$DATASET_PATH"_2

pushd "$DATASET_PATH"_2
ls | xargs -P 8 -I {} mogrify -resize 50% {}
popd

cp -r "$DATASET_PATH" "$DATASET_PATH"_4

pushd "$DATASET_PATH"_4
ls | xargs -P 8 -I {} mogrify -resize 25% {}
popd

cp -r "$DATASET_PATH" "$DATASET_PATH"_8

pushd "$DATASET_PATH"_8
ls | xargs -P 8 -I {} mogrify -resize 12.5% {}
popd