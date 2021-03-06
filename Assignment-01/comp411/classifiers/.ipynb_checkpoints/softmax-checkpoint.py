from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg, regtype='L2'):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength
    - regtype: Regularization type: L1 or L2

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization! Implement both L1 and L2 regularization based on the      #
    # parameter regtype.                                                        #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    scores = np.matmul(X, W)
    num_train = X.shape[0]
    num_classes = W.shape[1]

    for i in range(num_train):
      
      score = scores[i]
      score -= np.max(score)
      softmax_term = np.exp(score) / np.sum(np.exp(score))
      loss += -np.log(softmax_term[y[i]])
    
      for j in range(num_classes):
        dW[:,j] += softmax_term[j] * X[i]
      dW[:,y[i]] -= X[i]

    
    #average loss and grad
    loss = loss / num_train
    dW = dW / num_train

    #regularization 
    if regtype == "L1":
      regularization = np.sum(np.absolute(W)) * reg
      grad_reg =  (W > 1)
    elif regtype == "L2":
      regularization = np.sum(W * W) * reg
      grad_reg = 2 * reg * W
    
    dW += grad_reg
    loss += regularization

    


    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg, regtype='L2'):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization! Implement both L1 and L2 regularization based on the      #
    # parameter regtype.                                                        #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_train = X.shape[0]
    
    scores = np.matmul(X, W)
    max_of_scores = np.max(scores, axis=1, keepdims=True)
    scores -= max_of_scores
    softmax_term = np.exp(scores) / np.sum(np.exp(scores), axis=1, keepdims=True)
    
    loss = np.sum(-np.log(softmax_term[np.arange(num_train), y]))
    softmax_term[np.arange(num_train),y] -= 1
    dW = np.matmul(X.T, softmax_term)

    #average loss and grad
    loss = loss / num_train
    dW = dW / num_train

    #regularization 
    if regtype == "L1":
      regularization = np.sum(np.absolute(W)) * reg
      grad_reg = reg * (W > 0)
    else:
      regularization = np.sum(W * W) * reg
      grad_reg = 2 * reg * W

    loss += regularization
    dW += grad_reg
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
