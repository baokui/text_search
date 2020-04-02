import sys
import jieba
import tensorflow as tf
import numpy as np
import os
import time
import datetime
import random
from modules import calAUC
from textcnn import TextCNN
from tensorflow.contrib import learn
sys.path.append("../../nlprocess")
from NLProcess import textprocess,getVocab
from Tokenization import Tokenizer
# Data loading params
tf.flags.DEFINE_float("dev_sample_percentage", .1, "Percentage of the training data to use for validation")
tf.flags.DEFINE_string("train_data_file", "./data/train.txt", "Data source for the train data.")
tf.flags.DEFINE_string("test_data_file", "./data/test.txt", "Data source for the test data.")
tf.flags.DEFINE_string("vocab_file", "./data/vocab_char.txt", "Data source for the vocab data.")
tf.flags.DEFINE_string("out_dir", "./cnn-ckpt", "outputdir")

# Model Hyperparameters
tf.flags.DEFINE_integer("sequence_length", 10, "Dimensionality of sentence length (default: 10)")
tf.flags.DEFINE_integer("embedding_dim", 128, "Dimensionality of character embedding (default: 128)")
tf.flags.DEFINE_string("filter_sizes", "3,4,5", "Comma-separated filter sizes (default: '3,4,5')")
tf.flags.DEFINE_integer("num_filters", 128, "Number of filters per filter size (default: 128)")
tf.flags.DEFINE_float("dropout_keep_prob", 0.5, "Dropout keep probability (default: 0.5)")
tf.flags.DEFINE_float("l2_reg_lambda", 0.0, "L2 regularization lambda (default: 0.0)")

# Training parameters
tf.flags.DEFINE_integer("train_batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_integer("num_epochs", 200, "Number of training epochs (default: 200)")
tf.flags.DEFINE_integer("evaluate_every", 200, "Evaluate model on dev set after this many steps (default: 100)")
tf.flags.DEFINE_integer("checkpoint_every", 200, "Save model after this many steps (default: 100)")
tf.flags.DEFINE_integer("log_every", 50, "Save model after this many steps (default: 100)")
tf.flags.DEFINE_integer("num_checkpoints", 5, "Number of checkpoints to store (default: 5)")
# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")


FLAGS = tf.flags.FLAGS
def dataprepro(path_train,path_vocab):
    with open(path_train,'r') as f:
        S = f.read().strip().split('\n')
    S = [s.split('\t') for s in S]
    STrn = [textprocess(s[0]) for s in S]
    vocab = getVocab(STrn,50)
    V = [v[0] for v in vocab]
    with open(path_vocab,'w') as f:
        f.write('\n'.join(V))
def iterData(X,y,batch_size,epoch=20):
    L = [i for i in range(len(X))]
    for _ in range(epoch):
        random.shuffle(L)
        Xr = []
        yr = []
        for i in range(len(L)):
            Xr.append(X[L[i]])
            yr.append(y[L[i]])
            if len(Xr)==batch_size:
                yield Xr,yr
                Xr,yr = [],[]
        yield '__STOP__'
    yield '__RETURN__'
def preprocess():
    # Data Preparation
    # ==================================================
    # Load data
    tokenizer = Tokenizer(FLAGS.vocab_file)
    print("Loading data...")
    with open(FLAGS.train_data_file,'r') as f:
        S = f.read().strip().split('\n')
    S = [s.split('\t') for s in S]
    STrn = [' '.join(list(textprocess(s[0]))) for s in S]
    x_train = [tokenizer.convert_tokens_to_ids(STrn[i],seq_length=FLAGS.sequence_length) for i in range(len(S))]
    y_train = [int(S[i][1]) for i in range(len(S))]
    #y_train = [[int(t == 0), int(t == 1)] for t in y_train]
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    y_train = np.reshape(y_train, (len(y_train), 1))
    with open(FLAGS.test_data_file,'r') as f:
        S = f.read().strip().split('\n')
    S = [s.split('\t') for s in S]
    STrn = [textprocess(s[0]) for s in S]
    x_dev = [tokenizer.convert_tokens_to_ids(STrn[i],seq_length=FLAGS.sequence_length) for i in range(len(S))]
    y_dev = [int(S[i][1]) for i in range(len(S))]
    #y_dev = [[int(t==0),int(t==1)] for t in y_dev]
    x_dev = np.array(x_dev)
    y_dev = np.array(y_dev)
    y_dev = np.reshape(y_dev, (len(y_dev), 1))
    print("Vocabulary Size: {:d}".format(len(tokenizer.vocab)))
    print("Train/Test split: {:d}/{:d}".format(len(y_train), len(y_dev)))
    return x_train, y_train, tokenizer, x_dev, y_dev

def train(x_train, y_train, tokenizer, x_dev, y_dev):
    # Training
    # ==================================================

    with tf.Graph().as_default():
        session_conf = tf.ConfigProto(
          allow_soft_placement=FLAGS.allow_soft_placement,
          log_device_placement=FLAGS.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            cnn = TextCNN(
                sequence_length=x_train.shape[1],
                num_classes=y_train.shape[1],
                vocab_size=len(tokenizer.vocab),
                embedding_size=FLAGS.embedding_dim,
                filter_sizes=list(map(int, FLAGS.filter_sizes.split(","))),
                num_filters=FLAGS.num_filters,
                l2_reg_lambda=FLAGS.l2_reg_lambda)

            # Define Training procedure
            global_step = tf.Variable(0, name="global_step", trainable=False)
            optimizer = tf.train.AdamOptimizer(1e-3)
            grads_and_vars = optimizer.compute_gradients(cnn.loss)
            train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

            # Keep track of gradient values and sparsity (optional)
            grad_summaries = []
            for g, v in grads_and_vars:
                if g is not None:
                    grad_hist_summary = tf.summary.histogram("{}/grad/hist".format(v.name), g)
                    sparsity_summary = tf.summary.scalar("{}/grad/sparsity".format(v.name), tf.nn.zero_fraction(g))
                    grad_summaries.append(grad_hist_summary)
                    grad_summaries.append(sparsity_summary)
            grad_summaries_merged = tf.summary.merge(grad_summaries)

            # Output directory for models and summaries
            timestamp = str(int(time.time()))
            #out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))
            out_dir = FLAGS.out_dir
            print("Writing to {}\n".format(out_dir))

            # Summaries for loss and accuracy
            loss_summary = tf.summary.scalar("loss", cnn.loss)
            acc_summary = tf.summary.scalar("accuracy", cnn.accuracy)

            # Train Summaries
            train_summary_op = tf.summary.merge([loss_summary, acc_summary, grad_summaries_merged])
            train_summary_dir = os.path.join(out_dir, "summaries", "train")
            train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)

            # Dev summaries
            dev_summary_op = tf.summary.merge([loss_summary, acc_summary])
            dev_summary_dir = os.path.join(out_dir, "summaries", "dev")
            dev_summary_writer = tf.summary.FileWriter(dev_summary_dir, sess.graph)

            # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
            checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
            checkpoint_prefix = os.path.join(checkpoint_dir, "model")
            if not os.path.exists(checkpoint_dir):
                os.makedirs(checkpoint_dir)
            saver = tf.train.Saver(tf.global_variables(), max_to_keep=FLAGS.num_checkpoints)

            # Write vocabulary
            #vocab_processor.save(os.path.join(out_dir, "vocab"))

            # Initialize all variables
            sess.run(tf.global_variables_initializer())

            def train_step(x_batch, y_batch):
                """
                A single training step
                """
                feed_dict = {
                  cnn.input_x: x_batch,
                  cnn.input_y: y_batch,
                  cnn.dropout_keep_prob: FLAGS.dropout_keep_prob
                }
                _, step, summaries, loss, accuracy = sess.run(
                    [train_op, global_step, train_summary_op, cnn.loss, cnn.accuracy],
                    feed_dict)
                time_str = datetime.datetime.now().isoformat()
                if step%FLAGS.log_every==0:
                    print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, accuracy))
                    train_summary_writer.add_summary(summaries, step)

            def dev_step(x_batch, y_batch, writer=None):
                """
                Evaluates model on a dev set
                """
                feed_dict = {
                  cnn.input_x: x_batch,
                  cnn.input_y: y_batch,
                  cnn.dropout_keep_prob: 1.0
                }
                step, summaries, loss, accuracy,predict = sess.run(
                    [global_step, dev_summary_op, cnn.loss, cnn.accuracy,cnn.predictions],
                    feed_dict)
                y0 = [np.argmax(tt) for tt in y_batch]
                auc = calAUC(predict, y0)
                time_str = datetime.datetime.now().isoformat()
                print("{}: step {}, loss {:g}, acc {:g}, auc {:g}".format(time_str, step, loss, accuracy,auc))
                if writer:
                    writer.add_summary(summaries, step)

            # Generate batches
            iter = iterData(x_train, y_train, batch_size=FLAGS.train_batch_size, epoch=FLAGS.num_epochs)
            # Training loop. For each batch...
            data = next(iter)
            step = 0
            epoch = 0
            print('training begin')
            while data != '__RETURN__':
                if data == '__STOP__':
                    data = next(iter)
                    epoch += 1
                    continue
                x_batch, y_batch = data
                train_step(x_batch, y_batch)
                data = next(iter)
                current_step = tf.train.global_step(sess, global_step)
                if current_step % FLAGS.evaluate_every == 0:
                    print("\nEvaluation:")
                    dev_step(x_dev, y_dev, writer=dev_summary_writer)
                    print("")
                if current_step % FLAGS.checkpoint_every == 0:
                    path = saver.save(sess, checkpoint_prefix, global_step=current_step)
                    print("Saved model checkpoint to {}\n".format(path))

def main(argv=None):
    x_train, y_train, tokenizer, x_dev, y_dev = preprocess()
    train(x_train, y_train, tokenizer, x_dev, y_dev)

if __name__ == '__main__':
    tf.app.run()