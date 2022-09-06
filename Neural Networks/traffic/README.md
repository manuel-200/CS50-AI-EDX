Initially, with a dropout of 0.5, the neural network was really inaccurate (0.0581) and therefore, the dropout was decreased to 0.2. With a 0.2 dropout, the accuracy increased to 0.8893 and although we could keep decreasing the dropout and increasing the accuracy, it was left in 0.2 for avoiding overfitting problems. The filters used were also modified, and it was found that as less filters were used, the accuracy improved. As 64 filters decreased the accuracy to 0.0572 and decreasing the filters icreased the accuracy, the filters were changed from 32 to 16. 

On the other side, layers were also modified to find better results. The pooling layer was changed from max to average but it was found that it decreased the accuracy from 0.9034 to 0.8822 so it was left on max. Different number of layers were also tested, and it was found that as more convolution layers were added, the accuracy increased. Using two layers increased the accuracy from 0.9034 to 0.9604. Pooling layers had the opposite effect, as the number of layers increased, the accuracy decreased. Two pooling layers decreased the accuracy from 0.9604 to 0.5918. Different convention of layers were also tested, such as Convolutional + pooling + Convolutional + pooling and Convolutional + pooling + Convolutional. It was found that Convolutional + pooling + Convolutional had a better accuracy that the simple Convolutional + pooling combination and was better that C + P +C +P, with an accuracy of 0.9614. Therefore, this combination was chosen. Then, the number of hidden layers were modified. It was found that as more layers, the accuracy increased. Although the accuracy increased, the increased was really small and could cause overfitting. It was also found that reducing this layers had a big impact, as changing the hidden layers from 128 to 64 changed the accuracy from 0.9614 to 0.8944. Because of this tests, it was decided to leave 128 layers. Finally, pooling and convolution sizes were changed. It was found decreasing and increasing convolution size (initially in 3x3), caused the accuracy to decrease. On the other side, increasing the pooling layer (initially 2x2) also decreased the accuracy. Because of this, the sizes were left to their initial values.

The final neural network parameters can be observed on the code. The results can be seen below.

RESULTS:

- Dropout:
    - 0.5 = 0.0581
    - 0.2 = 0.8893
    - 0.1 = 0.9159

- Filters:
    - 16 = 0.9034
    - 32 = 0.8893
    - 64 = 0.0572

- Pooling layer
    - Max = 0.9034
    - Average = 0.8822

- Convolution:
    - 1 layer = 0.9034
    - 2 layer = 0.9604
    - 3 layer = 0.9809

- Pooling:
    - 1 layer = 0.9604
    - 2 layer = 0.5918



- Conv + pool:
    - C + P = 0.9034
    - C + P + C + P = 0.9452
    - C + P + C = 0.9614

- Hidden layers:
    - 1 x 128 = 0.9614
    - 1 x 64 = 0.8944
    - 1 x 256 = 0.9732
    - 2 x 128 = 0.9702
    - 1 x 128 / 1 x 64 = 0.9615

- Conv size:
    - 3x3 = 0.9614
    - 2x2 = 0.9436
    - 5x5 = 0.9543

- Pooling size:
    - 2x2 = 0.9614
    - 3x3 = 0.9551
    - 5x5 = 0.8908



