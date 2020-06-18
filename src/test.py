import time
from model import * 
from contextlib import redirect_stdout

nowtime = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))

# now = time.localtime()
# print(time.strftime('%Y%m%d_%H%M', time.localtime(time.time())))
# f = open(f"models/{nowtime}_log.txt", 'w')
# f.write(model.summary)
# f.close()

# print(model.summary())
# summary = str(model.summary())

with open('models/modelsummary.txt', 'w') as f:
    f.write("batch_size: %s\n" %batch_size)
    f.write("num_epoch: %s \n\n" %num_epoch)

    with redirect_stdout(f):
        model.summary()