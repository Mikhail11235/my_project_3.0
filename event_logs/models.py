from django.db import models

import pandas as pd

from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer


class CsvFile(models.Model):

    file = models.FileField(upload_to='files/')
    miner_type = models.CharField(max_length=100, choices=(('heuristics_miner', 'heuristics miner'),
                                                           ('alpha_miner', 'alpha miner')))

    def file_is_valid(self):
        self.file.seek(0)
        if self.file.name.split('.')[-1] != 'csv':
            return 0
        else:
            try:
                eventlog_attrs = pd.read_csv(self.file).columns
                for correct_attr in ['case:concept:name', 'concept:name', 'time:timestamp']:
                    if not correct_attr in eventlog_attrs:
                        return 0
            except:
                return 0
        return 1


class ModelImage(models.Model):
    image = models.CharField(max_length=100, null=True)
    file = models.ForeignKey(CsvFile, on_delete=models.CASCADE, null=True)

    def __convert(self, file, miner_type):
        file.seek(0)
        log = pd.read_csv(file)

        if miner_type == 'alpha_miner':
            net, initial_marking, final_marking = alpha_miner.apply(log)
            gviz = pn_visualizer.apply(net, initial_marking, final_marking)
            path = 'media/files/image_{}.png'.format(str(self.file_id))
            pn_visualizer.save(gviz, path)
        else:
            heu_net = heuristics_miner.apply_heu(log)
            gviz = hn_visualizer.apply(heu_net)
            path = 'media/files/image_{}.png'.format(str(self.file_id))
            hn_visualizer.save(gviz, path)

        self.image = path
        self.save(update_fields=["image"])

    def get_image(self):
        instance = CsvFile.objects.get(pk=self.file_id)
        file, miner_type = instance.file, instance.miner_type
        if not self.image:
            ModelImage.__convert(self, file, miner_type)
        return self.image
