import tensorflow as tf
import modules
import numpy as np
def simple_lr(feature_dim,W=[],b=[]):
    with tf.name_scope('inputs'):
        X_holder = tf.placeholder(tf.float32,shape=[None,feature_dim])
        y_holder = tf.placeholder(tf.float32,shape=[None,1])
        learning_rate = tf.placeholder(tf.float32)
    with tf.name_scope('parameters'):
        #embedding = tf.Variable(np.random.normal(size=(config.vocab_size, config.embeds)))
        if len(W)==0:
            Weights = tf.Variable(tf.zeros([feature_dim, 1]))
            biases = tf.Variable(tf.zeros([1, 1]))
        else:
            Weights = tf.Variable(W)
            biases = tf.Variable(b)
        threshold = tf.constant(value=0.5)
    with tf.name_scope('inference'):
        #X0 = tf.nn.embedding_lookup(embedding, X_holder0)
        #X = tf.concat([tf.cast(X0,tf.float32),X_holder1],axis=-1)
        logits = tf.matmul(X_holder, Weights) + biases
        # dense1 = tf.layers.dense(inputs=X_holder, units=128, activation=tf.nn.relu)
        #logits = tf.layers.dense(inputs=X, units=1, activation=None)
    with tf.name_scope('outputs_loss'):
        predict_y = tf.nn.sigmoid(logits)
        #c = tf.square(predict_y - y_holder)
        #loss = tf.reduce_mean(c)
        loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=y_holder))
    with tf.name_scope('train_op'):
        '''
        optimizer = modules.create_optimizer(init_learning_rate=config.init_learning_rate,
                                             end_learning_rate=config.end_learning_rate,
                                             warmup_steps=int(
                                                 config.epochs * config.nb_examples * 0.01 / config.batch_size),
                                             decay_steps=int(
                                                 config.epochs * config.nb_examples * 0.99 / config.batch_size))
        '''
        optimizer = tf.train.GradientDescentOptimizer(learning_rate)
        tvars = tf.trainable_variables()
        # grads, _ = tf.clip_by_global_norm(tf.gradients(loss, tvars), config.clip_grad)
        grads = optimizer.compute_gradients(loss, var_list=tf.get_collection(
            tf.GraphKeys.TRAINABLE_VARIABLES,
            scope='parameters'
        ))
        train_op = optimizer.minimize(loss)
        # train_op = optimizer.apply_gradients(zip(grads, tvars))
        correct_prediction = tf.squeeze(tf.equal(tf.cast(tf.greater(predict_y,threshold),dtype=tf.int32), tf.cast(y_holder,dtype=tf.int32)),axis=-1)
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        return X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy
def simple_svm(config):
    with tf.name_scope('inputs'):
        X_holder = tf.placeholder(tf.float32, shape=[config.batch_size, config.feature_dim])
        y_holder = tf.placeholder(tf.float32, shape=[config.batch_size, 1])
        learning_rate = tf.placeholder(tf.float32)
    with tf.name_scope('parameters'):
        # embedding = tf.Variable(np.random.normal(size=(config.vocab_size, config.embeds)))
        Weights = tf.Variable(tf.zeros([config.feature_dim, 1]))
        biases = tf.Variable(tf.zeros([1, 1]))
        threshold = tf.constant(value=0.5)
    with tf.name_scope('inference'):
        logits = tf.subtract(tf.matmul(X_holder, Weights), biases)
        predict_y_0 = (logits+1)/2
    with tf.name_scope('outputs_loss'):
        # Declare vector L2 'norm' function squared
        # predict_y = tf.maximum(0., tf.multiply(logits, y_holder))
        predict_y = tf.cast(tf.greater(logits, 0.0), dtype=tf.int32)
        l2_norm = tf.reduce_sum(tf.square(Weights))
        # Loss = max(0, 1-pred*actual) + alpha * L2_norm(A)^2
        alpha = tf.constant(0.01)
        classification_term = tf.reduce_mean(tf.maximum(0., tf.subtract(1., tf.multiply(logits, 2*y_holder-1))))

        loss = tf.add(classification_term, tf.multiply(alpha, l2_norm))
    with tf.name_scope('train_op'):
        optimizer = tf.train.GradientDescentOptimizer(0.05)
        grads = optimizer.compute_gradients(loss, var_list=tf.get_collection(
            tf.GraphKeys.TRAINABLE_VARIABLES,
            scope='parameters'
        ))
        train_op = optimizer.minimize(loss)
        # train_op = optimizer.apply_gradients(zip(grads, tvars))
        correct_prediction = tf.squeeze(tf.equal(predict_y, tf.cast(y_holder,dtype=tf.int32)),axis=-1)
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        return X_holder, y_holder, learning_rate, predict_y_0, loss, optimizer, train_op, grads, accuracy
def simple_lr_dense(config):
    with tf.name_scope('inputs'):
        X_holder = tf.placeholder(tf.float32,shape=[None,config.feature_dim])
        y_holder = tf.placeholder(tf.float32,shape=[None,1])
        learning_rate = tf.placeholder(tf.float32)
    with tf.name_scope('parameters'):
        #embedding = tf.Variable(np.random.normal(size=(config.vocab_size, config.embeds)))
        Weights = tf.Variable(tf.zeros([config.hiddenSize, 1]))
        biases = tf.Variable(tf.zeros([1, 1]))
        threshold = tf.constant(value=0.5)
    with tf.name_scope('inference'):
        dense1 = tf.layers.dense(inputs=X_holder, units=config.hiddenSize, activation=tf.nn.sigmoid)
        dense2 = tf.nn.dropout(dense1, config.keep_prob)
        logits = tf.matmul(dense2, Weights) + biases
        # dense1 = tf.layers.dense(inputs=X_holder, units=128, activation=tf.nn.relu)
        #logits = tf.layers.dense(inputs=X, units=1, activation=None)
    with tf.name_scope('outputs_loss'):
        predict_y = tf.nn.sigmoid(logits)
        #c = tf.square(predict_y - y_holder)
        #loss = tf.reduce_mean(c)
        loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=y_holder))
    with tf.name_scope('train_op'):
        '''
        optimizer = modules.create_optimizer(init_learning_rate=config.init_learning_rate,
                                             end_learning_rate=config.end_learning_rate,
                                             warmup_steps=int(
                                                 config.epochs * config.nb_examples * 0.01 / config.batch_size),
                                             decay_steps=int(
                                                 config.epochs * config.nb_examples * 0.99 / config.batch_size))
        '''
        optimizer = tf.train.GradientDescentOptimizer(learning_rate)
        tvars = tf.trainable_variables()
        # grads, _ = tf.clip_by_global_norm(tf.gradients(loss, tvars), config.clip_grad)
        grads = optimizer.compute_gradients(loss, var_list=tf.get_collection(
            tf.GraphKeys.TRAINABLE_VARIABLES,
            scope='parameters'
        ))
        train_op = optimizer.minimize(loss)
        # train_op = optimizer.apply_gradients(zip(grads, tvars))
        correct_prediction = tf.squeeze(tf.equal(tf.cast(tf.greater(predict_y,threshold),dtype=tf.int32), tf.cast(y_holder,dtype=tf.int32)),axis=-1)
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        return X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy
if __name__ == '__main__':
    pass