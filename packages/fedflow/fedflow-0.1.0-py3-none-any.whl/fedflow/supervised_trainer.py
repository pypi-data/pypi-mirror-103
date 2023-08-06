import os
import json

import torch
from torch.utils.data import random_split, DataLoader


class SupervisedTrainer(object):

    def __init__(self, device, model, optimizer, criterion, lr_scheduler=None, epoch=50,
                 dataset=None, batch_size=32,
                 epoch_action=None,
                 checkpoint_interval=10):
        super(SupervisedTrainer, self).__init__()
        self.device = device
        self.model = model
        self.optimizer = optimizer
        self.criterion = criterion
        self.lr_schduler = lr_scheduler
        self.epoch = epoch
        self.train_dataloader, self.val_dataloader = self.split_dataset(dataset, batch_size)
        self.epoch_action = epoch_action
        self.checkpoint_interval = checkpoint_interval
        self.history = {
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": [],
            "lr": []
        }

    def split_dataset(self, dataset, batch_size):
        if dataset is None:
            return None, None
        dataset_len = len(dataset)
        val_len = int(0.3 * dataset_len)
        train_len = dataset_len - val_len
        t, v = random_split(dataset, (train_len, val_len))
        return DataLoader(t, batch_size=batch_size, shuffle=True), DataLoader(v, batch_size=batch_size, shuffle=True)

    def train(self):
        self.__pre_train()
        with open("console.out", "w") as f:
            for e in range(self.epoch):
                t_loss, t_correct, t_total = self.__epoch_train(self.train_dataloader)
                with torch.no_grad():
                    v_loss, v_correct, v_total = self.__epoch_train(self.val_dataloader)
                f.write("EPOCH %d/%d\n" % (e + 1, self.epoch))
                f.write("\tTrain Loss: %.4f, Acc: %.2f%%\n" % (t_loss, 100 * t_correct / t_total))
                f.write("\tVal   Loss: %.4f, Acc: %.2f%%\n" % (v_loss, 100 * v_correct / v_total))
                f.flush()

                self.history["train_loss"].append(t_loss)
                self.history["train_acc"].append(t_correct / t_total)
                self.history["val_loss"].append(v_loss)
                self.history["val_acc"].append(v_correct / v_total)
                self.history["lr"].append(self.optimizer.param_groups[0]["lr"])

                if self.epoch_action is not None:
                    self.epoch_action(model=self.model, optimizer=self.optimizer, criterion=self.criterion)

                if self.lr_schduler is not None:
                    self.lr_schduler.step()

                if self.checkpoint_interval > 0:
                    if (e + 1) % self.checkpoint_interval == 0:
                        torch.save(self.model.state_dict(), "checkpoint/parameter-%d.checkpoint" % (e + 1))
                        torch.save(self.optimizer.state_dict(), "checkpoint/optimizer-%d.checkpoint" % (e + 1))
        self.__post_train()

    def __pre_train(self):
        os.makedirs("checkpoint", exist_ok=True)

    def __post_train(self):
        with open("history.json", "w") as f:
            f.write(json.dumps(self.history, indent=4))
        torch.save(self.model.state_dict(), "parameter.pth")
        torch.save(self.optimizer.state_dict(), "optimizer.pth")

    def __epoch_train(self, dataloader):
        correct = 0
        total = 0
        loss_total = 0
        iter_num = 0

        for i, data in enumerate(dataloader):
            inputs, labels = data
            inputs = inputs.to(self.device)
            labels = labels.to(self.device)

            if torch.is_grad_enabled():
                self.optimizer.zero_grad()

            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)

            if torch.is_grad_enabled():
                loss.backward()
                self.optimizer.step()

            loss_total += loss.item()
            iter_num += 1

            _, pred = torch.max(outputs, 1)
            c = (pred == labels)
            for i, lb in enumerate(labels):
                correct += c[i].item()
                total += 1

        return loss_total / iter_num, correct, total
