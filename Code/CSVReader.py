import pandas as pd
import numpy as np
import Objects

class Reader:
    def ReadCSVToObjectContainer(self,Filepath:str) -> Objects.ObjectContainer:

        AU_TO_M = 1.495978707e11        # 1 AU in meters
        AU_PER_DAY_TO_M_S = AU_TO_M / 86400.0  # AU/day → m/s


        df = pd.read_csv(Filepath)

        N = len(df)
        container = Objects.ObjectContainer(N)

        #string metadata
        container.names[:] = df['name'].values
        container.classes[:] = df['class'].values

        #numeric data
        container.ids[:] = df['id'].values.astype(np.int64)
        container.mass[:] = df['mass'].values.astype(np.float64)

        container.pos[:, 0] = df['pos_x'].values.astype(np.float64) * AU_TO_M
        container.pos[:, 1] = df['pos_y'].values.astype(np.float64) * AU_TO_M
        container.pos[:, 2] = df['pos_z'].values.astype(np.float64) * AU_TO_M

        container.vel[:, 0] = df['vel_x'].values.astype(np.float64) * AU_PER_DAY_TO_M_S
        container.vel[:, 1] = df['vel_y'].values.astype(np.float64) * AU_PER_DAY_TO_M_S
        container.vel[:, 2] = df['vel_z'].values.astype(np.float64) * AU_PER_DAY_TO_M_S

        container.acc[:] = 0.0 #acc 0 for start

        return container