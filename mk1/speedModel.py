from matplotlib import pyplot as plt

mSpeed = 500
minSpeed = 100
totalSteps = 2000

currentStep = range(0, totalSteps)
x = [v for v in currentStep]
y = [v for v in currentStep]
y = [
    mSpeed -
    (4 *
     (mSpeed - minSpeed)) / pow(totalSteps, 2) * pow(v - totalSteps / 2, 2)
    for v in y
]

plt.plot(x, y)
plt.show()
