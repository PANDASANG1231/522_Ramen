import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


def evaluate_performance(all_target, predicted, toplot=True,silent=True, save=None):
    all_target = np.array(all_target)
    predicted = np.array(predicted)
    fpr, tpr, thresholds = roc_curve(all_target, predicted)
    roc_auc = auc(fpr, tpr)
    ks = max(tpr-fpr)
    maxind = (tpr-fpr).argmax()

    event_rate = sum(all_target) / 1.0 / all_target.shape[0]
    cum_total = tpr * event_rate + fpr * (1-event_rate)
    minind, = np.nonzero(np.ravel(abs(cum_total - event_rate) == min(abs(cum_total - event_rate))))
    if minind.shape[0] > 0:
        minind = minind[0]

    if toplot:
        # KS plot
        plt.figure(figsize=(26,6))
        plt.subplot(1,4,1)
        plt.plot(fpr, tpr)
        plt.plot([0,1],[0,1], color='k', linestyle='--', linewidth=2)
        plt.title('KS='+str(round(ks,3))+ ' AUC='+str(round(roc_auc,3)), fontsize=20)
        plt.plot([fpr[maxind], fpr[maxind]], [fpr[maxind], tpr[maxind]], linewidth=4, color='r')
        plt.plot([fpr[minind]], [tpr[minind]], 'k.', markersize=10)

        plt.xlim([0,1])
        plt.ylim([0,1])
        plt.xlabel('False positive', fontsize=20); plt.ylabel('True positive', fontsize=20);
        if not silent:
            print ('KS=' + str(round(ks,3)) + ', AUC=' + str(round(roc_auc,3)) +', N='+str(predicted.shape[0]))
            print ('At threshold=' + str(round(event_rate, 3)) + ', TPR=' + str(round(tpr[minind],3)) + ', ' + str(int(round(tpr[minind]*event_rate*all_target.shape[0]))) + ' out of ' + str(int(round(event_rate*all_target.shape[0]))) ) 
            print ('At threshold=' + str(round(event_rate, 3)) + ', TPR=' + str(round(fpr[minind],3)) + ', ' + str(int(round(fpr[minind]*(1.0-event_rate)*all_target.shape[0]))) + ' out of ' + str(int(round((1.0-event_rate)*all_target.shape[0]))))  
    
        # Score distribution score
        plt.subplot(1,4,2)
        #print predicted.columns
        plt.hist(predicted, bins=20)
        plt.axvline(x=np.mean(predicted), linestyle='--')
        plt.axvline(x=np.mean(all_target), linestyle='--', color='g')
        plt.title('N='+str(all_target.shape[0])+' Tru='+str(round(np.mean(all_target),3))+' Pred='+str(round(np.mean(predicted),3)), fontsize=20)
        plt.xlabel('Target rate', fontsize=20)
        plt.ylabel('Count', fontsize=20)

        # Score average by percentile
        binnum = 10
        ave_predict = np.zeros((binnum))
        ave_target = np.zeros((binnum))
        indices = np.argsort(predicted)
        binsize = int(round(predicted.shape[0]/1.0/binnum))
        for i in range(binnum):
            startind = i*binsize
            endind = min(predicted.shape[0], (i+1)*binsize)
            ave_predict[i] = np.mean(predicted[indices[startind:endind]])
            ave_target[i] = np.mean(all_target[indices[startind:endind]])
        
        plt.subplot(1,4,3)
        plt.plot(ave_predict, 'b.-', label='Prediction', markersize=5)
        plt.plot(ave_target, 'r.-', label='Truth', markersize=5)
        # plt.legend(loc='lower right')
        plt.xlabel('Percentile', fontsize=20)
        plt.ylabel('Target rate', fontsize=20)
        plt.title("Sloping", fontsize=20)
        if not silent:
            print ('Ave_target: ' + str([round(i,4) for i in ave_target]))
            print ('Ave_predicted: ' + str(ave_predict))
            
            
        count_predict = np.zeros((binnum+1))
        count_target = np.zeros((binnum+1))
        indices = np.argsort(predicted,)
        binsize = int(round(predicted.shape[0]/1.0/binnum))
        for i in range(binnum+1):
            endind = min(predicted.shape[0], (i)*binsize)
            count_predict[i] = np.sum(all_target)-np.sum(all_target[indices[0:endind]])
            count_target[i] = np.sum(all_target)
        
        count_predict = list(count_predict)
        count_predict.reverse()
        ave_predict = list((count_predict/count_target))

        top_20_len = int(len(predicted)/5)
        top_20_ratio = np.sum(all_target[indices[-top_20_len:]])*100.0/np.sum(all_target)
        
        btm_10_len = int(len(predicted)/10)
        btm_10_ratio = np.sum(all_target[indices[:btm_10_len]])*100.0/np.sum(all_target)
        
        plt.subplot(1,4,4)
        plt.plot(ave_predict, 'b.-', markersize=5)
        # plt.legend(loc='up right')
        plt.xlabel('Top score bin(bad-->good)', fontsize=20)
        plt.ylabel('Capture rate', fontsize=20)
        plt.title("TOP20:{0}% , BTM10:{1}%".format(round(top_20_ratio,2),round(btm_10_ratio,2)), fontsize=20)
        if not silent:
            print ('#True: ' + str([int(i) for i in count_predict]))
            print ('%True: ' + str([round(i,2) for i in ave_predict]))            
            
        if save is not None:
            plt.savefig(save)
        else:
            plt.show()

    return ks


def mean_std_cross_val_scores(model, X_train, y_train, **kwargs):
    
    scores = cross_validate(model, X_train, y_train, **kwargs)

    mean_scores = pd.DataFrame(scores).mean()
    std_scores = pd.DataFrame(scores).std()
    out_col = []

    for i in range(len(mean_scores)):
        out_col.append((f"%0.3f (+/- %0.3f)" % (mean_scores[i], std_scores[i])))

    return pd.Series(data=out_col, index=mean_scores.index)


def handle_target(x, thresh=3.5):
    
    if x < thresh:
        return 0
    else:
        return 1