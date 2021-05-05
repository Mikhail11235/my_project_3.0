from django.db import models

import pandas as pd

from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer


class CsvFile(models.Model):

    file = models.FileField(upload_to='files/')
    image = models.CharField(max_length=100)
    miner_type = models.CharField(max_length=100, choices=(('heuristics_miner', 'heuristics miner'),
                                                           ('alpha_miner', 'alpha miner')))
        
    def __convert(self):
        self.file.seek(0)
        log = pd.read_csv(self.file)

        if self.miner_type == 'alpha_miner':
            net, initial_marking, final_marking = alpha_miner.apply(log)
            gviz = pn_visualizer.apply(net, initial_marking, final_marking)
            path = 'media/files/image_{}.png'.format(str(self.id))
            pn_visualizer.save(gviz, path)
        else:
            heu_net = heuristics_miner.apply_heu(log)
            gviz = hn_visualizer.apply(heu_net)
            path = 'media/files/image_{}.png'.format(str(self.id))
            hn_visualizer.save(gviz, path)

        self.image = path
        self.save(update_fields=["image"])

    def is_valid(self):
        self.file.seek(0)
        if self.file.name.split('.')[-1] != 'csv':
            return 'Invalid file type'
        else:
            try:
                eventlog_attrs = pd.read_csv(self.file).columns
                for correct_attr in ['case:concept:name', 'concept:name', 'time:timestamp']:
                    if not correct_attr in eventlog_attrs:
                        return 'This event log doesn\'t contain "{}"'.format(correct_attr)
            except:
                return 'error :('
        return 1

    def get_image(self):
        if not self.image:
            CsvFile.__convert(self)
        return self.image
