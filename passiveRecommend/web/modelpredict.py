from modules import getFeature,calAUC
from modeling import simple_lr,simple_lr_dense
import tensorflow as tf
def getModel(config_train,config_predict):
    mode = config_predict.mode
    path_ckpt = config_predict.path_ckpt
    if 'dense' in mode:
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr_dense(
            config_train)
    else:
        X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy = simple_lr(
            config_train.feature_dim)
    global_step = tf.train.get_or_create_global_step()
    train_op = tf.group(train_op, [tf.assign_add(global_step, 1)])
    saver = tf.train.Saver(max_to_keep=10)
    session = tf.Session()
    ckpt_file = tf.train.latest_checkpoint(path_ckpt)
    saver.restore(session, ckpt_file)
    return X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy,session
def predicting(inputStr, config_feature, X_holder, y_holder, learning_rate, predict_y,session,thr = 0.5):
    learning_rate_ = 0
    x0_test = [getFeature(inputStr, config_feature)]
    y_p0 = session.run(predict_y,
                       feed_dict={X_holder: x0_test, learning_rate: learning_rate_})
    p = y_p0[0][0]
    y = int(p>thr)
    return p,y
def predict(inputStr,words,config,w2v):
    x = getFeature(inputStr, words, config,w2v)
    w = config['weight_w']
    b = config['weight_b']
    logits = sum([w[i]*x[i] for i in range(len(w))])+b
    p = 1/(1+np.exp(-logits))
    return p
