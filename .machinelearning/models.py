import nn


class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.weight = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.weight

    def run(self, x):
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.weight, x)

    def get_prediction(self, x):
        "*** YOUR CODE HERE ***"
        if nn.as_scalar(self.run(x)) >= 0.0:
            return 1
        else:
            return -1

    def train(self, dataset):
        "*** YOUR CODE HERE ***"
        while True:
            flag = True
            for x, y in dataset.iterate_once(1):
                y = nn.as_scalar(y)
                if self.get_prediction(x) != y:
                    flag = False
                    self.weight.update(x, y)
            if flag:
                break


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """

    def __init__(self):
        "*** YOUR CODE HERE ***"

        self.hlayer1 = 50
        self.w1 = nn.Parameter(1, self.hlayer1)
        self.b1 = nn.Parameter(1, self.hlayer1)

        self.hlayer2 = 30
        self.w2 = nn.Parameter(self.hlayer1, self.hlayer2)
        self.b2 = nn.Parameter(1, self.hlayer2)

        self.w3 = nn.Parameter(self.hlayer2, 1)
        self.b3 = nn.Parameter(1, 1)

    def run(self, x):
        """
        Runs the model for a batch of examples.
        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"

        linear = nn.Linear(x, self.w1)
        bias = nn.AddBias(linear, self.b1)
        relu = nn.ReLU(bias)
        second = nn.ReLU(
            nn.AddBias(nn.Linear(relu, self.w2), self.b2))
        third = nn.AddBias(nn.Linear(second, self.w3), self.b3)
        return third

    def get_loss(self, x, y):
        check = self.run(x)
        return nn.SquareLoss(check, y)
        ""

    def train(self, dataset):
        while True:
            batch = 4
            rate = -0.05
            for (x, y) in dataset.iterate_once(batch):
                loss = self.get_loss(x, y)
                result = nn.gradients(
                    loss,
                    [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3])
                self.w1.update(result[0], rate)
                self.b1.update(result[1], rate)
                self.w2.update(result[2], rate)
                self.b2.update(result[3], rate)
                self.w3.update(result[4], rate)
                self.b3.update(result[5], rate)
            if nn.as_scalar(loss) < 0.002:
                break


class DigitClassificationModel(object):
    def __init__(self):
        self.size_input = 784
        self.size_output = 10

        self.hlayer1 = 200
        self.w1 = nn.Parameter(self.size_input,  self.hlayer1)
        self.b1 = nn.Parameter(1,  self.hlayer1)

        self.hlayer2 = 100
        self.w2 = nn.Parameter(self.hlayer1,  self.hlayer2)
        self.b2 = nn.Parameter(1, self.hlayer2)

        self.w3 = nn.Parameter(self.hlayer2, self.size_output)
        self.b3 = nn.Parameter(1, self.size_output)

    def run(self, x):
        l1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        l2 = nn.ReLU(nn.AddBias(nn.Linear(l1, self.w2), self.b2))
        l3 = nn.AddBias(nn.Linear(l2, self.w3), self.b3)

        return l3

    def get_loss(self, x, y):
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        rate = -0.06
        while True:
            for x, y in dataset.iterate_once(50):
                loss = self.get_loss(x, y)
                grad = nn.gradients(loss, [
                    self.w1, self.w2, self.w3, self.b1, self.b2, self.b3
                ])
                self.w1.update(grad[0], rate)
                self.w2.update(grad[1], rate)
                self.w3.update(grad[2], rate)
                self.b1.update(grad[3], rate)
                self.b2.update(grad[4], rate)
                self.b3.update(grad[5], rate)
            if dataset.get_validation_accuracy() >= 0.975:
                return


class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """

    def __init__(self):
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        self.iw = nn.Parameter(self.num_chars, 256)
        self.ib = nn.Parameter(1, 256)
        self.wx = nn.Parameter(self.num_chars, 256)
        self.hw = nn.Parameter(256, 256)
        self.b = nn.Parameter(1, 256)
        self.outw = nn.Parameter(256, len(self.languages))
        self.outb = nn.Parameter(1, len(self.languages))

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        h_i = nn.ReLU(nn.AddBias(nn.Linear(xs[0], self.iw), self.ib))
        for char in xs[1:]:
            h_i = nn.ReLU(nn.AddBias(nn.Add(nn.Linear(char, self.wx), nn.Linear(h_i, self.hw)), self.b))
        output = nn.AddBias(nn.Linear(h_i, self.outw), self.outb)
        return output

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.
        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.
        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        y_hat = self.run(xs)
        return nn.SoftmaxLoss(y_hat, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        rate = -0.1
        batch_size = 10
        while True:
            for x, y in dataset.iterate_once(batch_size):
                if dataset.get_validation_accuracy() >= 0.89:
                    return
                loss = self.get_loss(x, y)
                gradParams = nn.gradients(loss, [self.iw, self.ib, self.wx,
                                          self.hw, self.b, self.outw, self.outb])

                self.iw.update(gradParams[0], rate)
                self.ib.update(gradParams[1], rate)
                self.wx.update(gradParams[2], rate)
                self.hw.update(gradParams[3], rate)
                self.b.update(gradParams[4], rate)
                self.outw.update(gradParams[5], rate)
                self.outb.update(gradParams[6], rate)
