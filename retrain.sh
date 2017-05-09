#build the retrainer
bazel build tensorflow/examples/image_retraining:retrain

#retrain the last layer of Inception model
bazel-bin/tensorflow/examples/image_retraining/retrain --image_dir ~/images/training_images/ --output_graph ~/results/output_graph.pb --output_labels ~/results/output_labels.txt --bottleneck_dir ~/results/bottleneck --summaries_dir ~/results/retrain_logs