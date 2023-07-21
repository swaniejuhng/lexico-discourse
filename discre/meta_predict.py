import discourseParsing.DiscourseParser as DP
import discourseParsing.utils.SenseLabeller as SL
import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import csv
import pickle
import time
import math
import numpy as np
import argparse

def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)



def iteration(is_cuda, msg_id, word_seqs, tr_meta, tr_inst, tr_imipl, loss_fn, optim, model, training):
    for trainer_id, case, disCon, arg1Idx, arg2Idx in tr_meta[msg_id]:
        
        explicitInstances=tr_inst[trainer_id]['explicit']
        implicitInstances=tr_inst[trainer_id]['implicit']
        # explicit relation training
        explicit_loss = None
        implicit_loss = None
        explicit_losses_i=0
        implicit_losses_i=0
        if explicitInstances:
            model.zero_grad()
            class_vec, type_vec, subtype_vec, relation_vec = model((case, disCon, arg1Idx, arg2Idx),word_seqs[msg_id])
            for label, weight in explicitInstances['class']:
                if is_cuda:
                    label = label.cuda()
                loss = weight * loss_fn(class_vec, label)
                explicit_losses_i += float(loss)
                if explicit_loss:
                    explicit_loss += loss
                else:
                    explicit_loss = loss

            for label, weight in explicitInstances['type']:
                if is_cuda:
                    label = label.cuda()
                loss = weight * loss_fn(type_vec, label)
                explicit_losses_i += float(loss)
                if explicit_loss:
                    explicit_loss += loss
                else:
                    explicit_loss = loss

            for label, weight in explicitInstances['subtype']:
                if is_cuda:
                    label = label.cuda()
                loss = weight * loss_fn(subtype_vec, label)
                explicit_losses_i += float(loss)
                if explicit_loss:
                    explicit_loss += loss
                else:
                    explicit_loss = loss
            if training:
                explicit_loss.backward()
                optim.step()

        # implicit training

        if implicitInstances:
            model.zero_grad()
            class_vec, type_vec, subtype_vec, relation_vec = model((case, disCon, arg1Idx, arg2Idx),tr_imipl[trainer_id])
            for label, weight in implicitInstances['class']:
                if is_cuda:
                    label = label.cuda()
                loss = weight * loss_fn(class_vec, label)
                implicit_losses_i += float(loss)
                if implicit_loss:
                    implicit_loss += loss
                else:
                    implicit_loss = loss

            for label, weight in implicitInstances['type']:
                if is_cuda:
                    label = label.cuda()
                loss = weight * loss_fn(type_vec, label)
                implicit_losses_i += float(loss)
                if implicit_loss:
                    implicit_loss += loss
                else:
                    implicit_loss = loss

            for label, weight in implicitInstances['subtype']:
                if is_cuda:
                    label = label.cuda()
                loss = weight * loss_fn(subtype_vec, label)
                implicit_losses_i += float(loss)
                if implicit_loss:
                    implicit_loss += loss
                else:
                    implicit_loss = loss
            if training:
                implicit_loss.backward()
                optim.step()

        return explicit_losses_i, implicit_losses_i


parser = argparse.ArgumentParser(description='Discourse Parser Training')
def main():

    parser.add_argument('--input_dim', type=int, default=25,
                        help='the dimension of the hidden layer to be used. Default=25')
    parser.add_argument('--hidden_dim', type=int, default=25,
                        help='the dimension of the hidden layer to be used. Default=25')
    parser.add_argument('--seed', type=int, default=1, help='random seed to use. Default=1')
    parser.add_argument('--nEpochs', type=int, default=1000, help='number of epochs to train for')
    parser.add_argument('--lr', type=float, default=0.01, help='Learning Rate. Default=0.01')
    parser.add_argument('--dropout', type=float, default=0.3, help='Dropout Rate. Default=0.3')
    parser.add_argument('--cuda', action='store_true', default=False, help='use cuda?')
    parser.add_argument('--grad', type=str, default='SGD', help='Optimzer type: SGD? Adam? Default=SGD')
    parser.add_argument('--mini_batch', type=int, default=None, help='Optimzer type: SGD? Adam? Default=SGD')


    parser.add_argument('--model', type=str, default='./Trained_Models/',
                        help='pretrained model')
    parser.add_argument('--word_embedding_dict', type=str, default='./glove_25.dict',
                        help='the path for language dict models')
    parser.add_argument('--test_file', type=str,
                        help='test file')

    
    parser.add_argument('--train_shuffle', type=str, default='no',
                        help='no/replace/shuffle')
   
    parser.add_argument('--num_direction', type=int, default=2,
                        help='# of direction of RNN for sentiment detection, Default=2 (bidirectional)')
    parser.add_argument('--num_layer', type=int, default=1,
                        help='# of direction of RNN layers')


    
    parser.add_argument('--cell_type', type=str, default='LSTM',
                        help='cell selection: LSTM / GRU')

    parser.add_argument('--attn_act', type=str, default='None',
                        help='Attention Activation Selection: None / Tanh / ReLU')

    parser.add_argument('--valid_perc', type=float, default=0.1,
                        help='Setting aside the validation set. Default=10%')




    # Parsing the arguments from the command
    opt = parser.parse_args()
    print(opt)
    input_dim=opt.input_dim
    hidden_dim=opt.hidden_dim
    learning_rate=opt.lr
    optimizer_type=opt.grad
    num_direction=opt.num_direction
    dropout_rate=opt.dropout



    is_cuda= opt.cuda
    sl=SL.SenseLabeller()
    
    # fix the seed as '1' for now
    torch.cuda.manual_seed(opt.seed)
    if is_cuda:
        torch.cuda.manual_seed(opt.seed)


    word_seqs_test=pickle.load(open(opt.tr_file,"rb"))

    # Separate validation set
    # final training
    train_end_idx=int((1-opt.valid_perc)*len(meta_orig_train))
    train_ids=orig_train_ids[:train_end_idx]

    

    input_dim=opt.input_dim
    train_size=len(train_ids)
    valid_size=len(dev_ids)

    model = DP.DiscourseParser(opt)
    model.load_state_dict(torch.load(opt.model_name))

    loss_function = nn.BCEWithLogitsLoss()
    
    if is_cuda:
        model = model.cuda()
        loss_function = loss_function.cuda()


    lowest_dev_loss= float('inf')
    # Training
    total_start=time.time()
    model.train()
    explicit_losses=0
    implicit_losses=0
    start=time.time()
    with torch.no_grad():
        for i in training_set:
            # iteration(is_cuda, msg_id, word_seqs, tr_meta, tr_inst, tr_imipl, loss_fn, optim, model, training):
            explicit_losses_i,implicit_losses_i=iteration(is_cuda, i, word_seqs_orig_train, meta_orig_train, meta_orig_trI_train, meta_orig_imp_WS_train, loss_function, optimizer, model, True)
            explicit_losses+=explicit_losses_i
            implicit_losses+=implicit_losses_i


        end_time=timeSince(start)
        total_time=timeSince(total_start)
        print('[',"Epoch #: " + str(epoch),']')
        print("Training Loss: " + str((explicit_losses+implicit_losses)/len(training_set)))
        print("Training Explicit Relation Loss:",explicit_losses/len(training_set))
        print("Training Implicit Relation Loss:", implicit_losses/len(training_set))
        print("Epoch Time: %s"%(end_time))
        print("Total Time: %s"%(total_time))

    
                

if __name__=="__main__":
    main()
