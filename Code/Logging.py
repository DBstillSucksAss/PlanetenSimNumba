import os
import csv
import numpy as np

def LogState(Timestep: int, Container, DataToLog: list[str], Path: str):
    """
    Loggt den aktuellen Zustand des Systems in eine CSV 

    Eine Reihe pro Objekt pro Zeitstep

    Parameter:

    Timestep : int
        Momentaner Zeitstep
    Container : ObjectContainer
        DatenContainer
    DataToLog : list[str]
        Name der zu loggenden Attribute
        (z.B. ["id", "mass", "pos", "vel"]).
    Path : str
        Pfad zum CSV file.
    """
    if Timestep == 0 and os.path.exists(Path):
        os.remove(Path)

    write_header = not os.path.exists(Path)

    with open(Path, mode="a", newline="") as f:
        writer = csv.writer(f)

        #Header schreiben, falls File New erstellt
        if write_header:
            header = ["timestep", "object_index"]

            for name in DataToLog:
                data = getattr(Container, name)

                if data.ndim == 1:
                    header.append(name)
                elif data.ndim == 2:
                    for i in range(data.shape[1]):
                        header.append(f"{name}_{i}")
                else:
                    raise ValueError(f"Unsupported data shape for '{name}'")

            writer.writerow(header)

        # Loggen
        for i in range(Container.N):
            row = [Timestep, i]

            for name in DataToLog:
                data = getattr(Container, name)

                if data.ndim == 1:
                    row.append(data[i])
                elif data.ndim == 2:
                    row.extend(data[i])
                else:
                    raise ValueError(f"Unsupported data shape for '{name}'")

            writer.writerow(row)