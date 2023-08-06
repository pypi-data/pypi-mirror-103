import os
import re
import pickle
import pathlib
import sys
import io
from http.server import BaseHTTPRequestHandler, HTTPServer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.metrics import roc_curve, auc, precision_recall_curve,f1_score,confusion_matrix

def roc(y, ypred, font_ch=False):
    fpr, tpr, threshold = roc_curve(y, ypred)
    roc_auc = auc(fpr, tpr)
    plt.title('ROC Curve (AUC = %0.5f)' % roc_auc)
    plt.plot(fpr, tpr, drawstyle="steps-post")
    plt.plot([0, 1], [0, 1], 'k--', lw=1)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    if font_ch:
        plt.xlabel('假阳性率', fontproperties=FontProperties(fname=get_font()))
        plt.ylabel("真阳性率", fontproperties=FontProperties(fname=get_font()))
    else:
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
    plt.grid(True)
    plt.show()
def plot_confusion_matrix(y_true, y_pred, labels):
    cmap = plt.cm.pink
    cm = confusion_matrix(y_true, y_pred)
    tick_marks = np.array(range(len(labels))) + 0.5
    np.set_printoptions(precision=2)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.figure(figsize=(4, 4), dpi=120)
    ind_array = np.arange(len(labels))
    x, y = np.meshgrid(ind_array, ind_array)
    intFlag = 1 # 标记在图片中对文字是整数型还是浮点型
    for x_val, y_val in zip(x.flatten(), y.flatten()):
        #

        if (intFlag):
            c = cm[y_val][x_val]
            plt.text(x_val, y_val, "%d" % (c,), color='red', fontsize=8, va='center', ha='center')

        else:
            c = cm_normalized[y_val][x_val]
            if (c > 0.01):
                #这里是绘制数字，可以对数字大小和颜色进行修改
                plt.text(x_val, y_val, "%0.2f" % (c,), color='red', fontsize=7, va='center', ha='center')
            else:
                plt.text(x_val, y_val, "%d" % (0,), color='red', fontsize=7, va='center', ha='center')
    if(intFlag):
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
    else:
        plt.imshow(cm_normalized, interpolation='nearest', cmap=cmap)

    plt.gca().xaxis.set_label_position('bottom')
    plt.gca().xaxis.tick_bottom()
    plt.gca().invert_yaxis()
    plt.gca().set_xticks(tick_marks, minor=True)
    plt.gca().set_yticks(tick_marks, minor=True)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.colorbar()
    xlocations = np.array(range(len(labels)))
    plt.xticks(xlocations, labels, rotation=90)
    plt.yticks(xlocations, labels)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.grid(False)
    plt.tight_layout()
#     plt.title('Confusion Matrix', y=-0.1)
    plt.show()

class TableDataModel(object):
    def __init__(self):
        super(TableDataModel, self).__init__()

    def train(self, df):
        self.put_model_init()

    def predict(self, df):
        self.get_model_init()

    def load_train_data(self):
        pass

    def get_model_path(self):
        path = 'model' #self.params.modelPath
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def save_model_pkl(self):
        save_path = os.path.join(self.get_model_path(), "model.pkl")
        print("Saving model in " + save_path)
        with open(save_path, 'wb') as f:
            pickle.dump(self.models, f)

    def load_model_pkl(self):
        save_path = os.path.join(self.get_model_path(), "model.pkl")
        print("Loading model in " + save_path)
        with open(save_path, 'rb') as f:
            self.models = pickle.load(f)

    def put_model(self, obj):
        self.models[self.put_model_index] = obj
        self.put_model_index += 1

    def get_model(self):
        obj = self.models[self.get_model_index]
        self.get_model_index += 1
        return obj

    def put_model_init(self):
        self.models = {}
        self.put_model_index = 0

    def get_model_init(self):
        self.get_model_index = 0

    def print_model(self):
        display({k:type(v) for k,v in self.models.items()})

    def run(self, run_mode):
        if run_mode=='train':
            train_data = self.load_train_data()
            df = train_data['data']
            label = train_data['label']

            # 训练验证划分
            train, test = train_test_split(df, test_size = 0.2, random_state = 2021)
            train = train.reset_index(drop=True)
            test = test.reset_index(drop=True)

            feature = [col for col in train.columns if col not in [label]]
            test_X,test_y = test[feature], test[label]

            model = self

            model.train(train)
            model.save_model_pkl()

            model.load_model_pkl()
            results = model.predict(test_X)

            roc(test_y, results.loc[:,1])
            plot_confusion_matrix(test_y, np.argmax(results.to_numpy(), axis=1), [0,1])

        elif run_mode=='predict_online':
            model = self
            model.run_service()

    def run_service(self):
        model = self

        class handler(BaseHTTPRequestHandler):
            def do_POST(self):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
                post_data = self.rfile.read(content_length).decode('utf-8') # <--- Gets the data itself
                # display("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data)

                sio = io.StringIO(post_data)
                df = pd.read_csv(sio)
                # display(df.info())

                results = model.predict(df)
                s = io.StringIO()
                results.to_csv(s, index=False, header=False, encoding='utf-8-sig')
                message = s.getvalue()

                self.wfile.write(bytes(message, "utf8"))

        self.load_model_pkl()
        port = 8501
        with HTTPServer(('', port), handler) as server:
            print('Serving on port %d' % (port))
            server.serve_forever()
